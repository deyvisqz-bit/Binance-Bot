from src.strategy import evaluate_scalping_setup


print("=" * 60)
print("TEST DE ESTRATEGIA DE SCALPING")
print("=" * 60)


# ============================================================
# CASO 1: LONG COMPLETO
# ============================================================

analysis_15m = {
    "direction": "LONG"
}

analysis_5m = {
    "direction": "LONG"
}

analysis_1m = {
    "direction": "LONG"
}

entry_trigger = {
    "trigger": True,
    "direction": "LONG",
    "reason": "Cruce alcista EMA 7/25 con volumen"
}

result = evaluate_scalping_setup(
    analysis_15m,
    analysis_5m,
    analysis_1m,
    entry_trigger
)

print()
print("CASO 1: LONG COMPLETO")
print(f"15M: {result['direction_15m']}")
print(f"5M: {result['direction_5m']}")
print(f"1M: {result['direction_1m']}")
print(f"TRIGGER: {result['trigger']}")
print(f"DIRECCIÓN TRIGGER: {result['trigger_direction']}")
print(f"DECISIÓN: {result['direction']}")
print(f"MOTIVO: {result['reason']}")


# ============================================================
# CASO 2: SHORT COMPLETO
# ============================================================

analysis_15m = {
    "direction": "SHORT"
}

analysis_5m = {
    "direction": "SHORT"
}

analysis_1m = {
    "direction": "SHORT"
}

entry_trigger = {
    "trigger": True,
    "direction": "SHORT",
    "reason": "Precio bajo EMA 7 y EMA 25 con volumen"
}

result = evaluate_scalping_setup(
    analysis_15m,
    analysis_5m,
    analysis_1m,
    entry_trigger
)

print()
print("CASO 2: SHORT COMPLETO")
print(f"15M: {result['direction_15m']}")
print(f"5M: {result['direction_5m']}")
print(f"1M: {result['direction_1m']}")
print(f"TRIGGER: {result['trigger']}")
print(f"DIRECCIÓN TRIGGER: {result['trigger_direction']}")
print(f"DECISIÓN: {result['direction']}")
print(f"MOTIVO: {result['reason']}")


# ============================================================
# CASO 3: DIRECCIONES EN CONFLICTO
# ============================================================

analysis_15m = {
    "direction": "LONG"
}

analysis_5m = {
    "direction": "SHORT"
}

analysis_1m = {
    "direction": "SHORT"
}

entry_trigger = {
    "trigger": True,
    "direction": "SHORT",
    "reason": "Precio bajo EMA 7 y EMA 25 con volumen"
}

result = evaluate_scalping_setup(
    analysis_15m,
    analysis_5m,
    analysis_1m,
    entry_trigger
)

print()
print("CASO 3: DIRECCIONES EN CONFLICTO")
print(f"15M: {result['direction_15m']}")
print(f"5M: {result['direction_5m']}")
print(f"1M: {result['direction_1m']}")
print(f"TRIGGER: {result['trigger']}")
print(f"DIRECCIÓN TRIGGER: {result['trigger_direction']}")
print(f"DECISIÓN: {result['direction']}")
print(f"MOTIVO: {result['reason']}")


# ============================================================
# CASO 4: TODO ALINEADO PERO SIN TRIGGER
# ============================================================

analysis_15m = {
    "direction": "LONG"
}

analysis_5m = {
    "direction": "LONG"
}

analysis_1m = {
    "direction": "LONG"
}

entry_trigger = {
    "trigger": False,
    "direction": "LONG",
    "reason": "No existe trigger de entrada"
}

result = evaluate_scalping_setup(
    analysis_15m,
    analysis_5m,
    analysis_1m,
    entry_trigger
)

print()
print("CASO 4: SIN TRIGGER")
print(f"15M: {result['direction_15m']}")
print(f"5M: {result['direction_5m']}")
print(f"1M: {result['direction_1m']}")
print(f"TRIGGER: {result['trigger']}")
print(f"DIRECCIÓN TRIGGER: {result['trigger_direction']}")
print(f"DECISIÓN: {result['direction']}")
print(f"MOTIVO: {result['reason']}")


print()
print("=" * 60)
print("FIN DEL TEST")
print("=" * 60)