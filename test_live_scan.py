from src.binance_client import (
    create_public_client,
    get_futures_klines,
)

from src.trend_detector import (
    analyze_15m,
    analyze_5m,
    analyze_1m,
)

from src.entry_trigger import (
    detect_entry_trigger,
)

from src.entry_filter import (
    evaluate_entry_filter,
)

from src.range_position import (
    calculate_range_position,
)

from src.grid_engine import (
    build_dynamic_grid,
)

from src.operation_planner import (
    build_operation_plan,
)

from src.config import (
    INITIAL_CAPITAL,
    OPERATING_CAPITAL_PERCENT,
    LEVERAGE,
)


client = create_public_client()

symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
]


operating_capital = (
    INITIAL_CAPITAL
    * OPERATING_CAPITAL_PERCENT
)


for symbol in symbols:

    print()
    print("=" * 70)
    print(f"SCALPING: {symbol}")
    print("=" * 70)

    try:

        # ==========================================================
        # 1. OBTENER DATOS
        # ==========================================================

        df_15m = get_futures_klines(
            client,
            symbol,
            "15m",
            limit=200
        )

        df_5m = get_futures_klines(
            client,
            symbol,
            "5m",
            limit=200
        )

        df_1m = get_futures_klines(
            client,
            symbol,
            "1m",
            limit=200
        )

        # ==========================================================
        # 2. ANALIZAR TEMPORALIDADES
        # ==========================================================

        analysis_15m = analyze_15m(df_15m)

        analysis_5m = analyze_5m(df_5m)

        analysis_1m = analyze_1m(df_1m)

        # ==========================================================
        # 3. TRIGGER DE ENTRADA
        # ==========================================================

        entry_trigger = detect_entry_trigger(
            df_1m,
            analysis_1m["direction"]
        )

        # ==========================================================
        # 4. EVALUAR ESTRATEGIA
        # ==========================================================

        direction_15m = analysis_15m["direction"]
        direction_5m = analysis_5m["direction"]
        direction_1m = analysis_1m["direction"]

        trigger = entry_trigger["trigger"]
        trigger_direction = entry_trigger["direction"]

        strategy_direction = "WAIT"

        if (
            direction_15m == "LONG"
            and direction_5m == "LONG"
            and direction_1m == "LONG"
            and trigger
            and trigger_direction == "LONG"
        ):
            strategy_direction = "LONG"

        elif (
            direction_15m == "SHORT"
            and direction_5m == "SHORT"
            and direction_1m == "SHORT"
            and trigger
            and trigger_direction == "SHORT"
        ):
            strategy_direction = "SHORT"

        # ==========================================================
        # 5. MOSTRAR ANÁLISIS
        # ==========================================================

        print()
        print("ANÁLISIS")
        print("-" * 70)

        print(
            f"15M: {direction_15m}"
        )

        print(
            f"5M: {direction_5m}"
        )

        print(
            f"1M: {direction_1m}"
        )

        print(
            f"TRIGGER: {trigger}"
        )

        print(
            f"DIRECCIÓN TRIGGER: {trigger_direction}"
        )

        print(
            f"DECISIÓN ESTRATÉGICA: {strategy_direction}"
        )

        print(
            f"MOTIVO TRIGGER: "
            f"{entry_trigger.get('reason', '')}"
        )

        # ==========================================================
        # 6. SI NO HAY OPERACIÓN, ESPERAR
        # ==========================================================

        if strategy_direction == "WAIT":

            print()
            print("RESULTADO: WAIT")
            print("No se cumplen todas las condiciones.")

            continue

        # ==========================================================
        # 7. CONSTRUIR RANGO Y GRID DINÁMICO
        # ==========================================================

        grid_result = build_dynamic_grid(
            df_15m,
            lookback=50
        )

        if not grid_result["valid"]:

            print()
            print("RESULTADO: WAIT")
            print("Grid dinámico no válido.")

            continue

        range_low = grid_result["range_low"]
        range_high = grid_result["range_high"]

        current_price = grid_result["current_price"]

        # ==========================================================
        # 8. POSICIÓN DENTRO DEL RANGO
        # ==========================================================

        range_result = calculate_range_position(
            current_price,
            range_low,
            range_high
        )

        position_percent = (
            range_result["position_percent"]
        )

        zone = range_result["zone"]

        # ==========================================================
        # 9. FILTRO DE ENTRADA
        # ==========================================================

        entry_filter = evaluate_entry_filter(
            direction=strategy_direction,
            trigger=trigger,
            trigger_direction=trigger_direction,
            position_percent=position_percent,
        )

        print()
        print("RANGO")
        print("-" * 70)

        print(
            f"RANGE LOW: {range_low}"
        )

        print(
            f"RANGE HIGH: {range_high}"
        )

        print(
            f"PRECIO ACTUAL: {current_price}"
        )

        print(
            f"POSICIÓN EN RANGO: "
            f"{position_percent:.2f}%"
        )

        print(
            f"ZONA: {zone}"
        )

        print()
        print("FILTRO DE ENTRADA")
        print("-" * 70)

        print(
            f"RESULTADO: "
            f"{entry_filter['decision']}"
        )

        print(
            f"MOTIVO: "
            f"{entry_filter['reason']}"
        )

        # ==========================================================
        # 10. SI EL FILTRO RECHAZA, NO ENTRAR
        # ==========================================================

        if entry_filter["decision"] != "ENTRY":

            print()
            print("RESULTADO FINAL: WAIT")
            print("El filtro de entrada rechazó la operación.")

            continue

        # ==========================================================
        # 11. CREAR PLAN DE GRID
        # ==========================================================

        grid_plan = {
            "valid": True,
            "direction": strategy_direction,
            "range_low": range_low,
            "range_high": range_high,
            "levels": grid_result["levels"],
            "grid_levels": grid_result["grid"],
            "spacing": grid_result["spacing"],
            "reason": "Grid dinámico válido",
        }

        # ==========================================================
        # 12. CREAR PLAN DE OPERACIÓN
        # ==========================================================

        operation_plan = build_operation_plan(
            symbol=symbol,
            direction=strategy_direction,
            current_price=current_price,
            operating_capital=operating_capital,
            leverage=LEVERAGE,
            grid_plan=grid_plan,
        )

        # ==========================================================
        # 13. MOSTRAR PLAN COMPLETO
        # ==========================================================

        print()
        print("=" * 70)
        print("OPERACIÓN DETECTADA")
        print("=" * 70)

        print(
            f"SYMBOL: "
            f"{operation_plan['symbol']}"
        )

        print(
            f"DIRECTION: "
            f"{operation_plan['direction']}"
        )

        print(
            f"ENTRY: "
            f"{operation_plan['entry']}"
        )

        print(
            f"TAKE PROFIT: "
            f"{operation_plan['take_profit']}"
        )

        print(
            f"STOP LOSS: "
            f"{operation_plan['stop_loss']}"
        )

        print(
            f"OPERATING CAPITAL: "
            f"{operation_plan['operating_capital']:.4f}"
        )

        print(
            f"LEVERAGE: "
            f"{operation_plan['leverage']}x"
        )

        print(
            f"NOMINAL: "
            f"{operation_plan['nominal']:.4f}"
        )

        print(
            f"GRID LEVELS: "
            f"{operation_plan['levels']}"
        )

        print(
            f"GRID SPACING: "
            f"{operation_plan['spacing']}"
        )

        print()
        print("STATUS: READY")
        print("SIN ORDEN ENVIADA A BINANCE")

    except Exception as error:

        print()
        print(
            f"ERROR EN {symbol}: {error}"
        )


print()
print("=" * 70)
print("FIN DEL SCAN")
print("=" * 70)