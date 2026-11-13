from src.risk_manager import RiskManager


INITIAL_CAPITAL = 100.0
DAILY_TARGET_PERCENT = 0.05
DAILY_LOSS_LIMIT_PERCENT = 0.05
MAX_OPEN_POSITIONS = 10


print("=" * 70)
print("PRUEBA DEL LÍMITE DE PÉRDIDA DIARIA")
print("=" * 70)


# ============================================================
# CREAR RISK MANAGER
# ============================================================

manager = RiskManager(
    initial_capital=INITIAL_CAPITAL,
    daily_target_percent=DAILY_TARGET_PERCENT,
    daily_loss_limit_percent=DAILY_LOSS_LIMIT_PERCENT,
    max_open_positions=MAX_OPEN_POSITIONS,
)


# ============================================================
# ESTADO INICIAL
# ============================================================

print()
print("=" * 70)
print("ESTADO INICIAL")
print("=" * 70)

print(
    f"CAPITAL INICIAL: "
    f"{manager.initial_capital:.4f} USDT"
)

print(
    f"LÍMITE DE PÉRDIDA DIARIA: "
    f"{manager.calculate_daily_loss_limit(INITIAL_CAPITAL):.4f} USDT"
)

print(
    f"PNL DIARIO INICIAL: "
    f"{manager.daily_pnl:.4f} USDT"
)


# ============================================================
# PRUEBA 1: PÉRDIDA POR DEBAJO DEL LÍMITE
# ============================================================

print()
print("=" * 70)
print("PRUEBA 1: PÉRDIDA POR DEBAJO DEL LÍMITE")
print("=" * 70)

manager.daily_pnl = -4.99

result = manager.can_open_new_trade(
    current_capital=INITIAL_CAPITAL
)

print(
    f"PNL DIARIO: "
    f"{manager.daily_pnl:.4f} USDT"
)

print(
    f"PERMITIDA: "
    f"{result['allowed']}"
)

print(
    f"MOTIVO: "
    f"{result['reason']}"
)

if result["allowed"]:
    print("RESULTADO: OK")
else:
    print("RESULTADO: ERROR")


# ============================================================
# PRUEBA 2: LÍMITE EXACTO DE -5 USDT
# ============================================================

print()
print("=" * 70)
print("PRUEBA 2: LÍMITE EXACTO DE -5 USDT")
print("=" * 70)

manager.daily_pnl = -5.00

result = manager.can_open_new_trade(
    current_capital=INITIAL_CAPITAL
)

print(
    f"PNL DIARIO: "
    f"{manager.daily_pnl:.4f} USDT"
)

print(
    f"PERMITIDA: "
    f"{result['allowed']}"
)

print(
    f"MOTIVO: "
    f"{result['reason']}"
)

if not result["allowed"]:
    print("RESULTADO: OK")
else:
    print("RESULTADO: ERROR")


# ============================================================
# PRUEBA 3: PÉRDIDA SUPERIOR AL LÍMITE
# ============================================================

print()
print("=" * 70)
print("PRUEBA 3: PÉRDIDA SUPERIOR AL LÍMITE")
print("=" * 70)

manager.daily_pnl = -6.00

result = manager.can_open_new_trade(
    current_capital=INITIAL_CAPITAL
)

print(
    f"PNL DIARIO: "
    f"{manager.daily_pnl:.4f} USDT"
)

print(
    f"PERMITIDA: "
    f"{result['allowed']}"
)

print(
    f"MOTIVO: "
    f"{result['reason']}"
)

if not result["allowed"]:
    print("RESULTADO: OK")
else:
    print("RESULTADO: ERROR")


# ============================================================
# VALIDACIÓN FINAL
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN FINAL")
print("=" * 70)

manager.daily_pnl = -5.00

final_result = manager.can_open_new_trade(
    current_capital=INITIAL_CAPITAL
)

if not final_result["allowed"]:
    print("LÍMITE DE PÉRDIDA -5%: OK")
else:
    print("LÍMITE DE PÉRDIDA -5%: ERROR")


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)

print()
print("NO SE ENVIÓ NINGUNA ORDEN REAL.")