def evaluate_entry_filter(
    direction: str,
    trigger: bool,
    trigger_direction: str,
    position_percent: float,
) -> dict:
    """
    Filtro final antes de permitir una entrada.

    No ejecuta órdenes.
    Solo decide ENTRY o WAIT.
    """

    decision = "WAIT"
    reason = "No se cumplen las condiciones de entrada."

    if direction not in ("LONG", "SHORT"):
        return {
            "decision": decision,
            "reason": "Dirección inválida o WAIT.",
        }

    if not trigger:
        return {
            "decision": decision,
            "reason": "No existe trigger de entrada.",
        }

    if trigger_direction != direction:
        return {
            "decision": decision,
            "reason": "El trigger no coincide con la dirección.",
        }

    if direction == "LONG":

        if position_percent <= 70:
            decision = "ENTRY"
            reason = (
                "LONG confirmado y precio no está "
                "en zona excesivamente alta del rango."
            )
        else:
            reason = (
                "LONG rechazado: precio demasiado alto "
                "dentro del rango."
            )

    elif direction == "SHORT":

        if position_percent >= 30:
            decision = "ENTRY"
            reason = (
                "SHORT confirmado y precio no está "
                "en zona excesivamente baja del rango."
            )
        else:
            reason = (
                "SHORT rechazado: precio demasiado bajo "
                "dentro del rango."
            )

    return {
        "decision": decision,
        "reason": reason,
        "direction": direction,
        "position_percent": position_percent,
    }