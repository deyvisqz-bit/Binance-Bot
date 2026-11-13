from src.binance_client import create_public_client, get_futures_klines
from src.trend_detector import analyze_15m


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
        }


print("\n========================================")
print("ESCANEO DE MERCADO")
print("========================================")


for symbol in symbols:

    print(f"\n{symbol}")
    print("----------------------------------------")

    # -------------------------------
    # LIQUIDEZ
    # -------------------------------

    liquidity = market_data[symbol]["quote_volume"]

    print(f"Volumen 24H: {liquidity:,.0f} USDT")

    # -------------------------------
    # ANALISIS 15M
    # -------------------------------

    df = get_futures_klines(
        client,
        symbol,
        "15m",
        250
    )

    result = analyze_15m(df)

    print(f"Estructura: {result['structure']}")
    print(f"EMA 20: {result['ema_20']:.4f}")
    print(f"EMA 50: {result['ema_50']:.4f}")
    print(f"Volumen relativo: {result['volume_status']}x")
    print(f"ATR %: {result['atr_percent']:.2f}%")

    print("\nPuntuación:")
    print(f"LONG:  {result['long_score']}/100")
    print(f"SHORT: {result['short_score']}/100")

    print(f"DECISIÓN: {result['direction']}")