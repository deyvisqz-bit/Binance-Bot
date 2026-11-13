
import math
import pandas as pd


VOLUME_THRESHOLD = 1.2
MIN_CANDLES = 30


def detect_entry_trigger(
    df: pd.DataFrame,
    direction: str,
) -> dict:
    """
    Detecta un trigger de entrada utilizando velas cerradas.

    LONG:
        EMA 7 > EMA 25
        Precio > EMA 7
        Volumen confirmado

    SHORT:
        EMA 7 < EMA 25
        Precio < EMA 7
        Volumen confirmado

    También permite detectar un cruce reciente de EMA.
    No ejecuta órdenes.
    """

    direction = str(direction).upper()

    if direction not in ("LONG", "SHORT"):
        return {
            "trigger": False,
            "direction": "WAIT",
            "reason": "Dirección no válida.",
        }

    if df is None or len(df) < MIN_CANDLES:
        return {
            "trigger": False,
            "direction": direction,
            "reason": "Datos insuficientes.",
        }

    required_columns = {"close", "volume"}

    if not required_columns.issubset(df.columns):
        return {
            "trigger": False,
            "direction": direction,
            "reason": "Faltan columnas close o volume.",
        }

    data = df.copy()

    data["close"] = pd.to_numeric(
        data["close"], errors="coerce"
    )

    data["volume"] = pd.to_numeric(
        data["volume"], errors="coerce"
    )

    data = data.dropna(
        subset=["close", "volume"]
    ).reset_index(drop=True)

    if len(data) < MIN_CANDLES:
        return {
            "trigger": False,
            "direction": direction,
            "reason": "Datos válidos insuficientes.",
        }

    # Calcular medias móviles.
    data["ema_7"] = data["close"].ewm(
        span=7,
        adjust=False,
    ).mean()

    data["ema_25"] = data["close"].ewm(
        span=25,
        adjust=False,
    ).mean()

    # Utilizar exclusivamente velas cerradas.
    # La última fila se considera la vela en formación.
    current = data.iloc[-2]
    previous = data.iloc[-3]

    price = float(current["close"])
    volume = float(current["volume"])

    ema_7 = float(current["ema_7"])
    ema_25 = float(current["ema_25"])

    previous_ema_7 = float(previous["ema_7"])
    previous_ema_25 = float(previous["ema_25"])

    values = [
        price,
        volume,
        ema_7,
        ema_25,
        previous_ema_7,
        previous_ema_25,
    ]

    if not all(math.isfinite(value) for value in values):
        return {
            "trigger": False,
            "direction": direction,
            "reason": "Indicadores contienen valores no válidos.",
        }

    # Comparar el volumen de la vela cerrada con las
    # 20 velas cerradas anteriores.
    previous_volumes = data["volume"].iloc[-22:-2]

    if len(previous_volumes) < 20:
        return {
            "trigger": False,
            "direction": direction,
            "reason": "Historial de volumen insuficiente.",
        }

    average_volume = float(previous_volumes.mean())

    if average_volume > 0:
        volume_ratio = volume / average_volume
    else:
        volume_ratio = 0.0

    volume_confirmed = (
        volume_ratio >= VOLUME_THRESHOLD
    )

    # Detectar cruces de EMA.
    bullish_cross = (
        previous_ema_7 <= previous_ema_25
        and ema_7 > ema_25
    )

    bearish_cross = (
        previous_ema_7 >= previous_ema_25
        and ema_7 < ema_25
    )

    # Confirmaciones de tendencia.
    bullish_alignment = (
        price > ema_7 > ema_25
    )

    bearish_alignment = (
        price < ema_7 < ema_25
    )

    if direction == "LONG":
        cross_confirmed = bullish_cross
        alignment_confirmed = bullish_alignment

    else:
        cross_confirmed = bearish_cross
        alignment_confirmed = bearish_alignment

    trigger = (
        (cross_confirmed or alignment_confirmed)
        and volume_confirmed
    )

    # Diagnóstico de condiciones.
    diagnostics = {
        "ema_7": ema_7,
        "ema_25": ema_25,
        "price": price,
        "volume": volume,
        "average_volume": average_volume,
        "volume_ratio": volume_ratio,
        "volume_threshold": VOLUME_THRESHOLD,
        "volume_confirmed": volume_confirmed,
        "bullish_cross": bullish_cross,
        "bearish_cross": bearish_cross,
        "bullish_alignment": bullish_alignment,
        "bearish_alignment": bearish_alignment,
        "cross_confirmed": cross_confirmed,
        "alignment_confirmed": alignment_confirmed,
    }

    if trigger:
        if cross_confirmed:
            reason = (
                "Cruce de EMA confirmado con volumen."
            )
        else:
            reason = (
                "EMAs y precio alineados con volumen confirmado."
            )

        return {
            "trigger": True,
            "direction": direction,
            "reason": reason,
            **diagnostics,
        }

    # Explicar exactamente qué condición falló.
    missing_conditions = []

    if not cross_confirmed and not alignment_confirmed:
        missing_conditions.append(
            "No existe cruce ni alineación de EMA."
        )

    if not volume_confirmed:
        missing_conditions.append(
            f"Volumen insuficiente: {volume_ratio:.2f}x "
            f"(mínimo {VOLUME_THRESHOLD:.2f}x)."
        )

    reason = " ".join(missing_conditions)

    return {
        "trigger": False,
        "direction": direction,
        "reason": reason,
        **diagnostics,
    }
