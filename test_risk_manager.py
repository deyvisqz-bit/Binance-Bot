from src.risk_manager import RiskManager


INITIAL_CAPITAL = 100.0


manager = RiskManager(
    initial_capital=INITIAL_CAPITAL,
    daily_target_percent=0.05,
    daily_loss_limit_percent=0.05,
    max_open_positions=10,
)


print("=" * 70)
print("PRUEBA DEL GESTOR DE RIESGO")
print("=" * 70)


print()
print("=" * 70)
print("ESTADO INICIAL")
print("=" * 70)

status = manager.get_status(
    current_capital=100.0
)

print(
    f"PNL DIARIO: "
    f"{status['daily_pnl']:.4f} USDT"
)

print(
    f"OBJETIVO DIARIO: "
    f"{status['daily_target']:.4f} USDT"
)

print(
    f"LÍMITE DE PÉRDIDA: "
    f"{status['daily_loss_limit']:.4f} USDT"
)

print(
    f"POSICIONES ABIERTAS: "
    f"{status['open_positions']}"
)


print()
print("=" * 70)
print("PRUEBA 1: ABRIR POSICIONES")
print("=" * 70)

for i in range(10):

    result = manager.register_open_position()

    print(
        f"POSICIÓN {i + 1}: "
        f"{'PERMITIDA' if result['allowed'] else 'BLOQUEADA'}"
    )


print()
print("=" * 70)
print("PRUEBA 2: INTENTAR POSICIÓN #11")
print("=" * 70)

result = manager.can_open_new_trade(
    current_capital=100.0
)

print(
    f"PERMITIDA: "
    f"{result['allowed']}"
)

print(
    f"MOTIVO: "
    f"{result['reason']}"
)


print()
print("=" * 70)
print("PRUEBA 3: CERRAR UNA POSICIÓN")
print("=" * 70)

status = manager.register_closed_position(
    pnl=2.50,
    current_capital=102.50,
)

print(
    f"PNL DIARIO: "
    f"{status['daily_pnl']:.4f} USDT"
)

print(
    f"POSICIONES ABIERTAS: "
    f"{status['open_positions']}"
)


print()
print("=" * 70)
print("PRUEBA 4: OBJETIVO DIARIO")
print("=" * 70)

manager.daily_pnl = 5.00

result = manager.can_open_new_trade(
    current_capital=100.0
)

print(
    f"PERMITIDA: "
    f"{result['allowed']}"
)

print(
    f"MOTIVO: "
    f"{result['reason']}"
)


print()
print("=" * 70)
print("REINICIANDO DÍA")
print("=" * 70)

manager.reset_daily()

status = manager.get_status(
    current_capital=100.0
)

print(
    f"PNL DIARIO: "
    f"{status['daily_pnl']:.4f} USDT"
)

print(
    f"BLOQUEADO: "
    f"{status['trading_blocked']}"
)


print()
print("=" * 70)
print("PRUEBA 5: LÍMITE DE PÉRDIDA")
print("=" * 70)

manager.daily_pnl = -5.00

result = manager.can_open_new_trade(
    current_capital=100.0
)

print(
    f"PERMITIDA: "
    f"{result['allowed']}"
)

print(
    f"MOTIVO: "
    f"{result['reason']}"
)


print()
print("=" * 70)
print("VALIDACIÓN")
print("=" * 70)

manager.reset_daily()

for _ in range(10):
    manager.register_open_position()

result_max = manager.can_open_new_trade(
    current_capital=100.0
)

if not result_max["allowed"]:
    print("MÁXIMO 10 POSICIONES: OK")
else:
    print("MÁXIMO 10 POSICIONES: ERROR")


manager.reset_daily()

manager.daily_pnl = 5.00

result_target = manager.can_open_new_trade(
    current_capital=100.0
)

if not result_target["allowed"]:
    print("OBJETIVO DIARIO +5%: OK")
else:
    print("OBJETIVO DIARIO +5%: ERROR")


manager.reset_daily()

manager.daily_pnl = -5.00

result_loss = manager.can_open_new_trade(
    current_capital=100.0
)

if not result_loss["allowed"]:
    print("LÍMITE DIARIO -5%: OK")
else:
    print("LÍMITE DIARIO -5%: ERROR")


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)

print(
    "NO SE ENVIO NINGUNA ORDEN REAL."
)