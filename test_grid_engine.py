from src.binance_client import (
    create_public_client,
    get_futures_klines,
)

from src.grid_engine import (
    build_dynamic_grid,
)


print("=" * 60)
print("TEST DE GRID DINÁMICA")
print("=" * 60)


# ============================================================
# CONFIGURACIÓN
# ============================================================

symbol = "BTCUSDT"
timeframe = "15m"

lookback = 50


# ============================================================
# CLIENTE BINANCE
# ============================================================

client = create_public_client()


# ============================================================
# DATOS
# ============================================================

df = get_futures_klines(
    client=client,
    symbol=symbol,
    interval=timeframe,
    limit=100,
)


# ============================================================
# CONSTRUIR GRID
# ============================================================

result = build_dynamic_grid(
    df=df,
    lookback=lookback,
)


# ============================================================
# RESULTADOS
# ============================================================

print()
print(f"PAR: {symbol}")
print(f"TIMEFRAME: {timeframe}")
print(f"VELAS ANALIZADAS: {lookback}")

print()
print(
    f"PRECIO ACTUAL: "
    f"{result['current_price']:.6f}"
)

print(
    f"MÍNIMO DEL RANGO: "
    f"{result['range_low']:.6f}"
)

print(
    f"MÁXIMO DEL RANGO: "
    f"{result['range_high']:.6f}"
)

print(
    f"TAMAÑO DEL RANGO: "
    f"{result['range_size']:.6f}"
)

print(
    f"RANGO: "
    f"{result['range_percent']:.2f}%"
)

print()
print(
    f"ATR: "
    f"{result['atr']:.6f}"
)

print(
    f"ATR: "
    f"{result['atr_percent']:.2f}%"
)

print(
    f"RANGO EN ATR: "
    f"{result['range_in_atr']:.2f} ATR"
)

print()
print(
    f"NIVELES DINÁMICOS: "
    f"{result['levels']}"
)

print(
    f"SEPARACIÓN: "
    f"{result['spacing']:.6f}"
)

print(
    f"SEPARACIÓN EN ATR: "
    f"{result['spacing'] / result['atr']:.2f} ATR"
)

print()
print("NIVELES DE GRID:")

for index, price in enumerate(
    result["grid"],
    start=1,
):
    print(
        f"{index:02d}. {price:.6f}"
    )


print()
print("=" * 60)
print("FIN DEL TEST")
print("=" * 60)