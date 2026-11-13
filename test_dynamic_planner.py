from src.capital_manager import CapitalManager
from src.trade_manager import TradeManager
from src.operation_planner import build_operation_plan


INITIAL_CAPITAL = 100.0
OPERATING_PERCENT = 0.125
LEVERAGE = 10

SYMBOL = "BTCUSDT"
ENTRY_PRICE = 83601.85


grid_plan = {
    "valid": True,
    "range_low": 82706.20,
    "range_high": 84497.50,
    "range_size": 1791.30,
    "levels": 11,
    "grid_count": 11,
    "grid_levels": [
        82706.20,
        82885.33,
        83064.46,
        83243.59,
        83422.72,
        83601.85,
        83780.98,
        83960.11,
        84139.24,
        84318.37,
        84497.50,
    ],
    "grid": [
        82706.20,
        82885.33,
        83064.46,
        83243.59,
        83422.72,
        83601.85,
        83780.98,
        83960.11,
        84139.24,
        84318.37,
        84497.50,
    ],
    "spacing": 179.13,
}


print("=" * 70)
print("PRUEBA DEL PLANIFICADOR DINÁMICO")
print("=" * 70)


capital_manager = CapitalManager(
    initial_capital=INITIAL_CAPITAL,
    operating_capital_percent=OPERATING_PERCENT,
    leverage=LEVERAGE,
)

trade_manager = TradeManager(
    initial_capital=INITIAL_CAPITAL,
    operating_capital_percent=OPERATING_PERCENT,
    leverage=LEVERAGE,
    capital_manager=capital_manager,
)


print()
print("=" * 70)
print("ESTADO INICIAL")
print("=" * 70)

print(
    f"CAPITAL TOTAL: "
    f"{trade_manager.get_current_capital():.4f}"
)

print(
    f"CAPITAL OPERATIVO: "
    f"{trade_manager.get_operating_capital():.4f}"
)

print(
    f"NOMINAL: "
    f"{trade_manager.get_nominal():.4f}"
)


print()
print("=" * 70)
print("PLAN LONG")
print("=" * 70)


long_plan = build_operation_plan(
    symbol=SYMBOL,
    direction="LONG",
    current_price=ENTRY_PRICE,
    grid_plan=grid_plan,
    operating_capital=(
        trade_manager.get_operating_capital()
    ),
    leverage=LEVERAGE,
    nominal=trade_manager.get_nominal(),
)


print(
    f"DIRECCIÓN: "
    f"{long_plan['direction']}"
)

print(
    f"ENTRADA: "
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
    f"GRID LEVELS: "
    f"{long_plan['levels']}"
)


print()
print("=" * 70)
print("SIMULANDO GANANCIA DE +2.50 USDT")
print("=" * 70)


capital_manager.update_capital(
    pnl=2.50
)


print(
    f"NUEVO CAPITAL: "
    f"{trade_manager.get_current_capital():.4f}"
)

print(
    f"NUEVO CAPITAL OPERATIVO: "
    f"{trade_manager.get_operating_capital():.4f}"
)

print(
    f"NUEVO NOMINAL: "
    f"{trade_manager.get_nominal():.4f}"
)


print()
print("=" * 70)
print("PLAN SHORT DESPUÉS DE LA GANANCIA")
print("=" * 70)


short_plan = build_operation_plan(
    symbol=SYMBOL,
    direction="SHORT",
    current_price=ENTRY_PRICE,
    grid_plan=grid_plan,
    operating_capital=(
        trade_manager.get_operating_capital()
    ),
    leverage=LEVERAGE,
    nominal=trade_manager.get_nominal(),
)


print(
    f"DIRECCIÓN: "
    f"{short_plan['direction']}"
)

print(
    f"ENTRADA: "
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


print()
print("=" * 70)
print("VALIDACIÓN")
print("=" * 70)


if long_plan["valid"]:
    print("PLAN LONG: OK")
else:
    print("PLAN LONG: ERROR")


if short_plan["valid"]:
    print("PLAN SHORT: OK")
else:
    print("PLAN SHORT: ERROR")


if (
    abs(long_plan["nominal"] - 125.0)
    < 0.000001
):
    print("NOMINAL INICIAL: OK")
else:
    print("NOMINAL INICIAL: ERROR")


if (
    abs(short_plan["nominal"] - 128.125)
    < 0.000001
):
    print("NOMINAL DESPUÉS DE GANANCIA: OK")
else:
    print(
        "NOMINAL DESPUÉS DE GANANCIA: ERROR"
    )


if (
    long_plan["take_profit"]
    > long_plan["entry_price"]
    and
    long_plan["stop_loss"]
    < long_plan["entry_price"]
):
    print("TP/SL LONG: OK")
else:
    print("TP/SL LONG: ERROR")


if (
    short_plan["take_profit"]
    < short_plan["entry_price"]
    and
    short_plan["stop_loss"]
    > short_plan["entry_price"]
):
    print("TP/SL SHORT: OK")
else:
    print("TP/SL SHORT: ERROR")


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)

print(
    "NO SE ENVIO NINGUNA ORDEN REAL."
)