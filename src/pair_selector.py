import pandas as pd

from src.binance_client import get_futures_klines
from src.trend_detector import analyze_15m


# ============================================================
# CONFIGURACIÓN DEL SELECTOR
# ============================================================

DEFAULT_MAX_PAIRS = 10
DEFAULT_LIQUIDITY_CANDIDATES = 50


# ============================================================
# 1. OBTENER CONTRATOS USDT-M PERPETUOS
# ============================================================

def get_eligible_symbols(client):
    """
    Obtiene los contratos USDT-M perpetuos activos.
    """

    exchange_info = client.futures_exchange_info()

    eligible_symbols = []

    for symbol_info in exchange_info["symbols"]:

        if symbol_info["status"] != "TRADING":
            continue

        if symbol_info["contractType"] != "PERPETUAL":
            continue

        if symbol_info["quoteAsset"] != "USDT":
            continue

        eligible_symbols.append(symbol_info["symbol"])

    return eligible_symbols


# ============================================================
# 2. OBTENER DATOS DE MERCADO 24H
# ============================================================

def get_24h_market_data(client):
    """
    Obtiene información de mercado de todos los contratos
    Futures USDT-M.
    """

    tickers = client.futures_ticker()

    rows = []

    for ticker in tickers:

        symbol = ticker.get("symbol")

        if not symbol:
            continue

        try:
            quote_volume = float(
                ticker.get("quoteVolume", 0)
            )

            price_change_percent = float(
                ticker.get("priceChangePercent", 0)
            )

            last_price = float(
                ticker.get("lastPrice", 0)
            )

        except (TypeError, ValueError):
            continue

        rows.append(
            {
                "symbol": symbol,
                "quote_volume": quote_volume,
                "price_change_percent": price_change_percent,
                "last_price": last_price,
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# 3. PUNTAJE DE LIQUIDEZ
# ============================================================

def calculate_liquidity_score(
    quote_volume,
    minimum_volume,
    maximum_volume,
):
    """
    Puntúa la liquidez 24H de 0 a 40.

    Se utiliza una escala relativa dentro del grupo
    de candidatos analizados.
    """

    if quote_volume <= 0:
        return 0.0

    if maximum_volume <= minimum_volume:
        return 20.0

    normalized = (
        (quote_volume - minimum_volume)
        / (maximum_volume - minimum_volume)
    )

    normalized = max(0.0, min(1.0, normalized))

    return normalized * 40.0


# ============================================================
# 4. PUNTAJE DE VOLUMEN 15M
# ============================================================

def calculate_volume_score(volume_ratio):
    """
    Puntúa el volumen actual de 15M.

    El volumen demasiado bajo no interesa para scalping.
    Un volumen fuerte aumenta la prioridad del par.

    Máximo: 25 puntos.
    """

    if volume_ratio < 0.50:
        return 0.0

    if volume_ratio < 0.80:
        return 8.0

    if volume_ratio < 1.20:
        return 15.0

    if volume_ratio < 1.50:
        return 20.0

    return 25.0


# ============================================================
# 5. PUNTAJE DE TENDENCIA
# ============================================================

def calculate_trend_quality_score(analysis_15m):
    """
    Puntúa la claridad de la tendencia de 15M.

    Máximo: 25 puntos.
    """

    direction = analysis_15m["direction"]

    if direction == "NO_TRADE":
        return 0.0

    structure = analysis_15m["structure"]

    score = 10.0

    if structure == direction_map(direction):
        score += 5.0

    long_score = analysis_15m["long_score"]
    short_score = analysis_15m["short_score"]

    direction_score = max(
        long_score,
        short_score
    )

    if direction_score >= 90:
        score += 10.0

    elif direction_score >= 70:
        score += 7.0

    elif direction_score >= 60:
        score += 4.0

    return min(score, 25.0)


def direction_map(direction):
    """
    Convierte la dirección del análisis a la estructura esperada.
    """

    if direction == "LONG":
        return "BULLISH"

    if direction == "SHORT":
        return "BEARISH"

    return "NEUTRAL"


# ============================================================
# 6. PUNTAJE DE VOLATILIDAD
# ============================================================

def calculate_volatility_score(atr_percent):
    """
    Puntúa la volatilidad de 15M.

    Para scalping buscamos movimiento suficiente,
    pero evitamos extremos de volatilidad.

    Máximo: 10 puntos.
    """

    if atr_percent <= 0:
        return 0.0

    if atr_percent < 0.10:
        return 2.0

    if atr_percent < 0.25:
        return 5.0

    if atr_percent < 0.50:
        return 8.0

    if atr_percent < 1.00:
        return 10.0

    if atr_percent < 2.00:
        return 8.0

    if atr_percent < 3.00:
        return 5.0

    return 2.0


# ============================================================
# 7. PUNTAJE TOTAL
# ============================================================

def calculate_total_score(
    liquidity_score,
    volume_score,
    trend_score,
    volatility_score,
):
    """
    Calcula el puntaje total del candidato.

    Máximo teórico: 100.
    """

    return (
        liquidity_score
        + volume_score
        + trend_score
        + volatility_score
    )


# ============================================================
# 8. SELECTOR PRINCIPAL
# ============================================================

def select_pairs(
    client,
    max_pairs: int = DEFAULT_MAX_PAIRS,
    liquidity_candidates: int = DEFAULT_LIQUIDITY_CANDIDATES,
) -> list[dict]:
    """
    Selecciona pares candidatos para scalping.

    Proceso:

    1. Obtiene contratos USDT-M perpetuos.
    2. Obtiene volumen 24H.
    3. Ordena por liquidez.
    4. Toma los candidatos más líquidos.
    5. Analiza 15M.
    6. Descarta NO_TRADE.
    7. Descarta volumen 15M MUY BAJO.
    8. Calcula puntaje de liquidez.
    9. Calcula puntaje de volumen.
    10. Calcula calidad de tendencia.
    11. Calcula volatilidad.
    12. Ordena por puntaje total.
    13. Devuelve máximo max_pairs.

    IMPORTANTE:
    Este módulo NO abre operaciones.
    """

    print()
    print("=" * 60)
    print("DIAGNÓSTICO DEL SELECTOR")
    print("=" * 60)

    # --------------------------------------------------------
    # OBTENER SÍMBOLOS
    # --------------------------------------------------------

    eligible_symbols = get_eligible_symbols(client)

    print(
        f"CONTRATOS USDT-M PERPETUOS: "
        f"{len(eligible_symbols)}"
    )

    # --------------------------------------------------------
    # DATOS 24H
    # --------------------------------------------------------

    market_data = get_24h_market_data(client)

    if market_data.empty:
        print("ERROR: Binance no devolvió datos 24H.")
        return []

    # Mantener únicamente contratos elegibles

    market_data = market_data[
        market_data["symbol"].isin(eligible_symbols)
    ].copy()

    # Eliminar volúmenes inválidos

    market_data = market_data[
        market_data["quote_volume"] > 0
    ].copy()

    # Ordenar por volumen 24H

    market_data = market_data.sort_values(
        "quote_volume",
        ascending=False,
    )

    # Tomar candidatos

    candidates = market_data.head(
        liquidity_candidates
    ).copy()

    print(
        f"CANDIDATOS DE LIQUIDEZ: "
        f"{len(candidates)}"
    )

    if candidates.empty:
        print("NO HAY CANDIDATOS DISPONIBLES.")
        return []

    # Valores para normalizar liquidez

    minimum_volume = candidates[
        "quote_volume"
    ].min()

    maximum_volume = candidates[
        "quote_volume"
    ].max()

    # --------------------------------------------------------
    # CONTADORES DEL DIAGNÓSTICO
    # --------------------------------------------------------

    analyzed = 0
    discarded_no_trade = 0
    discarded_low_volume = 0
    errors = 0

    opportunities = []

    # --------------------------------------------------------
    # ANALIZAR CADA CANDIDATO
    # --------------------------------------------------------

    for _, row in candidates.iterrows():

        symbol = row["symbol"]

        analyzed += 1

        try:

            # ------------------------------------------------
            # DATOS 15M
            # ------------------------------------------------

            df_15m = get_futures_klines(
                client,
                symbol,
                "15m",
                200,
            )

            analysis_15m = analyze_15m(
                df_15m
            )

            # ------------------------------------------------
            # FILTRO 1: DIRECCIÓN
            # ------------------------------------------------

            if analysis_15m["direction"] == "NO_TRADE":

                discarded_no_trade += 1

                continue

            # ------------------------------------------------
            # FILTRO 2: VOLUMEN 15M
            # ------------------------------------------------

            if (
                analysis_15m["volume_status"]
                == "MUY BAJO"
            ):

                discarded_low_volume += 1

                continue

            # ------------------------------------------------
            # PUNTAJES
            # ------------------------------------------------

            liquidity_score = calculate_liquidity_score(
                row["quote_volume"],
                minimum_volume,
                maximum_volume,
            )

            volume_score = calculate_volume_score(
                analysis_15m["volume_ratio"]
            )

            trend_score = calculate_trend_quality_score(
                analysis_15m
            )

            volatility_score = calculate_volatility_score(
                analysis_15m["atr_percent"]
            )

            total_score = calculate_total_score(
                liquidity_score,
                volume_score,
                trend_score,
                volatility_score,
            )

            # ------------------------------------------------
            # GUARDAR OPORTUNIDAD
            # ------------------------------------------------

            opportunities.append(
                {
                    "symbol": symbol,

                    "direction_15m":
                        analysis_15m["direction"],

                    "structure_15m":
                        analysis_15m["structure"],

                    "volume_status_15m":
                        analysis_15m["volume_status"],

                    "volume_ratio_15m":
                        analysis_15m["volume_ratio"],

                    "atr_percent_15m":
                        analysis_15m["atr_percent"],

                    "quote_volume_24h":
                        row["quote_volume"],

                    "liquidity_score":
                        liquidity_score,

                    "volume_score":
                        volume_score,

                    "trend_score":
                        trend_score,

                    "volatility_score":
                        volatility_score,

                    "total_score":
                        total_score,
                }
            )

        except Exception as error:

            errors += 1

            print(
                f"{symbol} -> ERROR: {error}"
            )

    # --------------------------------------------------------
    # ORDENAR OPORTUNIDADES
    # --------------------------------------------------------

    opportunities.sort(
        key=lambda item: item["total_score"],
        reverse=True,
    )

    # --------------------------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("DIAGNÓSTICO DEL SELECTOR")
    print("=" * 60)

    print(
        f"CANDIDATOS ANALIZADOS: "
        f"{analyzed}"
    )

    print(
        f"DESCARTADOS POR NO_TRADE: "
        f"{discarded_no_trade}"
    )

    print(
        f"DESCARTADOS POR VOLUMEN MUY BAJO: "
        f"{discarded_low_volume}"
    )

    print(
        f"ERRORES: "
        f"{errors}"
    )

    print(
        f"CANDIDATOS APTOS: "
        f"{len(opportunities)}"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # SELECCIÓN FINAL
    # --------------------------------------------------------

    selected = opportunities[
        :max_pairs
    ]

    print()
    print(
        f"PARES SELECCIONADOS: "
        f"{len(selected)}"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # MOSTRAR RANKING
    # --------------------------------------------------------

    for position, opportunity in enumerate(
        selected,
        start=1,
    ):

        print(
            f"{position:02d}. "
            f"{opportunity['symbol']} | "
            f"{opportunity['direction_15m']} | "
            f"Score: "
            f"{opportunity['total_score']:.1f} | "
            f"Vol15M: "
            f"{opportunity['volume_ratio_15m']:.2f}x | "
            f"ATR: "
            f"{opportunity['atr_percent_15m']:.2f}%"
        )

    print("=" * 60)

    return selected