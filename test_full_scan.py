from src.binance_client import create_public_client, get_futures_klines
from src.pair_selector import select_pairs
from src.trend_detector import (
    analyze_5m,
    analyze_1m,
)
from src.entry_trigger import detect_entry_trigger
from src.strategy import evaluate_scalping_setup


MAX_PAIRS = 10


client = create_public_client()


print("=" * 80)
print("ESCANEO COMPLETO DINÁMICO DE SCALPING")
print("=" * 80)

try:

    # ---------------------------------------------------------
    # 1. SELECCIONAR PARES DINÁMICAMENTE
    # ---------------------------------------------------------

    selected_pairs = select_pairs(
        client,
        max_pairs=MAX_PAIRS,
        liquidity_candidates=50,
    )

    print()
    print(f"PARES SELECCIONADOS: {len(selected_pairs)}")
    print()

    if not selected_pairs:
        print("NO SE ENCONTRARON PARES APTOS.")
        print("=" * 80)
        print("FIN DEL ESCANEO")
        print("=" * 80)
        raise SystemExit

    # ---------------------------------------------------------
    # 2. ANALIZAR CADA PAR
    # ---------------------------------------------------------

    for opportunity in selected_pairs:

        symbol = opportunity["symbol"]

        print()
        print("=" * 80)
        print(f"PAR: {symbol}")
        print("=" * 80)

        try:

            # -------------------------------------------------
            # 15M
            # -------------------------------------------------

            analysis_15m = {
                "direction": opportunity["direction_15m"],
                "structure": opportunity["structure_15m"],
                "volume_status": opportunity["volume_status_15m"],
                "volume_ratio": opportunity["volume_ratio_15m"],
                "atr_percent": opportunity["atr_percent_15m"],
            }

            # -------------------------------------------------
            # 5M
            # -------------------------------------------------

            df_5m = get_futures_klines(
                client,
                symbol,
                "5m",
                200,
            )

            analysis_5m = analyze_5m(df_5m)

            # -------------------------------------------------
            # 1M
            # -------------------------------------------------

            df_1m = get_futures_klines(
                client,
                symbol,
                "1m",
                200,
            )

            analysis_1m = analyze_1m(df_1m)

            # -------------------------------------------------
            # TRIGGER DE ENTRADA
            # -------------------------------------------------

            entry_trigger = detect_entry_trigger(
                df_1m,
                analysis_1m["direction"],
            )

            # -------------------------------------------------
            # DECISIÓN FINAL
            # -------------------------------------------------

            result = evaluate_scalping_setup(
                analysis_15m,
                analysis_5m,
                analysis_1m,
                entry_trigger,
            )

            # -------------------------------------------------
            # MOSTRAR RESULTADO
            # -------------------------------------------------

            print(
                f"15M: {analysis_15m['direction']} | "
                f"{analysis_15m['volume_status']} | "
                f"{analysis_15m['volume_ratio']:.2f}x"
            )

            print(
                f"5M:  {analysis_5m['direction']} | "
                f"{analysis_5m['volume_status']} | "
                f"{analysis_5m['volume_ratio']:.2f}x"
            )

            print(
                f"1M:  {analysis_1m['direction']} | "
                f"{analysis_1m['volume_status']} | "
                f"{analysis_1m['volume_ratio']:.2f}x"
            )

            print(
                f"TRIGGER: {entry_trigger['trigger']} | "
                f"{entry_trigger['direction']}"
            )

            print(
                f"TRIGGER MOTIVO: "
                f"{entry_trigger['reason']}"
            )

            print()

            print(
                f"DECISIÓN FINAL: "
                f"{result['direction']}"
            )

            print(
                f"MOTIVO: "
                f"{result['reason']}"
            )

        except Exception as error:

            print()
            print(f"{symbol} → ERROR")
            print(error)

    # ---------------------------------------------------------
    # FIN
    # ---------------------------------------------------------

    print()
    print("=" * 80)
    print("FIN DEL ESCANEO COMPLETO DINÁMICO")
    print("=" * 80)

except Exception as error:

    print()
    print("ERROR GENERAL DEL ESCANEO")
    print(error)