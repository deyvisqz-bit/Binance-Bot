from src.binance_client import create_public_client, get_futures_klines
from src.trend_detector import (
    analyze_15m,
    analyze_5m,
    analyze_1m,
)
from src.entry_trigger import detect_entry_trigger
from src.strategy import evaluate_scalping_setup


SYMBOL = "BTCUSDT"


client = create_public_client()


# ============================================================
# OBTENER DATOS REALES DE BINANCE
# ============================================================

df_15m = get_futures_klines(
    client,
    SYMBOL,
    "15m",
    200
)

df_5m = get_futures_klines(
    client,
    SYMBOL,
    "5m",
    200
)

df_1m = get_futures_klines(
    client,
    SYMBOL,
    "1m",
    200
)


# ============================================================
# ANALIZAR CADA TIMEFRAME
# ============================================================

analysis_15m = analyze_15m(df_15m)
analysis_5m = analyze_5m(df_5m)
analysis_1m = analyze_1m(df_1m)


# ============================================================
# TRIGGER DE ENTRADA
# ============================================================

entry_direction = analysis_1m["direction"]

entry_trigger = detect_entry_trigger(
    df_1m,
    entry_direction
)


# ============================================================
# EVALUAR CONFLUENCIA
# ============================================================

result = evaluate_scalping_setup(
    analysis_15m,
    analysis_5m,
    analysis_1m,
    entry_trigger
)


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

print("=" * 60)
print(f"ANÁLISIS EN TIEMPO REAL: {SYMBOL}")
print("=" * 60)

print()
print("15M")
print(f"Dirección: {analysis_15m['direction']}")
print(f"Estructura: {analysis_15m['structure']}")
print(f"Volumen: {analysis_15m['volume_status']}")
print(f"Score LONG: {analysis_15m['long_score']}")
print(f"Score SHORT: {analysis_15m['short_score']}")

print()
print("5M")
print(f"Dirección: {analysis_5m['direction']}")
print(f"Estructura: {analysis_5m['structure']}")
print(f"Volumen: {analysis_5m['volume_status']}")
print(f"Score LONG: {analysis_5m['long_score']}")
print(f"Score SHORT: {analysis_5m['short_score']}")

print()
print("1M")
print(f"Dirección: {analysis_1m['direction']}")
print(f"Estructura: {analysis_1m['structure']}")
print(f"Volumen: {analysis_1m['volume_status']}")
print(f"Score LONG: {analysis_1m['long_score']}")
print(f"Score SHORT: {analysis_1m['short_score']}")

print()
print("TRIGGER 1M")
print(f"Trigger: {entry_trigger['trigger']}")
print(f"Dirección: {entry_trigger['direction']}")
print(f"Volumen: {entry_trigger['volume_ratio']:.2f}x")
print(f"Motivo: {entry_trigger['reason']}")

print()
print("=" * 60)
print("DECISIÓN FINAL")
print("=" * 60)

print(f"DECISIÓN: {result['direction']}")
print(f"MOTIVO: {result['reason']}")

print("=" * 60)