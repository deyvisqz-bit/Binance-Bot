
from typing import Any

from src.binance_client import get_futures_klines
from src.pair_selector import select_pairs
from src.trend_detector import (
    analyze_15m,
    analyze_5m,
    analyze_1m,
)
from src.entry_trigger import detect_entry_trigger
from src.strategy import evaluate_scalping_setup
from src.grid_engine import build_dynamic_grid
from src.range_position import calculate_range_position
from src.entry_filter import evaluate_entry_filter


def _get_direction(result: dict) -> str:
    """Extrae LONG, SHORT o WAIT de un análisis."""

    for key in ("direction", "final_direction", "signal"):
        value = result.get(key)

        if isinstance(value, str):
            value = value.upper()

            if value in ("LONG", "SHORT"):
                return value

    return "WAIT"


def _get_price(data: Any) -> float:
    """Obtiene el último precio disponible de las velas."""

    if data is None or len(data) == 0:
        raise ValueError("No hay datos de precio.")

    return float(data.iloc[-1]["close"])


def _build_result(
    symbol: str,
    decision: str,
    reason: str,
    price: float | None = None,
    direction: str = "WAIT",
    analysis_15m: dict | None = None,
    analysis_5m: dict | None = None,
    analysis_1m: dict | None = None,
    trigger: dict | None = None,
    range_position: dict | None = None,
    grid_plan: dict | None = None,
    entry_filter: dict | None = None,
) -> dict:

    return {
        "symbol": symbol,
        "decision": decision,
        "direction": direction,
        "price": price,
        "reason": reason,
        "trend_15m": analysis_15m,
        "trend_5m": analysis_5m,
        "trend_1m": analysis_1m,
        "trigger": trigger,
        "range_position": range_position,
        "grid_plan": grid_plan,
        "entry_filter": entry_filter,
    }


def analyze_candidate(client: Any, candidate: dict) -> dict:
    """
    Analiza un par en 15M, 5M y 1M.
    Devuelve ENTRY o WAIT.
    No ejecuta órdenes.
    """

    symbol = candidate.get("symbol", "UNKNOWN")

    try:
        # 1. Obtener datos de mercado.
        data_15m = get_futures_klines(
            client, symbol, "15m", limit=200
        )

        data_5m = get_futures_klines(
            client, symbol, "5m", limit=200
        )

        data_1m = get_futures_klines(
            client, symbol, "1m", limit=200
        )

        if any(
            data is None or len(data) < 30
            for data in (data_15m, data_5m, data_1m)
        ):
            return _build_result(
                symbol,
                "WAIT",
                "Datos insuficientes para analizar el par.",
            )

        # 2. Obtener precio.
        current_price = _get_price(data_1m)

        # 3. Analizar los tres marcos temporales.
        analysis_15m = analyze_15m(data_15m)
        analysis_5m = analyze_5m(data_5m)
        analysis_1m = analyze_1m(data_1m)

        direction_15m = _get_direction(analysis_15m)

        # 4. Buscar trigger en 1M.
        trigger = detect_entry_trigger(
            data_1m,
            direction_15m,
        )

        # 5. Evaluar alineación de tendencias.
        strategy_result = evaluate_scalping_setup(
            analysis_15m,
            analysis_5m,
            analysis_1m,
            trigger,
        )

        direction = _get_direction(strategy_result)

        if direction == "WAIT":
            reason = strategy_result.get(
                "reason",
                "No existe confirmación de los tres marcos temporales.",
            )

            return _build_result(
                symbol=symbol,
                decision="WAIT",
                reason=reason,
                price=current_price,
                analysis_15m=analysis_15m,
                analysis_5m=analysis_5m,
                analysis_1m=analysis_1m,
                trigger=trigger,
            )

        # 6. Construir rango dinámico.
        grid_plan = build_dynamic_grid(
            data_15m,
            lookback=50,
        )

        if not grid_plan or not grid_plan.get("valid"):
            return _build_result(
                symbol=symbol,
                decision="WAIT",
                reason="El rango dinámico no es válido.",
                price=current_price,
                direction=direction,
                analysis_15m=analysis_15m,
                analysis_5m=analysis_5m,
                analysis_1m=analysis_1m,
                trigger=trigger,
                grid_plan=grid_plan,
            )

        range_min = grid_plan.get("range_low")
        range_max = grid_plan.get("range_high")

        if range_min is None or range_max is None:
            return _build_result(
                symbol=symbol,
                decision="WAIT",
                reason="El rango no contiene límites válidos.",
                price=current_price,
                direction=direction,
                analysis_15m=analysis_15m,
                analysis_5m=analysis_5m,
                analysis_1m=analysis_1m,
                trigger=trigger,
                grid_plan=grid_plan,
            )

        # 7. Calcular posición dentro del rango.
        position = calculate_range_position(
            current_price,
            float(range_min),
            float(range_max),
        )

        # 8. Aplicar filtro final.
        filter_result = evaluate_entry_filter(
            direction=direction,
            trigger=trigger.get("trigger", False),
            trigger_direction=trigger.get("direction", "WAIT"),
            position_percent=position["position_percent"],
        )

        decision = filter_result.get("decision", "WAIT")

        return _build_result(
            symbol=symbol,
            decision=decision,
            reason=filter_result.get("reason", ""),
            price=current_price,
            direction=direction if decision == "ENTRY" else "WAIT",
            analysis_15m=analysis_15m,
            analysis_5m=analysis_5m,
            analysis_1m=analysis_1m,
            trigger=trigger,
            range_position=position,
            grid_plan=grid_plan,
            entry_filter=filter_result,
        )

    except Exception as error:
        return _build_result(
            symbol=symbol,
            decision="WAIT",
            reason=f"Error durante el análisis: {error}",
        )


def run_market_pipeline(
    client: Any,
    max_pairs: int = 10,
) -> dict:
    """Ejecuta el análisis completo de los pares seleccionados."""

    try:
        candidates = select_pairs(
            client,
            max_pairs=max_pairs,
        )

        results = []

        for candidate in candidates:
            result = analyze_candidate(client, candidate)
            results.append(result)

        entries = [
            item for item in results
            if item["decision"] == "ENTRY"
        ]

        waits = [
            item for item in results
            if item["decision"] != "ENTRY"
        ]

        return {
            "success": True,
            "pairs_analyzed": len(results),
            "entries_found": len(entries),
            "waiting": len(waits),
            "entries": entries,
            "results": results,
        }

    except Exception as error:
        return {
            "success": False,
            "pairs_analyzed": 0,
            "entries_found": 0,
            "waiting": 0,
            "entries": [],
            "results": [],
            "error": str(error),
        }
