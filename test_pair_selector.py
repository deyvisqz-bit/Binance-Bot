from src.binance_client import create_public_client
from src.pair_selector import select_pairs


client = create_public_client()


print("=" * 70)
print("SELECTOR DE PARES PARA SCALPING")
print("=" * 70)

pairs = select_pairs(
    client,
    max_pairs=10,
    liquidity_candidates=30,
)

print()

if not pairs:
    print("NO SE ENCONTRARON CANDIDATOS")
else:

    print(f"CANDIDATOS ENCONTRADOS: {len(pairs)}")
    print()

    for pair in pairs:

        print("-" * 70)

        print(f"PAR: {pair['symbol']}")
        print(f"DIRECCIÓN 15M: {pair['direction_15m']}")
        print(f"ESTRUCTURA 15M: {pair['structure_15m']}")
        print(f"VOLUMEN 15M: {pair['volume_status_15m']}")
        print(
            f"VOLUMEN 15M: "
            f"{pair['volume_ratio_15m']:.2f}x"
        )
        print(
            f"ATR 15M: "
            f"{pair['atr_percent_15m']:.2f}%"
        )
        print(
            f"VOLUMEN 24H: "
            f"{pair['quote_volume_24h']:,.0f} USDT"
        )

print()
print("=" * 70)
print("FIN DEL SELECTOR")
print("=" * 70)