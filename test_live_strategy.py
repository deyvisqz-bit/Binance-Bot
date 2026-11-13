from src.binance_client import create_public_client, get_futures_klines
from src.trend_detector import analyze_15m
from src.strategy import evaluate_scalping_setup


SYMBOL = "BTCUSDT"


client = create_public_client()


def get_analysis(symbol, timeframe):
    df = get_futures_klines(
        client,
        symbol,
        timeframe,
        limit=200
    )

    return analyze_15m(df)


analysis_15m = get_analysis(SYMBOL, "15m")
analysis_5m = get_analysis(SYMBOL, "5m")
analysis_1m = get_analysis(SYMBOL, "1m")


result = evaluate_scalping_setup(
    analysis_15m,
    analysis_5m,
    analysis_1m
)


print("=" * 60)
print(f"ANÁLISIS REAL DE SCALPING: {SYMBOL}")
print("=" * 60)

print(f"15M: {analysis_15m['direction']}")
print(f"5M:  {analysis_5m['direction']}")
print(f"1M:  {analysis_1m['direction']}")

print("-" * 60)

print(f"Score LONG:  {result['long_score']}/100")
print(f"Score SHORT: {result['short_score']}/100")
print(f"DECISIÓN:    {result['direction']}")
print(f"MOTIVO:      {result['reason']}")

print("=" * 60)