from src.binance_client import (
    create_public_client,
    get_futures_klines,
)

from src.grid_engine import (
    build_dynamic_grid,
)

from src.range_position import (
    calculate_range_position,
)

from src.entry_filter import (
    evaluate_entry_filter,
)

from src.operation_planner import (
    build_operation_plan,
)


# ==========================================================
# CONFIGURACIÓN DE PRUEBA
# ==========================================================

SYMBOL = "BTCUSDT"

INITIAL_CAPITAL = 100.0
OPERATING_CAPITAL_PERCENT = 0.125
LEVERAGE = 10

OPERATING_CAPITAL = (
    INITIAL_CAPITAL
    * OPERATING_CAPITAL_PERCENT
)


# ==========================================================
# CLIENTE PÚBLICO DE BINANCE
# ==========================================================

client = create_public_client()


# ==========================================================
# FUNCIÓN PARA CREAR EL GRID PLAN
# ==========================================================

def create_grid_plan(
    direction,
    range_low,
    range_high,
    range_size,
    levels,
    grid,
    spacing,
):
    """
    Construye un grid_plan compatible con
    grid_engine y operation_planner.

    Se mantienen nombres alternativos temporalmente
    para evitar incompatibilidades entre módulos.
    """

    return {
        # Estado
        "valid": True,

        # Dirección
        "direction": direction,

        # Rango principal
        "range_low": range_low,
        "range_high": range_high,

        # Nombres utilizados por operation_planner
        "range_min": range_low,
        "range_max": range_high,

        # Tamaño del rango
        "range_size": range_size,

        # Cantidad de niveles
        "levels": levels,
        "grid_count": levels,

        # Niveles del grid
        "grid": grid,
        "grid_levels": grid,

        # Separación
        "spacing": spacing,
        "grid_spacing": spacing,

        # Información
        "reason": (
            f"Prueba controlada {direction}"
        ),
    }


# ==========================================================
# INICIO
# ==========================================================

print()
print("=" * 70)
print("PRUEBA CONTROLADA DEL PIPELINE")
print("=" * 70)

print()
print(f"PAR: {SYMBOL}")
print("DATOS: BINANCE REAL")
print("ÓRDENES: DESACTIVADAS")


# ==========================================================
# OBTENER DATOS 15M
# ==========================================================

df_15m = get_futures_klines(
    client,
    SYMBOL,
    "15m",
    limit=200
)


# ==========================================================
# CONSTRUIR GRID DINÁMICO
# ==========================================================

grid_result = build_dynamic_grid(
    df_15m,
    lookback=50
)


if not grid_result["valid"]:

    print()
    print("ERROR: Grid dinámico no válido.")
    raise SystemExit


# ==========================================================
# EXTRAER DATOS DEL GRID
# ==========================================================

range_low = grid_result["range_low"]
range_high = grid_result["range_high"]
range_size = grid_result["range_size"]

grid = grid_result["grid"]
levels = grid_result["levels"]
spacing = grid_result["spacing"]


# ==========================================================
# MOSTRAR GRID
# ==========================================================

print()
print("=" * 70)
print("GRID DINÁMICO")
print("=" * 70)

print(
    f"RANGE LOW:  {range_low}"
)

print(
    f"RANGE HIGH: {range_high}"
)

print(
    f"RANGE SIZE: {range_size}"
)

print(
    f"NIVELES:    {levels}"
)

print(
    f"SPACING:    {spacing}"
)


# ==========================================================
# PRECIO DE PRUEBA
# ==========================================================

# Utilizamos el 50% del rango.
#
# Esto NO es una señal real.
# Es solamente una condición controlada
# para probar el pipeline completo.

test_price = (
    range_low
    + (range_size * 0.50)
)


# ==========================================================
# POSICIÓN DENTRO DEL RANGO
# ==========================================================

range_result = calculate_range_position(
    test_price,
    range_low,
    range_high
)


position_percent = (
    range_result["position_percent"]
)

zone = range_result["zone"]


print()
print("=" * 70)
print("POSICIÓN DENTRO DEL RANGO")
print("=" * 70)

print(
    f"PRECIO DE PRUEBA: {test_price}"
)

print(
    f"POSICIÓN: {position_percent:.2f}%"
)

print(
    f"ZONA: {zone}"
)


# ==========================================================
# CREAR GRID PLAN LONG
# ==========================================================

long_grid_plan = create_grid_plan(
    direction="LONG",
    range_low=range_low,
    range_high=range_high,
    range_size=range_size,
    levels=levels,
    grid=grid,
    spacing=spacing,
)


# ==========================================================
# CREAR GRID PLAN SHORT
# ==========================================================

short_grid_plan = create_grid_plan(
    direction="SHORT",
    range_low=range_low,
    range_high=range_high,
    range_size=range_size,
    levels=levels,
    grid=grid,
    spacing=spacing,
)


# ==========================================================
# PRUEBA LONG
# ==========================================================

print()
print("=" * 70)
print("PRUEBA LONG")
print("=" * 70)


long_filter = evaluate_entry_filter(
    direction="LONG",
    trigger=True,
    trigger_direction="LONG",
    position_percent=position_percent,
)


print(
    f"FILTRO: {long_filter['decision']}"
)

print(
    f"MOTIVO: {long_filter['reason']}"
)


if long_filter["decision"] == "ENTRY":

    try:

        long_operation = build_operation_plan(
            symbol=SYMBOL,
            direction="LONG",
            current_price=test_price,
            operating_capital=OPERATING_CAPITAL,
            leverage=LEVERAGE,
            grid_plan=long_grid_plan,
        )


        print()
        print("=" * 70)
        print("PLAN LONG")
        print("=" * 70)

        print(
            f"SYMBOL:          "
            f"{long_operation['symbol']}"
        )

        print(
            f"DIRECTION:       "
            f"{long_operation['direction']}"
        )

        print(
            f"ENTRY:           "
            f"{long_operation['entry']}"
        )

        print(
            f"TAKE PROFIT:     "
            f"{long_operation['take_profit']}"
        )

        print(
            f"STOP LOSS:       "
            f"{long_operation['stop_loss']}"
        )

        print(
            f"CAPITAL:         "
            f"{long_operation['operating_capital']:.4f}"
        )

        print(
            f"LEVERAGE:        "
            f"{long_operation['leverage']}x"
        )

        print(
            f"NOMINAL:         "
            f"{long_operation['nominal']:.4f}"
        )

        print(
            f"GRID LEVELS:     "
            f"{long_operation['levels']}"
        )

        print(
            f"GRID SPACING:    "
            f"{long_operation['spacing']}"
        )

        print()
        print("LONG: PIPELINE OK")

    except Exception as error:

        print()
        print("ERROR EN PLAN LONG")
        print(
            f"{type(error).__name__}: {error}"
        )

else:

    print()
    print("LONG: FILTRO RECHAZADO")


# ==========================================================
# PRUEBA SHORT
# ==========================================================

print()
print("=" * 70)
print("PRUEBA SHORT")
print("=" * 70)


short_filter = evaluate_entry_filter(
    direction="SHORT",
    trigger=True,
    trigger_direction="SHORT",
    position_percent=position_percent,
)


print(
    f"FILTRO: {short_filter['decision']}"
)

print(
    f"MOTIVO: {short_filter['reason']}"
)


if short_filter["decision"] == "ENTRY":

    try:

        short_operation = build_operation_plan(
            symbol=SYMBOL,
            direction="SHORT",
            current_price=test_price,
            operating_capital=OPERATING_CAPITAL,
            leverage=LEVERAGE,
            grid_plan=short_grid_plan,
        )


        print()
        print("=" * 70)
        print("PLAN SHORT")
        print("=" * 70)

        print(
            f"SYMBOL:          "
            f"{short_operation['symbol']}"
        )

        print(
            f"DIRECTION:       "
            f"{short_operation['direction']}"
        )

        print(
            f"ENTRY:           "
            f"{short_operation['entry']}"
        )

        print(
            f"TAKE PROFIT:     "
            f"{short_operation['take_profit']}"
        )

        print(
            f"STOP LOSS:       "
            f"{short_operation['stop_loss']}"
        )

        print(
            f"CAPITAL:         "
            f"{short_operation['operating_capital']:.4f}"
        )

        print(
            f"LEVERAGE:        "
            f"{short_operation['leverage']}x"
        )

        print(
            f"NOMINAL:         "
            f"{short_operation['nominal']:.4f}"
        )

        print(
            f"GRID LEVELS:     "
            f"{short_operation['levels']}"
        )

        print(
            f"GRID SPACING:    "
            f"{short_operation['spacing']}"
        )

        print()
        print("SHORT: PIPELINE OK")

    except Exception as error:

        print()
        print("ERROR EN PLAN SHORT")
        print(
            f"{type(error).__name__}: {error}"
        )

else:

    print()
    print("SHORT: FILTRO RECHAZADO")


# ==========================================================
# FINAL
# ==========================================================

print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)

print()
print("NO SE ENVIÓ NINGUNA ORDEN A BINANCE.")
print("NO SE ABRIÓ NINGUNA POSICIÓN.")