from src.binance_client import create_public_client, get_futures_klines
from src.trend_detector import analyze_1m


client = create_public_client()

symbol = "BTCUSDT"

df = get_futures_klines(
    client,
    symbol,
    "1m",
    200
)

result = analyze_1m(df)

print("=" * 40)
print(f"ANÁLISIS 1M - {symbol}")
print("=" * 40)

print(f"Dirección: {result['direction']}")
print(f"Estructura: {result['structure']}")
print(f"Precio: {result['price']}")
print(f"EMA 20: {result['ema_20']}")
print(f"EMA 50: {result['ema_50']}")
print(f"Volumen relativo: {result['volume_ratio']:.2f}x")
print(f"ATR %: {result['atr_percent']:.2f}%")

print("-" * 40)
print(f"Score LONG: {result['long_score']}/100")
print(f"Score SHORT: {result['short_score']}/100")
print(f"DECISIÓN: {result['direction']}")
print("-" * 40)