import pandas as pd
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula los indicadores utilizados para analizar la tendencia.
    """

    data = df.copy()

    # Medias móviles
    data["ema_20"] = EMAIndicator(
        close=data["close"],
        window=20
    ).ema_indicator()

    data["ema_50"] = EMAIndicator(
        close=data["close"],
        window=50
    ).ema_indicator()

    # ATR para medir volatilidad
    atr = AverageTrueRange(
        high=data["high"],
        low=data["low"],
        close=data["close"],
        window=14
    )

    data["atr"] = atr.average_true_range()

    data["atr_percent"] = (
        data["atr"] / data["close"]
    ) * 100

    # Volumen medio
    data["volume_ma"] = (
        data["volume"]
        .rolling(window=20)
        .mean()
    )

    # Relación entre volumen actual y volumen medio
    data["volume_ratio"] = (
        data["volume"] / data["volume_ma"]
    )

    return data


def detect_structure(df: pd.DataFrame) -> str:
    """
    Detecta de forma sencilla la estructura reciente del precio.
    """

    if len(df) < 20:
        return "NEUTRAL"

    recent = df.tail(20)

    first_half = recent.iloc[:10]
    second_half = recent.iloc[10:]

    first_high = first_half["high"].max()
    second_high = second_half["high"].max()

    first_low = first_half["low"].min()
    second_low = second_half["low"].min()

    higher_high = second_high > first_high
    higher_low = second_low > first_low

    lower_high = second_high < first_high
    lower_low = second_low < first_low

    if higher_high and higher_low:
        return "BULLISH"

    if lower_high and lower_low:
        return "BEARISH"

    return "NEUTRAL"


def calculate_trend_score(data: pd.DataFrame) -> dict:
    """
    Calcula una puntuación de confluencia LONG/SHORT.

    El score NO representa una probabilidad real de ganar.
    Es una medida de cuántas condiciones están alineadas.
    """

    latest = data.iloc[-1]

    price = latest["close"]
    ema_20 = latest["ema_20"]
    ema_50 = latest["ema_50"]
    volume_ratio = latest["volume_ratio"]

    structure = detect_structure(data)

    long_score = 0
    short_score = 0

    # ----------------------------------------
    # MEDIAS MÓVILES
    # ----------------------------------------

    if price > ema_20:
        long_score += 20

    if price < ema_20:
        short_score += 20

    if ema_20 > ema_50:
        long_score += 20

    if ema_20 < ema_50:
        short_score += 20

    # ----------------------------------------
    # ESTRUCTURA
    # ----------------------------------------

    if structure == "BULLISH":
        long_score += 30

    elif structure == "BEARISH":
        short_score += 30

    # ----------------------------------------
    # VOLUMEN
    # ----------------------------------------

    if volume_ratio < 0.50:
        volume_status = "MUY BAJO"

    elif volume_ratio < 0.80:
        volume_status = "BAJO"

    elif volume_ratio < 1.20:
        volume_status = "NORMAL"

    else:
        volume_status = "FUERTE"

    # El volumen acompaña la dirección
    # cuando es NORMAL o FUERTE.
    if volume_status in ("NORMAL", "FUERTE"):

        if long_score > short_score:
            long_score += 20

        elif short_score > long_score:
            short_score += 20

    # ----------------------------------------
    # DECISIÓN
    # ----------------------------------------

    if long_score >= 60 and long_score > short_score:
        direction = "LONG"

    elif short_score >= 60 and short_score > long_score:
        direction = "SHORT"

    else:
        direction = "NO_TRADE"

    return {
        "direction": direction,
        "volume_status": volume_status,
        "long_score": long_score,
        "short_score": short_score,
        "structure": structure,
        "price": price,
        "ema_20": ema_20,
        "ema_50": ema_50,
        "volume_ratio": volume_ratio,
        "atr": latest["atr"],
        "atr_percent": latest["atr_percent"],
    }


def analyze_15m(df: pd.DataFrame) -> dict:
    """
    Ejecuta el análisis completo del timeframe 15M.
    """

    data = calculate_indicators(df)

    return calculate_trend_score(data)

def analyze_5m(df: pd.DataFrame) -> dict:
    """
    Ejecuta el análisis completo del timeframe 5M.
    """
    data = calculate_indicators(df)

    return calculate_trend_score(data)

def analyze_1m(df: pd.DataFrame) -> dict:
    """
    Ejecuta el análisis completo del timeframe 1M.
    """
    data = calculate_indicators(df)

    return calculate_trend_score(data)    