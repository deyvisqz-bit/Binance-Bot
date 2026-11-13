from src.binance_client import (
    create_public_client,
    get_futures_klines,
)

from src.range_calculator import (
    calculate_dynamic_range,
)


client = create_public_client()

symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
]

print("=" * 70)
print("PRUEBA DE RANGO DINÁMICO PARA GRID")
print("=" * 70)

for symbol in symbols:

    print()
    print("-" * 70)
    print(f"PAR: {symbol}")
    print("-" * 70)

    try:

        df = get_futures_klines(
            client,
            symbol,
            "15m",
            100,
        )

        result = calculate_dynamic_range(
            df,
            lookback=20,
        )

        if not result["valid"]:
            print("RANGO NO VÁLIDO")
            print(result["reason"])
            continue

        print(
            f"PRECIO ACTUAL: "
            f"{result['current_price']:.8f}"
        )

        print(
            f"MÍNIMO DEL RANGO: "
            f"{result['range_low']:.8f}"
        )

        print(
            f"MÁXIMO DEL RANGO: "
            f"{result['range_high']:.8f}"
        )

        print(
            f"AMPLITUD: "
            f"{result['range_percent']:.2f}%"
        )

        if result["position_in_range"] is not None:

            print(
                f"POSICIÓN EN EL RANGO: "
                f"{result['position_in_range']:.2f}%"
            )

        print(
            f"VELAS ANALIZADAS: "
            f"{result['lookback']}"
        )

    except Exception as error:

        print()
        print("ERROR:")
        print(error)


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)