from typing import Optional


def calculate_tp_sl(
    entry_price: float,
    direction: str,
    operating_capital: float,
    leverage: int = 10,
    take_profit_percent: float = 0.02,
    stop_loss_percent: float = 0.05,
) -> dict:
    """
    Calcula TP y SL basados en el CAPITAL OPERATIVO de la operación.

    Ejemplo:
        Capital operativo = 12.50 USDT
        Leverage = 10x
        TP = 2% del capital operativo = +0.25 USDT
        SL = 5% del capital operativo = -0.625 USDT

    El movimiento de precio necesario se obtiene a partir del nominal:
        nominal = operating_capital * leverage
    """

    if direction not in ("LONG", "SHORT"):
        return {
            "valid": False,
            "reason": "Dirección inválida.",
        }

    if entry_price <= 0:
        return {
            "valid": False,
            "reason": "El precio de entrada debe ser mayor que cero.",
        }

    if operating_capital <= 0:
        return {
            "valid": False,
            "reason": "El capital operativo debe ser mayor que cero.",
        }

    if leverage <= 0:
        return {
            "valid": False,
            "reason": "El apalancamiento debe ser mayor que cero.",
        }

    if take_profit_percent <= 0:
        return {
            "valid": False,
            "reason": "El porcentaje de Take Profit debe ser mayor que cero.",
        }

    if stop_loss_percent <= 0:
        return {
            "valid": False,
            "reason": "El porcentaje de Stop Loss debe ser mayor que cero.",
        }

    operating_capital = float(operating_capital)
    leverage = int(leverage)

    nominal = operating_capital * leverage

    # Objetivos monetarios sobre el capital operativo
    take_profit_pnl = operating_capital * take_profit_percent
    stop_loss_pnl = operating_capital * stop_loss_percent

    # Movimiento de precio necesario para conseguir ese PnL
    take_profit_price_percent = take_profit_pnl / nominal
    stop_loss_price_percent = stop_loss_pnl / nominal

    if direction == "LONG":
        take_profit = entry_price * (
            1 + take_profit_price_percent
        )

        stop_loss = entry_price * (
            1 - stop_loss_price_percent
        )

    else:  # SHORT
        take_profit = entry_price * (
            1 - take_profit_price_percent
        )

        stop_loss = entry_price * (
            1 + stop_loss_price_percent
        )

    return {
        "valid": True,

        "entry_price": float(entry_price),

        "take_profit": float(take_profit),
        "stop_loss": float(stop_loss),

        # Porcentajes sobre el capital operativo
        "take_profit_percent": float(take_profit_percent),
        "stop_loss_percent": float(stop_loss_percent),

        # PnL objetivo en USDT
        "take_profit_pnl": float(take_profit_pnl),
        "stop_loss_pnl": float(stop_loss_pnl),

        # Movimiento real del precio
        "take_profit_price_percent": float(
            take_profit_price_percent
        ),
        "stop_loss_price_percent": float(
            stop_loss_price_percent
        ),

        "operating_capital": float(operating_capital),
        "nominal": float(nominal),
        "leverage": leverage,
    }


def _extract_grid_information(grid_plan: dict) -> dict:

    range_low = grid_plan.get("range_low")

    if range_low is None:
        range_low = grid_plan.get("range_min")

    range_high = grid_plan.get("range_high")

    if range_high is None:
        range_high = grid_plan.get("range_max")

    range_size = grid_plan.get("range_size")

    if (
        range_size is None
        and range_low is not None
        and range_high is not None
    ):
        range_size = range_high - range_low

    spacing = grid_plan.get("spacing", 0.0)

    grid_points = grid_plan.get("grid")

    if not isinstance(grid_points, list):
        grid_points = grid_plan.get("grid_points")

    if not isinstance(grid_points, list):
        grid_points = []

    levels = grid_plan.get("levels")

    if levels is None:
        levels = grid_plan.get("grid_count")

    if levels is None and len(grid_points) > 0:
        levels = len(grid_points)

    if levels is None:
        grid_levels_value = grid_plan.get("grid_levels")

        if isinstance(grid_levels_value, int):
            levels = grid_levels_value

    if levels is None:
        levels = 0

    try:
        levels = int(levels)
    except (TypeError, ValueError):
        levels = 0

    return {
        "range_low": range_low,
        "range_high": range_high,
        "range_size": range_size,
        "levels": levels,
        "grid_points": grid_points,
        "spacing": spacing,
    }


def build_operation_plan(
    symbol: str,
    direction: str,
    current_price: float,
    grid_plan: dict,
    operating_capital: float,
    leverage: int = 10,
) -> dict:

    if direction not in ("LONG", "SHORT"):
        return {
            "valid": False,
            "symbol": symbol,
            "direction": direction,
            "reason": (
                "No existe una dirección válida para operar."
            ),
        }

    if not isinstance(grid_plan, dict):
        return {
            "valid": False,
            "symbol": symbol,
            "direction": direction,
            "reason": "El plan de grid no es válido.",
        }

    if not grid_plan.get("valid", False):
        return {
            "valid": False,
            "symbol": symbol,
            "direction": direction,
            "reason": "El plan de grid no es válido.",
        }

    if current_price <= 0:
        return {
            "valid": False,
            "symbol": symbol,
            "direction": direction,
            "reason": (
                "El precio de entrada debe ser mayor que cero."
            ),
        }

    if operating_capital <= 0:
        return {
            "valid": False,
            "symbol": symbol,
            "direction": direction,
            "reason": (
                "El capital operativo debe ser mayor que cero."
            ),
        }

    if leverage <= 0:
        return {
            "valid": False,
            "symbol": symbol,
            "direction": direction,
            "reason": (
                "El apalancamiento debe ser mayor que cero."
            ),
        }

    entry_price = float(current_price)
    operating_capital = float(operating_capital)
    leverage = int(leverage)

    tp_sl = calculate_tp_sl(
        entry_price=entry_price,
        direction=direction,
        operating_capital=operating_capital,
        leverage=leverage,
        take_profit_percent=0.02,
        stop_loss_percent=0.05,
    )

    if not tp_sl.get("valid", False):
        return {
            "valid": False,
            "symbol": symbol,
            "direction": direction,
            "reason": "No se pudo calcular TP/SL.",
        }

    nominal = operating_capital * leverage

    grid_info = _extract_grid_information(grid_plan)

    range_low = grid_info["range_low"]
    range_high = grid_info["range_high"]
    range_size = grid_info["range_size"]
    levels = grid_info["levels"]
    grid_points = grid_info["grid_points"]
    spacing = grid_info["spacing"]

    return {
        "valid": True,

        "symbol": symbol,
        "direction": direction,

        "current_price": entry_price,
        "entry_price": entry_price,
        "entry": entry_price,

        # Precios de salida
        "take_profit": tp_sl["take_profit"],
        "stop_loss": tp_sl["stop_loss"],

        # Objetivos porcentuales sobre capital operativo
        "take_profit_percent": tp_sl[
            "take_profit_percent"
        ],
        "stop_loss_percent": tp_sl[
            "stop_loss_percent"
        ],

        # PnL monetario esperado
        "take_profit_pnl": tp_sl[
            "take_profit_pnl"
        ],
        "stop_loss_pnl": tp_sl[
            "stop_loss_pnl"
        ],

        # Movimiento de precio necesario
        "take_profit_price_percent": tp_sl[
            "take_profit_price_percent"
        ],
        "stop_loss_price_percent": tp_sl[
            "stop_loss_price_percent"
        ],

        # Capital
        "operating_capital": operating_capital,
        "capital": operating_capital,

        # Apalancamiento y nominal
        "leverage": leverage,
        "nominal": nominal,
        "notional": nominal,

        # Grid
        "range_low": range_low,
        "range_high": range_high,
        "range_size": range_size,

        "grid_range_min": range_low,
        "grid_range_max": range_high,

        "grid_range_low": range_low,
        "grid_range_high": range_high,

        "levels": levels,
        "grid_levels": levels,
        "grid_count": levels,

        "grid": grid_points,
        "grid_points": grid_points,

        "spacing": spacing,

        "grid_plan": grid_plan,

        "reason": (
            "Plan de operación construido correctamente. "
            "No se ejecutó ninguna orden."
        ),
    }