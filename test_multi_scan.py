from src.binance_client import create_public_client, get_futures_klines
from src.trend_detector import (
    analyze_15m,
    analyze_5m,
    analyze_1m,
)
from src.entry_trigger import detect_entry_trigger
from src.strategy import evaluate_scalping_setup


SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
]


client = create_public_client()


print("=" * 70)
print("ESCANEO MULTI-PAR DE SCALPING")
print("=" * 70)


for symbol in SYMBOLS:

    try:

        df_15m = get_futures_klines(
            client,
            symbol,
            "15m",
            200
        )

        df_5m = get_futures_klines(
            client,
            symbol,
            "5m",
            200
        )

        df_1m = get_futures_klines(
            client,
            symbol,
            "1m",
            200
        )


        analysis_15m = analyze_15m(df_15m)
        analysis_5m = analyze_5m(df_5m)
        analysis_1m = analyze_1m(df_1m)


        entry_trigger = detect_entry_trigger(
            df_1m,
            analysis_1m["direction"]
        )


        result = evaluate_scalping_setup(
            analysis_15m,
            analysis_5m,
            analysis_1m,
            entry_trigger
        )


        print()
        print("=" * 70)
        print(symbol)
        print("=" * 70)

        print(
            f"15M: {analysis_15m['direction']} "
            f"| {analysis_15m['volume_status']}"
        )

        print(
            f"5M:  {analysis_5m['direction']} "
            f"| {analysis_5m['volume_status']}"
        )

        print(
            f"1M:  {analysis_1m['direction']} "
            f"| {analysis_1m['volume_status']}"
        )

        print(
            f"TRIGGER: {entry_trigger['trigger']} "
            f"| {entry_trigger['direction']}"
        )

        print(
            f"DECISIÓN: {result['direction']}"
        )

        print(
            f"MOTIVO: {result['reason']}"
        )


    except Exception as error:

        print()
        print(f"{symbol} → ERROR")
        print(error)


print()
print("=" * 70)
print("FIN DEL ESCANEO")
print("=" * 70)