from src.capital_manager import CapitalManager
from src.trade_manager import TradeManager
from src.risk_controlled_trade_manager import RiskControlledTradeManager


# ============================================================
# CONFIGURACIÓN
# ============================================================

INITIAL_CAPITAL = 100.0
OPERATING_PERCENT = 0.125
LEVERAGE = 10

SYMBOL_1 = "BTCUSDT"
SYMBOL_2 = "ETHUSDT"

ENTRY_PRICE_1 = 83601.85
ENTRY_PRICE_2 = 3000.00

PROFIT_PNL = 2.50


# ============================================================
# INICIO
# ============================================================

print("=" * 70)
print("PRUEBA DE MÚLTIPLES OPERACIONES")
print("=" * 70)


# ============================================================
# CAPITAL MANAGER
# ============================================================

capital_manager = CapitalManager(
    initial_capital=INITIAL_CAPITAL,
    operating_capital_percent=OPERATING_PERCENT,
    leverage=LEVERAGE,
)


# ============================================================
# TRADE MANAGER
# ============================================================

trade_manager = TradeManager(
    initial_capital=INITIAL_CAPITAL,
    operating_capital_percent=OPERATING_PERCENT,
    leverage=LEVERAGE,
    capital_manager=capital_manager,
)


# ============================================================
# RISK CONTROLLED TRADE MANAGER
# ============================================================

manager = RiskControlledTradeManager(
    trade_manager=trade_manager,
    initial_capital=INITIAL_CAPITAL,
    daily_target_percent=0.05,
    daily_loss_limit_percent=0.05,
    max_open_positions=10,
)


# ============================================================
# ESTADO INICIAL
# ============================================================

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


# ============================================================
# OPERACIÓN 1
# ============================================================

print()
print("=" * 70)
print("OPERACIÓN 1")
print("=" * 70)

risk_check_1 = manager.can_open_trade()

print(
    f"PERMITIDA: "
    f"{risk_check_1['allowed']}"
)

print(
    f"MOTIVO: "
    f"{risk_check_1['reason']}"
)

if not risk_check_1["allowed"]:
    print()
    print("ERROR: La operación 1 no fue permitida.")
    raise SystemExit


print()
print("ABRIENDO OPERACIÓN 1 → LONG")

open_result_1 = manager.open_trade(
    symbol=SYMBOL_1,
    direction="LONG",
    entry_price=ENTRY_PRICE_1,
)

print(
    f"OPERACIÓN ABIERTA: "
    f"{open_result_1['opened']}"
)

print(
    f"MOTIVO: "
    f"{open_result_1['reason']}"
)

if not open_result_1["opened"]:
    print()
    print("ERROR: La operación 1 no pudo abrirse.")
    raise SystemExit


trade_1 = open_result_1["trade"]


# ============================================================
# ESTADO OPERACIÓN 1
# ============================================================

print()
print("=" * 70)
print("ESTADO DURANTE OPERACIÓN 1")
print("=" * 70)

risk_status_1 = manager.get_risk_status()

print(
    f"POSICIONES ABIERTAS: "
    f"{risk_status_1['open_positions']}"
)

print(
    f"MÁXIMO PERMITIDO: "
    f"{risk_status_1['max_open_positions']}"
)

print(
    f"PNL DIARIO: "
    f"{risk_status_1['daily_pnl']:.4f} USDT"
)


# ============================================================
# CERRAR OPERACIÓN 1
# ============================================================

exit_price_1 = ENTRY_PRICE_1 * 1.02

print()
print("=" * 70)
print("CERRANDO OPERACIÓN 1 → TAKE PROFIT")
print("=" * 70)

close_result_1 = manager.close_trade(
    trade=trade_1,
    exit_price=exit_price_1,
    exit_reason="TAKE_PROFIT",
    pnl=PROFIT_PNL,
)

print(
    f"RESULTADO: "
    f"{close_result_1['exit_reason']}"
)

print(
    f"PNL: "
    f"{close_result_1['pnl']:.4f} USDT"
)

print(
    f"CAPITAL ACTUAL: "
    f"{manager.get_current_capital():.4f} USDT"
)

print(
    f"NUEVO CAPITAL OPERATIVO: "
    f"{manager.get_operating_capital():.4f} USDT"
)

print(
    f"NUEVO NOMINAL: "
    f"{manager.get_nominal():.4f} USDT"
)

print(
    f"¿PUEDE ABRIR OTRA?: "
    f"{close_result_1['can_open_new_trade']}"
)


# ============================================================
# VALIDACIÓN DESPUÉS DE OPERACIÓN 1
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN DESPUÉS DE OPERACIÓN 1")
print("=" * 70)

expected_capital_1 = 102.50
expected_operating_1 = 12.8125
expected_nominal_1 = 128.125

check_1 = [
    abs(manager.get_current_capital() - expected_capital_1) < 0.000001,
    abs(manager.get_operating_capital() - expected_operating_1) < 0.000001,
    abs(manager.get_nominal() - expected_nominal_1) < 0.000001,
    close_result_1["can_open_new_trade"] is True,
]

if all(check_1):
    print("OPERACIÓN 1: OK")
else:
    print("OPERACIÓN 1: ERROR")


# ============================================================
# OPERACIÓN 2
# ============================================================

print()
print("=" * 70)
print("OPERACIÓN 2")
print("=" * 70)

risk_check_2 = manager.can_open_trade()

print(
    f"PERMITIDA: "
    f"{risk_check_2['allowed']}"
)

print(
    f"MOTIVO: "
    f"{risk_check_2['reason']}"
)

if not risk_check_2["allowed"]:
    print()
    print("ERROR: La operación 2 no fue permitida.")
    raise SystemExit


print()
print("ABRIENDO OPERACIÓN 2 → LONG")

open_result_2 = manager.open_trade(
    symbol=SYMBOL_2,
    direction="LONG",
    entry_price=ENTRY_PRICE_2,
)

print(
    f"OPERACIÓN ABIERTA: "
    f"{open_result_2['opened']}"
)

print(
    f"MOTIVO: "
    f"{open_result_2['reason']}"
)

if not open_result_2["opened"]:
    print()
    print("ERROR: La operación 2 no pudo abrirse.")
    raise SystemExit


trade_2 = open_result_2["trade"]


# ============================================================
# ESTADO OPERACIÓN 2
# ============================================================

print()
print("=" * 70)
print("ESTADO DURANTE OPERACIÓN 2")
print("=" * 70)

risk_status_2 = manager.get_risk_status()

print(
    f"POSICIONES ABIERTAS: "
    f"{risk_status_2['open_positions']}"
)

print(
    f"MÁXIMO PERMITIDO: "
    f"{risk_status_2['max_open_positions']}"
)

print(
    f"PNL DIARIO: "
    f"{risk_status_2['daily_pnl']:.4f} USDT"
)


# ============================================================
# CERRAR OPERACIÓN 2
# ============================================================

exit_price_2 = ENTRY_PRICE_2 * 1.02

print()
print("=" * 70)
print("CERRANDO OPERACIÓN 2 → TAKE PROFIT")
print("=" * 70)

close_result_2 = manager.close_trade(
    trade=trade_2,
    exit_price=exit_price_2,
    exit_reason="TAKE_PROFIT",
    pnl=PROFIT_PNL,
)

print(
    f"RESULTADO: "
    f"{close_result_2['exit_reason']}"
)

print(
    f"PNL: "
    f"{close_result_2['pnl']:.4f} USDT"
)

print(
    f"CAPITAL ACTUAL: "
    f"{manager.get_current_capital():.4f} USDT"
)

print(
    f"NUEVO CAPITAL OPERATIVO: "
    f"{manager.get_operating_capital():.4f} USDT"
)

print(
    f"NUEVO NOMINAL: "
    f"{manager.get_nominal():.4f} USDT"
)

print(
    f"¿PUEDE ABRIR OTRA?: "
    f"{close_result_2['can_open_new_trade']}"
)


# ============================================================
# VALIDACIÓN DESPUÉS DE OPERACIÓN 2
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN DESPUÉS DE OPERACIÓN 2")
print("=" * 70)

expected_capital_2 = 105.00
expected_operating_2 = 13.125
expected_nominal_2 = 131.25

check_2 = [
    abs(manager.get_current_capital() - expected_capital_2) < 0.000001,
    abs(manager.get_operating_capital() - expected_operating_2) < 0.000001,
    abs(manager.get_nominal() - expected_nominal_2) < 0.000001,
]

if all(check_2):
    print("OPERACIÓN 2: OK")
else:
    print("OPERACIÓN 2: ERROR")


# ============================================================
# VALIDACIÓN DEL PNL DIARIO
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN DEL PNL DIARIO")
print("=" * 70)

print(
    f"PNL DIARIO FINAL: "
    f"{manager.risk_manager.daily_pnl:.4f} USDT"
)

expected_daily_pnl = 5.00

if abs(manager.risk_manager.daily_pnl - expected_daily_pnl) < 0.000001:
    print("PNL DIARIO +5.00 USDT: OK")
else:
    print("PNL DIARIO +5.00 USDT: ERROR")


# ============================================================
# VALIDACIÓN DEL BLOQUEO DIARIO
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN DEL BLOQUEO POR OBJETIVO")
print("=" * 70)

daily_target_check = manager.can_open_trade()

print(
    f"PERMITIDA: "
    f"{daily_target_check['allowed']}"
)

print(
    f"MOTIVO: "
    f"{daily_target_check['reason']}"
)

if not daily_target_check["allowed"]:
    print("BLOQUEO POR OBJETIVO +5%: OK")
else:
    print("BLOQUEO POR OBJETIVO +5%: ERROR")


# ============================================================
# VALIDACIÓN FINAL
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN FINAL")
print("=" * 70)

checks = [
    abs(manager.get_current_capital() - 105.00) < 0.000001,
    abs(manager.get_operating_capital() - 13.125) < 0.000001,
    abs(manager.get_nominal() - 131.25) < 0.000001,
    abs(manager.risk_manager.daily_pnl - 5.00) < 0.000001,
    daily_target_check["allowed"] is False,
]

if all(checks):
    print("CICLO DE MÚLTIPLES OPERACIONES: OK")
else:
    print("CICLO DE MÚLTIPLES OPERACIONES: ERROR")


# ============================================================
# FIN
# ============================================================

print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)

print()
print("NO SE ENVIÓ NINGUNA ORDEN REAL.")