from src.binance_client import create_public_client, get_futures_klines
from src.entry_trigger import detect_entry_trigger


client = create_public_client()

symbol = "XRPUSDT"

df = get_futures_klines(
    client,
    symbol,
    "1m",
    100
)

print("=" * 60)
print(f"TRIGGER DE ENTRADA 1M: {symbol}")
print("=" * 60)

for direction in ["LONG", "SHORT"]:

    result = detect_entry_trigger(
        df,
        direction
    )

    print()
    print(f"DIRECCIÓN: {direction}")
    print(f"TRIGGER: {result['trigger']}")
    print(f"PRECIO: {result['price']:.6f}")
    print(f"VOLUMEN: {result['volume_ratio']:.2f}x")
    print(f"MOTIVO: {result['reason']}")

print("=" * 60)