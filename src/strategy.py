def evaluate_scalping_setup(
    analysis_15m: dict,
    analysis_5m: dict,
    analysis_1m: dict,
    entry_trigger: dict,
) -> dict:
    """
    Evalúa una oportunidad de scalping para un bot sin supervisión.

    Reglas:
    - 15M debe tener una dirección clara.
    - 5M debe estar alineado con 15M.
    - 1M debe confirmar la entrada mediante un trigger real.
    - Si cualquiera de estas condiciones falla, WAIT.
    """

    direction_15m = analysis_15m["direction"]
    direction_5m = analysis_5m["direction"]
    direction_1m = analysis_1m["direction"]

    trigger = entry_trigger["trigger"]
    trigger_direction = entry_trigger["direction"]

    long_score = 0
    short_score = 0

    direction = "WAIT"
    reason = "Sin condiciones suficientes para entrada"

    # ============================================================
    # LONG
    # ============================================================

    if (
        direction_15m == "LONG"
        and direction_5m == "LONG"
        and direction_1m == "LONG"
        and trigger is True
        and trigger_direction == "LONG"
    ):
        long_score = 100
        direction = "LONG"
        reason = "15M, 5M y 1M alineados + trigger LONG confirmado"

    # ============================================================
    # SHORT
    # ============================================================

    elif (
        direction_15m == "SHORT"
        and direction_5m == "SHORT"
        and direction_1m == "SHORT"
        and trigger is True
        and trigger_direction == "SHORT"
    ):
        short_score = 100
        direction = "SHORT"
        reason = "15M, 5M y 1M alineados + trigger SHORT confirmado"

    # ============================================================
    # WAIT
    # ============================================================

    else:
        if direction_15m == "NO_TRADE":
            reason = "15M sin dirección clara"

        elif direction_5m != direction_15m:
            reason = "5M no confirma la dirección de 15M"

        elif direction_1m != direction_15m:
            reason = "1M no confirma la dirección de 15M"

        elif not trigger:
            reason = "Sin trigger de entrada en 1M"

    return {
        "direction": direction,
        "long_score": long_score,
        "short_score": short_score,
        "direction_15m": direction_15m,
        "direction_5m": direction_5m,
        "direction_1m": direction_1m,
        "trigger": trigger,
        "trigger_direction": trigger_direction,
        "trigger_reason": entry_trigger.get("reason", ""),
        "reason": reason,
    }