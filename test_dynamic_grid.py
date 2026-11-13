from src.binance_client import (
    create_public_client,
    get_futures_klines,
)

from src.range_calculator import (
    calculate_dynamic_range,
)

from src.grid_engine import (
    build_dynamic_grid,
)


SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
]

GRID_LEVELS = 8


client = create_public_client()


print("=" * 80)
print("GRID DINÁMICO")
print("=" * 80)


for symbol in SYMBOLS:

    print()
    print("-" * 80)
    print(f"PAR: {symbol}")
    print("-" * 80)

    try:

        df = get_futures_klines(
            client,
            symbol,
            "15m",
            100,
        )

        range_result = calculate_dynamic_range(
            df
        )

        if not range_result["valid"]:

            print("RANGO NO VÁLIDO")
            print(range_result["reason"])
            continue

        range_low = range_result["range_low"]
        range_high = range_result["range_high"]

        print(
            f"RANGO: "
            f"{range_low} → {range_high}"
        )

        grid_result = build_dynamic_grid(
    df,
    lookback=50,

        )

        if not grid_result["valid"]:

            print("GRID NO VÁLIDO")
            print(grid_result["reason"])
            continue

        print(
            f"NIVELES: "
            f"{grid_result['levels']}"
        )

        print(
            f"SEPARACIÓN: "
            f"{grid_result['spacing']}"
        )

        print()
        print("NIVELES:")

        for number, price in enumerate(
            grid_result["grid"],
            start=1,
        ):

            print(
                f"Nivel {number:02d}: "
                f"{price:.8f}"
            )

    except Exception as error:

        print()
        print("ERROR:")
        print(error)


print()
print("=" * 80)
print("FIN DEL GRID DINÁMICO")
print("=" * 80)