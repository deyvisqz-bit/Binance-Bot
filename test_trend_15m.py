from src.binance_client import create_public_client, get_futures_klines
from src.trend_detector import analyze_15m


client = create_public_client()

symbol = symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",
    "XRPUSDT",
]
for symbol in symbols:

    df = get_futures_klines(
        client,
        symbol,
        "15m",
        250
    )

    result = analyze_15m(df)

    print("\n==============================")
    print(f"ANÁLISIS 15M - {symbol}")
    print("==============================")

    print(f"Precio: {result['price']}")
    print(f"EMA 20: {result['ema_20']}")
    print(f"EMA 50: {result['ema_50']}")
    print(f"Estructura: {result['structure']}")
    print(f"Volumen relativo: {result['volume_ratio']:.2f}x")
    print(f"ATR %: {result['atr_percent']:.2f}%")

    print("------------------------------")
    print(f"Score LONG: {result['long_score']}/100")
    print(f"Score SHORT: {result['short_score']}/100")
    print(f"DECISIÓN: {result['direction']}")