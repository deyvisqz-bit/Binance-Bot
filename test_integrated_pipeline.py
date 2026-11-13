from src.binance_client import (
    create_public_client,
    get_futures_klines,
)

from src.grid_engine import build_dynamic_grid

from src.range_position import (
    calculate_range_position,
)

from src.entry_filter import (
    evaluate_entry_filter,
)

from src.operation_planner import (
    build_operation_plan,
)

from src.capital_manager import (
    CapitalManager,
)

from src.trade_manager import (
    TradeManager,
)

from src.trade_simulator import (
    simulate_trade,
)


# ============================================================
# CONFIGURACIÓN DE LA PRUEBA
# ============================================================

SYMBOL = "BTCUSDT"

INITIAL_CAPITAL = 100.0

OPERATING_CAPITAL_PERCENT = 0.125

LEVERAGE = 10

TIMEFRAME = "15m"

CANDLE_LIMIT = 200


# ============================================================
# INICIO
# ============================================================

print("=" * 70)
print("PIPELINE INTEGRADO DEL BOT")
print("=" * 70)

print()
print("PAR:", SYMBOL)
print("DATOS: BINANCE REAL")
print("ÓRDENES REALES: DESACTIVADAS")


# ============================================================
# CLIENTE BINANCE
# ============================================================

client = create_public_client()


# ============================================================
# CAPITAL
# ============================================================

capital_manager = CapitalManager(
    initial_capital=INITIAL_CAPITAL,
    operating_capital_percent=(
        OPERATING_CAPITAL_PERCENT
    ),
    leverage=LEVERAGE,
)

trade_manager = TradeManager(
    initial_capital=INITIAL_CAPITAL,
    operating_capital_percent=(
        OPERATING_CAPITAL_PERCENT
    ),
    leverage=LEVERAGE,
    capital_manager=capital_manager,
)


print()
print("=" * 70)
print("CAPITAL INICIAL")
print("=" * 70)

print(
    f"CAPITAL TOTAL: "
    f"{trade_manager.get_current_capital():.4f} USDT"
)

print(
    f"CAPITAL OPERATIVO: "
    f"{trade_manager.get_operating_capital():.4f} USDT"
)

print(
    f"NOMINAL: "
    f"{trade_manager.get_nominal():.4f} USDT"
)


# ============================================================
# DATOS REALES DE BINANCE
# ============================================================

print()
print("=" * 70)
print("DESCARGANDO DATOS")
print("=" * 70)

df = get_futures_klines(
    client=client,
    symbol=SYMBOL,
    interval=TIMEFRAME,
    limit=CANDLE_LIMIT,
)

print(
    f"VELAS RECIBIDAS: {len(df)}"
)

if len(df) < 50:

    print(
        "ERROR: No hay suficientes velas."
    )

    raise SystemExit


# ============================================================
# GRID DINÁMICO
# ============================================================

print()
print("=" * 70)
print("GRID DINÁMICO")
print("=" * 70)

grid_result = build_dynamic_grid(
    df,
    lookback=50,
)

if not grid_result.get("valid", False):

    print(
        "ERROR: El grid dinámico no es válido."
    )

    raise SystemExit


range_low = grid_result["range_low"]

range_high = grid_result["range_high"]

range_size = grid_result["range_size"]

levels = grid_result["levels"]

grid = grid_result["grid"]

spacing = grid_result["spacing"]

current_price = float(
    df.iloc[-1]["close"]
)


print(
    f"RANGE LOW: {range_low:.4f}"
)

print(
    f"RANGE HIGH: {range_high:.4f}"
)

print(
    f"RANGE SIZE: {range_size:.4f}"
)

print(
    f"GRID LEVELS: {levels}"
)

print(
    f"GRID SPACING: {spacing:.4f}"
)

print(
    f"PRECIO ACTUAL: {current_price:.4f}"
)


# ============================================================
# POSICIÓN DENTRO DEL RANGO
# ============================================================

print()
print("=" * 70)
print("POSICIÓN DENTRO DEL RANGO")
print("=" * 70)

range_result = calculate_range_position(
    current_price,
    range_low,
    range_high,
)

position_percent = range_result[
    "position_percent"
]

zone = range_result["zone"]


print(
    f"POSICIÓN: "
    f"{position_percent:.2f}%"
)

print(
    f"ZONA: {zone}"
)


# ============================================================
# GRID PLAN
# ============================================================

grid_plan = {
    "valid": True,

    "range_low": range_low,

    "range_high": range_high,

    "range_min": range_low,

    "range_max": range_high,

    "range_size": range_size,

    "levels": levels,

    "grid_count": levels,

    "grid_levels": grid,

    "grid": grid,

    "spacing": spacing,

    "grid_spacing": spacing,

    "reason": (
        "Grid dinámico generado "
        "con datos reales de Binance."
    ),
}


# ============================================================
# PRUEBA LONG
# ============================================================

print()
print("=" * 70)
print("ETAPA LONG")
print("=" * 70)

long_filter = evaluate_entry_filter(
    direction="LONG",
    trigger=True,
    trigger_direction="LONG",
    position_percent=position_percent,
)

print(
    f"FILTRO: "
    f"{long_filter['decision']}"
)

print(
    f"MOTIVO: "
    f"{long_filter['reason']}"
)


if long_filter["decision"] == "ENTRY":

    long_plan = build_operation_plan(
        symbol=SYMBOL,
        direction="LONG",
        current_price=current_price,
        grid_plan=grid_plan,
        operating_capital=(
            trade_manager.get_operating_capital()
        ),
        leverage=LEVERAGE,
        nominal=trade_manager.get_nominal(),
    )

    if not long_plan["valid"]:

        print(
            "ERROR: Plan LONG inválido."
        )

        raise SystemExit

    print()
    print("PLAN LONG")

    print(
        f"ENTRY: "
        f"{long_plan['entry_price']:.4f}"
    )

    print(
        f"TAKE PROFIT: "
        f"{long_plan['take_profit']:.4f}"
    )

    print(
        f"STOP LOSS: "
        f"{long_plan['stop_loss']:.4f}"
    )

    print(
        f"CAPITAL OPERATIVO: "
        f"{long_plan['operating_capital']:.4f}"
    )

    print(
        f"NOMINAL: "
        f"{long_plan['nominal']:.4f}"
    )

    print(
        "PLAN LONG: OK"
    )

else:

    print(
        "LONG: WAIT"
    )

    long_plan = None


# ============================================================
# SIMULACIÓN DE CIERRE LONG
# ============================================================

if long_plan is not None:

    print()
    print("=" * 70)
    print("SIMULACIÓN LONG → TAKE PROFIT")
    print("=" * 70)

    long_trade = trade_manager.open_trade(
        symbol=SYMBOL,
        direction="LONG",
        entry_price=long_plan["entry_price"],
        nominal=long_plan["nominal"],
    )

    long_simulation = simulate_trade(
        entry_price=long_plan["entry_price"],
        direction="LONG",
        nominal=long_plan["nominal"],
        price_path=[
            long_plan["entry_price"] * 1.005,
            long_plan["entry_price"] * 1.010,
            long_plan["entry_price"] * 1.015,
            long_plan["take_profit"],
        ],
    )

    long_result = trade_manager.close_trade(
        trade=long_trade,
        exit_price=long_simulation["exit_price"],
        exit_reason=long_simulation["exit_reason"],
        pnl=long_simulation["pnl"],
    )

    print(
        f"RESULTADO: "
        f"{long_result['exit_reason']}"
    )

    print(
        f"SALIDA: "
        f"{long_result['exit_price']:.4f}"
    )

    print(
        f"PNL: "
        f"{long_result['pnl']:.4f} USDT"
    )

    print(
        f"CAPITAL ACTUALIZADO: "
        f"{long_result['capital_after']:.4f} USDT"
    )

    print(
        f"NUEVO CAPITAL OPERATIVO: "
        f"{long_result['operating_capital_after']:.4f} USDT"
    )

    print(
        f"NUEVO NOMINAL: "
        f"{long_result['nominal_after']:.4f} USDT"
    )


# ============================================================
# NUEVO ESCANEO DESPUÉS DEL CIERRE
# ============================================================

print()
print("=" * 70)
print("NUEVO ESCANEO DESPUÉS DEL CIERRE")
print("=" * 70)

print(
    f"CAPITAL ACTUAL: "
    f"{trade_manager.get_current_capital():.4f} USDT"
)

print(
    f"CAPITAL OPERATIVO: "
    f"{trade_manager.get_operating_capital():.4f} USDT"
)

print(
    f"NOMINAL DISPONIBLE: "
    f"{trade_manager.get_nominal():.4f} USDT"
)


# ============================================================
# PRUEBA SHORT CON CAPITAL ACTUALIZADO
# ============================================================

print()
print("=" * 70)
print("ETAPA SHORT")
print("=" * 70)

short_filter = evaluate_entry_filter(
    direction="SHORT",
    trigger=True,
    trigger_direction="SHORT",
    position_percent=position_percent,
)

print(
    f"FILTRO: "
    f"{short_filter['decision']}"
)

print(
    f"MOTIVO: "
    f"{short_filter['reason']}"
)


if short_filter["decision"] == "ENTRY":

    short_plan = build_operation_plan(
        symbol=SYMBOL,
        direction="SHORT",
        current_price=current_price,
        grid_plan=grid_plan,
        operating_capital=(
            trade_manager.get_operating_capital()
        ),
        leverage=LEVERAGE,
        nominal=trade_manager.get_nominal(),
    )

    if not short_plan["valid"]:

        print(
            "ERROR: Plan SHORT inválido."
        )

        raise SystemExit

    print()
    print("PLAN SHORT")

    print(
        f"ENTRY: "
        f"{short_plan['entry_price']:.4f}"
    )

    print(
        f"TAKE PROFIT: "
        f"{short_plan['take_profit']:.4f}"
    )

    print(
        f"STOP LOSS: "
        f"{short_plan['stop_loss']:.4f}"
    )

    print(
        f"CAPITAL OPERATIVO: "
        f"{short_plan['operating_capital']:.4f}"
    )

    print(
        f"NOMINAL: "
        f"{short_plan['nominal']:.4f}"
    )

    print(
        "PLAN SHORT: OK"
    )

else:

    print(
        "SHORT: WAIT"
    )

    short_plan = None


# ============================================================
# ESTADÍSTICAS FINALES
# ============================================================

print()
print("=" * 70)
print("ESTADÍSTICAS FINALES")
print("=" * 70)

stats = trade_manager.get_statistics()

print(
    f"CAPITAL INICIAL: "
    f"{stats['initial_capital']:.4f} USDT"
)

print(
    f"CAPITAL FINAL: "
    f"{stats['current_capital']:.4f} USDT"
)

print(
    f"CAPITAL OPERATIVO: "
    f"{stats['operating_capital']:.4f} USDT"
)

print(
    f"NOMINAL ACTUAL: "
    f"{stats['nominal']:.4f} USDT"
)

print(
    f"PNL DEL DÍA: "
    f"{stats['daily_pnl']:.4f} USDT"
)

print(
    f"OPERACIONES: "
    f"{stats['total_trades']}"
)

print(
    f"GANADORAS: "
    f"{stats['winning_trades']}"
)

print(
    f"PERDEDORAS: "
    f"{stats['losing_trades']}"
)

print(
    f"WIN RATE: "
    f"{stats['win_rate']:.2f}%"
)


# ============================================================
# VALIDACIÓN
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN DEL PIPELINE")
print("=" * 70)

if grid_result["valid"]:
    print("GRID DINÁMICO: OK")
else:
    print("GRID DINÁMICO: ERROR")


if (
    0 <= position_percent <= 100
):
    print("POSICIÓN EN RANGO: OK")
else:
    print("POSICIÓN EN RANGO: ERROR")


if long_plan is not None:
    print("PLAN LONG INTEGRADO: OK")
else:
    print(
        "PLAN LONG INTEGRADO: WAIT"
    )


if long_plan is not None:

    if (
        long_result["exit_reason"]
        == "TAKE_PROFIT"
    ):
        print(
            "CIERRE LONG TP: OK"
        )

    else:
        print(
            "CIERRE LONG TP: ERROR"
        )


if short_plan is not None:

    print(
        "PLAN SHORT DINÁMICO: OK"
    )


print()
print("=" * 70)
print("FIN DEL PIPELINE")
print("=" * 70)

print(
    "NO SE ENVIO NINGUNA ORDEN REAL."
)