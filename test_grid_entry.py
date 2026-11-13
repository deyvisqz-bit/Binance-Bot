from src.grid_engine import build_grid_plan
from src.grid_entry import analyze_grid_position


RANGE_LOW = 1.5542
RANGE_HIGH = 1.5804
LEVELS = 8


print("=" * 70)
print("PRUEBA DE ENTRADA EN GRID")
print("=" * 70)


# ============================================================
# CREAR GRID
# ============================================================

grid = build_grid_plan(
    direction="LONG",
    range_low=RANGE_LOW,
    range_high=RANGE_HIGH,
    levels=LEVELS,
)


if not grid["valid"]:

    print("ERROR AL CREAR GRID")
    print(grid["reason"])

else:

    grid_levels = grid["grid_levels"]

    print()
    print("GRID GENERADO")
    print(f"RANGO: {RANGE_LOW} → {RANGE_HIGH}")
    print(f"NIVELES: {LEVELS}")
    print()


    # ========================================================
    # PRUEBA LONG
    # ========================================================

    print("=" * 70)
    print("PRUEBA LONG")
    print("=" * 70)

    current_price = 1.5750

    result = analyze_grid_position(
        current_price=current_price,
        grid_levels=grid_levels,
        direction="LONG",
    )

    print(f"PRECIO ACTUAL: {current_price}")
    print(f"VÁLIDO: {result['valid']}")

    if result["valid"]:

        print(
            f"POSICIÓN EN RANGO: "
            f"{result['position_percent']:.2f}%"
        )

        print(
            f"NIVEL INFERIOR: "
            f"{result['nearest_lower']:.8f}"
        )

        print(
            f"NIVEL SUPERIOR: "
            f"{result['nearest_upper']:.8f}"
        )

        print(
            f"NIVEL REFERENCIA LONG: "
            f"{result['reference_level']:.8f}"
        )

        print(
            f"DISTANCIA: "
            f"{result['distance_percent']:.4f}%"
        )

        print(
            f"MOTIVO: "
            f"{result['reason']}"
        )


    # ========================================================
    # PRUEBA SHORT
    # ========================================================

    print()
    print("=" * 70)
    print("PRUEBA SHORT")
    print("=" * 70)

    current_price = 1.5750

    result = analyze_grid_position(
        current_price=current_price,
        grid_levels=grid_levels,
        direction="SHORT",
    )

    print(f"PRECIO ACTUAL: {current_price}")
    print(f"VÁLIDO: {result['valid']}")

    if result["valid"]:

        print(
            f"POSICIÓN EN RANGO: "
            f"{result['position_percent']:.2f}%"
        )

        print(
            f"NIVEL INFERIOR: "
            f"{result['nearest_lower']:.8f}"
        )

        print(
            f"NIVEL SUPERIOR: "
            f"{result['nearest_upper']:.8f}"
        )

        print(
            f"NIVEL REFERENCIA SHORT: "
            f"{result['reference_level']:.8f}"
        )

        print(
            f"DISTANCIA: "
            f"{result['distance_percent']:.4f}%"
        )

        print(
            f"MOTIVO: "
            f"{result['reason']}"
        )


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)