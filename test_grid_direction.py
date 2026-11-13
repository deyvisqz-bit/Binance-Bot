from src.grid_engine import (
    determine_grid_side,
    build_grid_plan,
)


print("=" * 70)
print("PRUEBA DE DIRECCIÓN DEL GRID")
print("=" * 70)


TESTS = [
    "LONG",
    "SHORT",
    "WAIT",
]


for direction in TESTS:

    print()
    print("-" * 70)
    print(f"DIRECCIÓN: {direction}")
    print("-" * 70)

    result = determine_grid_side(direction)

    print(f"VÁLIDO: {result['valid']}")
    print(f"LADO: {result['side']}")
    print(f"MOTIVO: {result['reason']}")


print()
print("=" * 70)
print("PRUEBA DE PLAN GRID LONG")
print("=" * 70)


long_plan = build_grid_plan(
    direction="LONG",
    range_low=1.5542,
    range_high=1.5804,
    levels=8,
)


print(f"VÁLIDO: {long_plan['valid']}")
print(f"DIRECCIÓN: {long_plan['direction']}")
print(f"RANGO: {long_plan['range_low']} → {long_plan['range_high']}")
print(f"NIVELES: {long_plan['levels']}")
print(f"SEPARACIÓN: {long_plan['spacing']}")
print(f"MOTIVO: {long_plan['reason']}")

print()

for number, price in enumerate(
    long_plan["grid_levels"],
    start=1,
):
    print(
        f"Nivel {number:02d}: "
        f"{price:.8f}"
    )


print()
print("=" * 70)
print("PRUEBA DE PLAN GRID SHORT")
print("=" * 70)


short_plan = build_grid_plan(
    direction="SHORT",
    range_low=1.5542,
    range_high=1.5804,
    levels=8,
)


print(f"VÁLIDO: {short_plan['valid']}")
print(f"DIRECCIÓN: {short_plan['direction']}")
print(f"RANGO: {short_plan['range_low']} → {short_plan['range_high']}")
print(f"NIVELES: {short_plan['levels']}")
print(f"SEPARACIÓN: {short_plan['spacing']}")
print(f"MOTIVO: {short_plan['reason']}")

print()

for number, price in enumerate(
    short_plan["grid_levels"],
    start=1,
):
    print(
        f"Nivel {number:02d}: "
        f"{price:.8f}"
    )


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)