from typing import Dict, List


def analyze_grid_position(
    current_price: float,
    grid_levels: List[float],
    direction: str,
) -> Dict:
    """
    Analiza la posición del precio actual dentro del Grid.

    LONG:
        Busca el nivel inmediatamente inferior o igual
        al precio actual.

    SHORT:
        Busca el nivel inmediatamente superior o igual
        al precio actual.

    No ejecuta órdenes.
    """

    direction = direction.upper()

    if current_price <= 0:
        return {
            "valid": False,
            "reason": "El precio actual debe ser mayor que 0.",
        }

    if not grid_levels:
        return {
            "valid": False,
            "reason": "No existen niveles de Grid.",
        }

    if direction not in ("LONG", "SHORT"):
        return {
            "valid": False,
            "reason": "La dirección debe ser LONG o SHORT.",
        }

    levels = sorted(grid_levels)

    range_low = levels[0]
    range_high = levels[-1]

    # Por debajo del rango
    if current_price < range_low:

        return {
            "valid": False,
            "reason": "El precio está por debajo del rango del Grid.",
            "current_price": current_price,
            "range_low": range_low,
            "range_high": range_high,
            "position_percent": 0.0,
        }

    # Por encima del rango
    if current_price > range_high:

        return {
            "valid": False,
            "reason": "El precio está por encima del rango del Grid.",
            "current_price": current_price,
            "range_low": range_low,
            "range_high": range_high,
            "position_percent": 100.0,
        }

    # Posición porcentual dentro del rango
    range_size = range_high - range_low

    if range_size == 0:

        return {
            "valid": False,
            "reason": "El rango del Grid no puede tener tamaño cero.",
        }

    position_percent = (
        (current_price - range_low)
        / range_size
    ) * 100

    lower_levels = [
        level
        for level in levels
        if level <= current_price
    ]

    upper_levels = [
        level
        for level in levels
        if level >= current_price
    ]

    nearest_lower = (
        max(lower_levels)
        if lower_levels
        else None
    )

    nearest_upper = (
        min(upper_levels)
        if upper_levels
        else None
    )

    # LONG
    if direction == "LONG":

        reference_level = nearest_lower

        if reference_level is None:

            return {
                "valid": False,
                "reason": "No existe nivel inferior para LONG.",
            }

        distance_percent = (
            (current_price - reference_level)
            / reference_level
        ) * 100

        return {
            "valid": True,
            "direction": "LONG",
            "current_price": current_price,
            "range_low": range_low,
            "range_high": range_high,
            "position_percent": position_percent,
            "reference_level": reference_level,
            "nearest_lower": nearest_lower,
            "nearest_upper": nearest_upper,
            "distance_percent": distance_percent,
            "reason": "Nivel de referencia LONG encontrado.",
        }

    # SHORT
    reference_level = nearest_upper

    if reference_level is None:

        return {
            "valid": False,
            "reason": "No existe nivel superior para SHORT.",
        }

    distance_percent = (
        (reference_level - current_price)
        / current_price
    ) * 100

    return {
        "valid": True,
        "direction": "SHORT",
        "current_price": current_price,
        "range_low": range_low,
        "range_high": range_high,
        "position_percent": position_percent,
        "reference_level": reference_level,
        "nearest_lower": nearest_lower,
        "nearest_upper": nearest_upper,
        "distance_percent": distance_percent,
        "reason": "Nivel de referencia SHORT encontrado.",
    }