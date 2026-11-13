import pandas as pd


def calculate_dynamic_range(
    df: pd.DataFrame,
    lookback: int = 20,
) -> dict:
    """
    Calcula un rango dinámico utilizando
    el máximo y mínimo de las velas recientes.

    No ejecuta órdenes.
    No abre posiciones.
    Solo calcula el rango candidato para el Grid.
    """

    if len(df) < lookback:
        return {
            "valid": False,
            "reason": "Datos insuficientes",
        }

    recent = df.tail(lookback)

    range_high = recent["high"].max()
    range_low = recent["low"].min()

    current_price = df.iloc[-1]["close"]

    range_size = range_high - range_low

    if range_low > 0:
        range_percent = (
            range_size / range_low
        ) * 100
    else:
        range_percent = 0.0

    if range_size > 0 and range_low <= current_price <= range_high:
        position_in_range = (
            (current_price - range_low)
            / range_size
        ) * 100
    else:
        position_in_range = None

    return {
        "valid": True,
        "range_low": range_low,
        "range_high": range_high,
        "current_price": current_price,
        "range_size": range_size,
        "range_percent": range_percent,
        "position_in_range": position_in_range,
        "lookback": lookback,
    }