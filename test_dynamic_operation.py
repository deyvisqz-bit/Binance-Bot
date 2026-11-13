from src.trade_manager import TradeManager
from src.trade_simulator import simulate_trade


INITIAL_CAPITAL = 100.0
ENTRY = 83601.85


print("=" * 70)
print("PRUEBA DE OPERACIÓN DINÁMICA")
print("=" * 70)

manager = TradeManager(
    initial_capital=INITIAL_CAPITAL,
    operating_capital_percent=0.125,
    leverage=10,
)


print()
print("=" * 70)
print("ESTADO INICIAL")
print("=" * 70)

print(
    f"CAPITAL: "
    f"{manager.get_current_capital():.4f} USDT"
)

print(
    f"CAPITAL OPERATIVO: "
    f"{manager.get_operating_capital():.4f} USDT"
)

print(
    f"NOMINAL: "
    f"{manager.get_nominal():.4f} USDT"
)


print()
print("=" * 70)
print("OPERACIÓN 1")
print("=" * 70)

trade_1 = manager.open_trade(
    symbol="BTCUSDT",
    direction="LONG",
    entry_price=ENTRY,
)

print(
    f"NOMINAL UTILIZADO: "
    f"{trade_1['nominal']:.4f} USDT"
)

simulation_1 = simulate_trade(
    entry_price=ENTRY,
    direction="LONG",
    nominal=trade_1["nominal"],
    price_path=[
        84000,
        84500,
        85000,
        85500,
    ],
)

result_1 = manager.close_trade(
    trade=trade_1,
    exit_price=simulation_1["exit_price"],
    exit_reason=simulation_1["exit_reason"],
    pnl=simulation_1["pnl"],
)

print(
    f"RESULTADO: "
    f"{result_1['exit_reason']}"
)

print(
    f"PNL: "
    f"{result_1['pnl']:.4f} USDT"
)

print(
    f"CAPITAL NUEVO: "
    f"{result_1['capital_after']:.4f} USDT"
)

print(
    f"NUEVO CAPITAL OPERATIVO: "
    f"{result_1['operating_capital_after']:.4f} USDT"
)

print(
    f"NUEVO NOMINAL: "
    f"{result_1['nominal_after']:.4f} USDT"
)


print()
print("=" * 70)
print("OPERACIÓN 2")
print("=" * 70)

trade_2 = manager.open_trade(
    symbol="BTCUSDT",
    direction="SHORT",
    entry_price=ENTRY,
)

print(
    f"CAPITAL ANTES: "
    f"{trade_2['capital_before']:.4f} USDT"
)

print(
    f"CAPITAL OPERATIVO: "
    f"{trade_2['operating_capital']:.4f} USDT"
)

print(
    f"NOMINAL UTILIZADO: "
    f"{trade_2['nominal']:.4f} USDT"
)

simulation_2 = simulate_trade(
    entry_price=ENTRY,
    direction="SHORT",
    nominal=trade_2["nominal"],
    price_path=[
        84000,
        85000,
        86000,
        87000,
        88000,
    ],
)

result_2 = manager.close_trade(
    trade=trade_2,
    exit_price=simulation_2["exit_price"],
    exit_reason=simulation_2["exit_reason"],
    pnl=simulation_2["pnl"],
)

print(
    f"RESULTADO: "
    f"{result_2['exit_reason']}"
)

print(
    f"PNL: "
    f"{result_2['pnl']:.4f} USDT"
)

print(
    f"CAPITAL FINAL: "
    f"{result_2['capital_after']:.4f} USDT"
)

print(
    f"NUEVO CAPITAL OPERATIVO: "
    f"{result_2['operating_capital_after']:.4f} USDT"
)

print(
    f"NUEVO NOMINAL: "
    f"{result_2['nominal_after']:.4f} USDT"
)


print()
print("=" * 70)
print("ESTADÍSTICAS")
print("=" * 70)

stats = manager.get_statistics()

print(
    f"CAPITAL INICIAL: "
    f"{stats['initial_capital']:.4f} USDT"
)

print(
    f"CAPITAL FINAL: "
    f"{stats['current_capital']:.4f} USDT"
)

print(
    f"CAPITAL OPERATIVO ACTUAL: "
    f"{stats['operating_capital']:.4f} USDT"
)

print(
    f"NOMINAL ACTUAL: "
    f"{stats['nominal']:.4f} USDT"
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


print()
print("=" * 70)
print("VALIDACIÓN")
print("=" * 70)

expected_first_nominal = 125.0

if abs(
    trade_1["nominal"]
    - expected_first_nominal
) < 0.000001:

    print("NOMINAL INICIAL: OK")

else:

    print("NOMINAL INICIAL: ERROR")


expected_second_nominal = (
    result_1["capital_after"]
    * 0.125
    * 10
)

if abs(
    trade_2["nominal"]
    - expected_second_nominal
) < 0.000001:

    print("NOMINAL DINÁMICO: OK")

else:

    print("NOMINAL DINÁMICO: ERROR")


expected_current_nominal = (
    result_2["capital_after"]
    * 0.125
    * 10
)

if abs(
    manager.get_nominal()
    - expected_current_nominal
) < 0.000001:

    print("CAPITAL → NOMINAL: OK")

else:

    print("CAPITAL → NOMINAL: ERROR")


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)
print("NO SE ENVIO NINGUNA ORDEN REAL.")