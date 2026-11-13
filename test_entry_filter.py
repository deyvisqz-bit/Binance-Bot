from src.entry_filter import evaluate_entry_filter


print("=" * 60)
print("TEST DEL FILTRO DE ENTRADA")
print("=" * 60)


casos = [
    {
        "nombre": "LONG VÁLIDO",
        "direction": "LONG",
        "trigger": True,
        "trigger_direction": "LONG",
        "position_percent": 55,
    },
    {
        "nombre": "LONG DEMASIADO ALTO",
        "direction": "LONG",
        "trigger": True,
        "trigger_direction": "LONG",
        "position_percent": 85,
    },
    {
        "nombre": "SHORT VÁLIDO",
        "direction": "SHORT",
        "trigger": True,
        "trigger_direction": "SHORT",
        "position_percent": 55,
    },
    {
        "nombre": "SHORT DEMASIADO BAJO",
        "direction": "SHORT",
        "trigger": True,
        "trigger_direction": "SHORT",
        "position_percent": 15,
    },
    {
        "nombre": "SIN TRIGGER",
        "direction": "LONG",
        "trigger": False,
        "trigger_direction": "LONG",
        "position_percent": 50,
    },
    {
        "nombre": "TRIGGER CONTRARIO",
        "direction": "LONG",
        "trigger": True,
        "trigger_direction": "SHORT",
        "position_percent": 50,
    },
]


for caso in casos:

    result = evaluate_entry_filter(
        direction=caso["direction"],
        trigger=caso["trigger"],
        trigger_direction=caso["trigger_direction"],
        position_percent=caso["position_percent"],
    )

    print()
    print(f"CASO: {caso['nombre']}")
    print(f"DIRECCIÓN: {caso['direction']}")
    print(f"TRIGGER: {caso['trigger']}")
    print(f"POSICIÓN: {caso['position_percent']:.2f}%")
    print(f"DECISIÓN: {result['decision']}")
    print(f"MOTIVO: {result['reason']}")


print()
print("=" * 60)
print("FIN DEL TEST")
print("=" * 60)