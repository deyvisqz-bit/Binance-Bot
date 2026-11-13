
from typing import List, Dict, Optional


def calculate_unrealized_pnl(
    entry_price: float,
    current_price: float,
    direction: str,
    nominal: float,
) -> float:
    """Calcula el PnL bruto usando el nominal de la posición."""

    if entry_price <= 0:
        raise ValueError("El precio de entrada debe ser mayor que cero.")

    if current_price <= 0:
        raise ValueError("El precio actual debe ser mayor que cero.")

    if nominal <= 0:
        raise ValueError("El nominal debe ser mayor que cero.")

    if direction == "LONG":
        price_change_percent = (
            current_price - entry_price
        ) / entry_price

    elif direction == "SHORT":
        price_change_percent = (
            entry_price - current_price
        ) / entry_price

    else:
        raise ValueError("La dirección debe ser LONG o SHORT.")

    return nominal * price_change_percent


def _resolve_margin(
    nominal: float,
    leverage: float,
    margin: Optional[float] = None,
) -> float:
    """Obtiene el margen asignado a la operación."""

    if nominal <= 0:
        raise ValueError("El nominal debe ser mayor que cero.")

    if leverage <= 0:
        raise ValueError("El apalancamiento debe ser mayor que cero.")

    if margin is None:
        margin = nominal / leverage

    if margin <= 0:
        raise ValueError("El margen debe ser mayor que cero.")

    return float(margin)


def get_exit_prices(
    entry_price: float,
    direction: str,
    take_profit_percent: float = 0.02,
    stop_loss_percent: float = 0.05,
    nominal: Optional[float] = None,
    margin: Optional[float] = None,
    leverage: float = 10.0,
) -> Dict:
    """
    Calcula los precios de salida.

    Take Profit:
        Porcentaje de movimiento favorable del precio.

    Stop Loss:
        Porcentaje del margen asignado que se permite perder.

    Los porcentajes se expresan como decimales:
        0.02 = 2 %
        0.05 = 5 %
    """

    if entry_price <= 0:
        raise ValueError("El precio de entrada debe ser mayor que cero.")

    if direction not in ("LONG", "SHORT"):
        raise ValueError("La dirección debe ser LONG o SHORT.")

    if not 0 < take_profit_percent:
        raise ValueError("El Take Profit debe ser mayor que cero.")

    if not 0 < stop_loss_percent < 1:
        raise ValueError(
            "El Stop Loss debe estar entre 0 % y 100 % del margen."
        )

    if leverage <= 0:
        raise ValueError("El apalancamiento debe ser mayor que cero.")

    # Si no se especifican nominal y margen, se calcula el movimiento
    # del precio suponiendo que el margen es nominal / apalancamiento.
    if nominal is None and margin is None:
        stop_price_move_percent = stop_loss_percent / leverage

    elif nominal is not None:
        resolved_margin = _resolve_margin(
            nominal=nominal,
            leverage=leverage,
            margin=margin,
        )

        # Pérdida permitida / nominal = movimiento adverso del precio.
        allowed_loss = resolved_margin * stop_loss_percent
        stop_price_move_percent = allowed_loss / nominal

    else:
        raise ValueError(
            "Para calcular el Stop Loss, proporciona el nominal "
            "y el margen asignado."
        )

    if direction == "LONG":
        take_profit_price = entry_price * (
            1 + take_profit_percent
        )
        stop_loss_price = entry_price * (
            1 - stop_price_move_percent
        )

    else:  # SHORT
        take_profit_price = entry_price * (
            1 - take_profit_percent
        )
        stop_loss_price = entry_price * (
            1 + stop_price_move_percent
        )

    return {
        "take_profit_price": take_profit_price,
        "stop_loss_price": stop_loss_price,
        "take_profit_percent": take_profit_percent,
        "stop_loss_margin_percent": stop_loss_percent,
        "stop_price_move_percent": stop_price_move_percent,
        "leverage": leverage,
    }


def check_exit_condition(
    entry_price: float,
    current_price: float,
    direction: str,
    take_profit_percent: float = 0.02,
    stop_loss_percent: float = 0.05,
    nominal: Optional[float] = None,
    margin: Optional[float] = None,
    leverage: float = 10.0,
) -> Dict:
    """Comprueba si se alcanzó el Take Profit o el Stop Loss."""

    if current_price <= 0:
        raise ValueError("El precio actual debe ser mayor que cero.")

    prices = get_exit_prices(
        entry_price=entry_price,
        direction=direction,
        take_profit_percent=take_profit_percent,
        stop_loss_percent=stop_loss_percent,
        nominal=nominal,
        margin=margin,
        leverage=leverage,
    )

    take_profit_price = prices["take_profit_price"]
    stop_loss_price = prices["stop_loss_price"]

    if direction == "LONG":
        if current_price >= take_profit_price:
            reason = "TAKE_PROFIT"
            exit_price = take_profit_price

        elif current_price <= stop_loss_price:
            reason = "STOP_LOSS"
            exit_price = stop_loss_price

        else:
            reason = None
            exit_price = None

    else:  # SHORT
        if current_price <= take_profit_price:
            reason = "TAKE_PROFIT"
            exit_price = take_profit_price

        elif current_price >= stop_loss_price:
            reason = "STOP_LOSS"
            exit_price = stop_loss_price

        else:
            reason = None
            exit_price = None

    return {
        "closed": reason is not None,
        "reason": reason or "OPERACION_ACTIVA",
        "exit_price": exit_price,
        **prices,
    }


def simulate_trade(
    entry_price: float,
    direction: str,
    nominal: float,
    price_path: List[float],
    take_profit_percent: float = 0.02,
    stop_loss_percent: float = 0.05,
    margin: Optional[float] = None,
    leverage: float = 10.0,
) -> Dict:
    """
    Simula una operación sin enviar órdenes a Binance.

    El Stop Loss limita la pérdida bruta objetivo al porcentaje
    configurado del margen asignado.

    Si no se proporciona margin, se estima como nominal / leverage.
    """

    if entry_price <= 0:
        return {
            "valid": False,
            "reason": "Precio de entrada inválido.",
        }

    if nominal <= 0:
        return {
            "valid": False,
            "reason": "Nominal inválido.",
        }

    if direction not in ("LONG", "SHORT"):
        return {
            "valid": False,
            "reason": "Dirección inválida.",
        }

    if not isinstance(price_path, list) or not price_path:
        return {
            "valid": False,
            "reason": "El recorrido de precios está vacío.",
        }

    if leverage <= 0:
        return {
            "valid": False,
            "reason": "El apalancamiento debe ser mayor que cero.",
        }

    try:
        margin = _resolve_margin(
            nominal=nominal,
            leverage=leverage,
            margin=margin,
        )

        prices = get_exit_prices(
            entry_price=entry_price,
            direction=direction,
            take_profit_percent=take_profit_percent,
            stop_loss_percent=stop_loss_percent,
            nominal=nominal,
            margin=margin,
            leverage=leverage,
        )

    except ValueError as error:
        return {
            "valid": False,
            "reason": str(error),
        }

    allowed_loss = margin * stop_loss_percent
    current_price = entry_price
    candles_monitored = 0

    for price in price_path:
        try:
            current_price = float(price)

            if current_price <= 0:
                return {
                    "valid": False,
                    "reason": "El recorrido contiene un precio inválido.",
                }

            candles_monitored += 1

            exit_check = check_exit_condition(
                entry_price=entry_price,
                current_price=current_price,
                direction=direction,
                take_profit_percent=take_profit_percent,
                stop_loss_percent=stop_loss_percent,
                nominal=nominal,
                margin=margin,
                leverage=leverage,
            )

        except (TypeError, ValueError) as error:
            return {
                "valid": False,
                "reason": f"Error al procesar el precio: {error}",
            }

        if exit_check["closed"]:
            exit_price = exit_check["exit_price"]

            realized_pnl = calculate_unrealized_pnl(
                entry_price=entry_price,
                current_price=exit_price,
                direction=direction,
                nominal=nominal,
            )

            return {
                "valid": True,
                "closed": True,
                "direction": direction,
                "entry_price": entry_price,
                "current_price": current_price,
                "exit_price": exit_price,
                "exit_reason": exit_check["reason"],
                "take_profit_price": prices["take_profit_price"],
                "stop_loss_price": prices["stop_loss_price"],
                "nominal": nominal,
                "margin": margin,
                "leverage": leverage,
                "stop_loss_limit": allowed_loss,
                "pnl": realized_pnl,
                "candles_monitored": candles_monitored,
                "message": "Operación cerrada en la simulación.",
            }

    unrealized_pnl = calculate_unrealized_pnl(
        entry_price=entry_price,
        current_price=current_price,
        direction=direction,
        nominal=nominal,
    )

    return {
        "valid": True,
        "closed": False,
        "direction": direction,
        "entry_price": entry_price,
        "current_price": current_price,
        "exit_price": None,
        "exit_reason": None,
        "take_profit_price": prices["take_profit_price"],
        "stop_loss_price": prices["stop_loss_price"],
        "nominal": nominal,
        "margin": margin,
        "leverage": leverage,
        "stop_loss_limit": allowed_loss,
        "pnl": unrealized_pnl,
        "candles_monitored": candles_monitored,
        "message": "La operación continúa activa en la simulación.",
    }
