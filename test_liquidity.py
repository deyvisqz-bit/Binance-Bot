from src.binance_client import create_public_client


client = create_public_client()

symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
]


tickers = client.futures_ticker()

market_data = {}

for ticker in tickers:
    symbol = ticker["symbol"]

    if symbol in symbols:
        market_data[symbol] = {
            "quote_volume": float(ticker["quoteVolume"]),
            "price_change": float(ticker["priceChangePercent"]),
        }


print("\n==============================")
print("ANÁLISIS DE LIQUIDEZ 24H")
print("==============================")

for symbol in symbols:

    data = market_data.get(symbol)

    if data is None:
        print(f"{symbol}: SIN DATOS")
        continue

    print(f"\n{symbol}")
    print(f"Volumen 24H: {data['quote_volume']:,.0f} USDT")
    print(f"Cambio 24H: {data['price_change']:.2f}%")