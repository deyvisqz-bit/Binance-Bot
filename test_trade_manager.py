from src.trade_manager import TradeManager
from src.trade_simulator import simulate_trade


INITIAL_CAPITAL = 100.0
NOMINAL = 125.0
ENTRY = 83601.85


print("=" * 70)
print("PRUEBA DEL CICLO COMPLETO DE OPERACIÓN")
print("=" * 70)

manager = TradeManager(
    initial_capital=INITIAL_CAPITAL
)

print()
print("CAPITAL INICIAL:")
print(
    f"{manager.current_capital:.4f} USDT"
)


print()
print("=" * 70)
print("OPERACIÓN 1: LONG → TAKE PROFIT")
print("=" * 70)

trade = manager.open_trade(
    symbol="BTCUSDT",
    direction="LONG",
    entry_price=ENTRY,
    nominal=NOMINAL,
)

price_path = [
    83700,
    84000,
    84500,
    85000,
    85500,
]

simulation = simulate_trade(
    entry_price=ENTRY,
    direction="LONG",
    nominal=NOMINAL,
    price_path=price_path,
)

closed_trade = manager.close_trade(
    trade=trade,
    exit_price=simulation["exit_price"],
    exit_reason=simulation["exit_reason"],
    pnl=simulation["pnl"],
)

print(
    f"ENTRADA: {closed_trade['entry_price']:.4f}"
)

print(
    f"SALIDA: {closed_trade['exit_price']:.4f}"
)

print(
    f"RESULTADO: {closed_trade['exit_reason']}"
)

print(
    f"PNL: {closed_trade['pnl']:.4f} USDT"
)

print(
    f"CAPITAL DESPUÉS: "
    f"{closed_trade['capital_after']:.4f} USDT"
)


print()
print("=" * 70)
print("OPERACIÓN 2: SHORT → STOP LOSS")
print("=" * 70)

entry_2 = 83601.85

trade = manager.open_trade(
    symbol="BTCUSDT",
    direction="SHORT",
    entry_price=entry_2,
    nominal=NOMINAL,
)

price_path = [
    84000,
    85000,
    86000,
    87000,
    88000,
]

simulation = simulate_trade(
    entry_price=entry_2,
    direction="SHORT",
    nominal=NOMINAL,
    price_path=price_path,
)

closed_trade = manager.close_trade(
    trade=trade,
    exit_price=simulation["exit_price"],
    exit_reason=simulation["exit_reason"],
    pnl=simulation["pnl"],
)

print(
    f"ENTRADA: {closed_trade['entry_price']:.4f}"
)

print(
    f"SALIDA: {closed_trade['exit_price']:.4f}"
)

print(
    f"RESULTADO: {closed_trade['exit_reason']}"
)

print(
    f"PNL: {closed_trade['pnl']:.4f} USDT"
)

print(
    f"CAPITAL DESPUÉS: "
    f"{closed_trade['capital_after']:.4f} USDT"
)


print()
print("=" * 70)
print("ESTADÍSTICAS FINALES")
print("=" * 70)

stats = manager.get_statistics()

print(
    f"CAPITAL INICIAL: "
    f"{stats['initial_capital']:.4f} USDT"
)

print(
    f"CAPITAL ACTUAL: "
    f"{stats['current_capital']:.4f} USDT"
)

print(
    f"CAMBIO: "
    f"{stats['capital_change']:.4f} USDT"
)

print(
    f"CAMBIO %: "
    f"{stats['capital_change_percent']:.4f}%"
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


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)
print("NO SE ENVIO NINGUNA ORDEN REAL.")