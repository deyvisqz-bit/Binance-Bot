from src.grid_engine import generate_grid_levels


tests = [
    {
        "symbol": "BTCUSDT",
        "low": 83750.0,
        "high": 84106.8,
        "levels": 8,
    },
    {
        "symbol": "ETHUSDT",
        "low": 2679.71,
        "high": 2695.17,
        "levels": 8,
    },
    {
        "symbol": "SOLUSDT",
        "low": 120.48,
        "high": 122.42,
        "levels": 8,
    },
    {
        "symbol": "XRPUSDT",
        "low": 1.5542,
        "high": 1.5804,
        "levels": 8,
    },
]


print("=" * 70)
print("PRUEBA DEL GRID ARITMÉTICO")
print("=" * 70)


for test in tests:

    print()
    print("-" * 70)
    print(f"PAR: {test['symbol']}")
    print("-" * 70)

    result = generate_grid_levels(
        range_low=test["low"],
        range_high=test["high"],
        levels=test["levels"],
    )

    if not result["valid"]:
        print("GRID NO VÁLIDO")
        print(result["reason"])
        continue

    print(f"MÍNIMO: {result['range_low']}")
    print(f"MÁXIMO: {result['range_high']}")
    print(f"NIVELES: {result['levels']}")
    print(f"SEPARACIÓN: {result['spacing']}")

    print()
    print("NIVELES DEL GRID:")

    for number, price in enumerate(
        result["grid_levels"],
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