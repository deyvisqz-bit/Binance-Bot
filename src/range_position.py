
import math


def calculate_range_position(
    price: float,
    range_min: float,
    range_max: float,
) -> dict:
    """
    Calcula la posición del precio dentro del rango.

    0%   = mínimo del rango
    50%  = mitad del rango
    100% = máximo del rango
    """

    try:
        price = float(price)
        range_min = float(range_min)
        range_max = float(range_max)
    except (TypeError, ValueError):
        raise ValueError("Los valores del rango deben ser numéricos.")

    if not all(math.isfinite(v) for v in (price, range_min, range_max)):
        raise ValueError("Los valores del rango deben ser finitos.")

    if price <= 0:
        raise ValueError("El precio debe ser mayor que cero.")

    if range_min <= 0:
        raise ValueError("El mínimo del rango debe ser mayor que cero.")

    if range_max <= range_min:
        raise ValueError("El máximo debe ser mayor que el mínimo.")

    position_percent = (
        (price - range_min)
        / (range_max - range_min)
    ) * 100

    position_percent = max(0.0, min(100.0, position_percent))

    if position_percent <= 30:
        zone = "BAJA"
    elif position_percent <= 70:
        zone = "MEDIA"
    else:
        zone = "ALTA"

    return {
        "position_percent": position_percent,
        "zone": zone,
        "distance_to_min": price - range_min,
        "distance_to_max": range_max - price,
    }
