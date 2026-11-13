from src.capital_manager import CapitalManager
from src.trade_manager import TradeManager
from src.risk_controlled_trade_manager import RiskControlledTradeManager


# ============================================================
# CONFIGURACIÓN
# ============================================================

INITIAL_CAPITAL = 100.0
OPERATING_PERCENT = 0.125
LEVERAGE = 10

SYMBOL = "BTCUSDT"
ENTRY_PRICE = 83601.85

PROFIT_PNL = 2.50


# ============================================================
# INICIO
# ============================================================

print("=" * 70)
print("PRUEBA DEL CICLO COMPLETO DE GANANCIA")
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
# CONTROL DE RIESGO
# ============================================================

print()
print("=" * 70)
print("CONTROL DE RIESGO ANTES DE ENTRAR")
print("=" * 70)

risk_check = manager.can_open_trade()

print(
    f"PERMITIDA: "
    f"{risk_check['allowed']}"
)

print(
    f"MOTIVO: "
    f"{risk_check['reason']}"
)


if not risk_check["allowed"]:
    print()
    print("ERROR: La operación inicial no fue permitida.")
    raise SystemExit


# ============================================================
# ABRIR LONG
# ============================================================

print()
print("=" * 70)
print("ABRIENDO LONG")
print("=" * 70)

open_result = manager.open_trade(
    symbol=SYMBOL,
    direction="LONG",
    entry_price=ENTRY_PRICE,
)

print(
    f"OPERACIÓN ABIERTA: "
    f"{open_result['opened']}"
)

print(
    f"MOTIVO: "
    f"{open_result['reason']}"
)


if not open_result["opened"]:
    print()
    print("ERROR: La operación no pudo abrirse.")
    raise SystemExit


trade = open_result["trade"]


# ============================================================
# ESTADO DURANTE LA OPERACIÓN
# ============================================================

print()
print("=" * 70)
print("ESTADO DURANTE LA OPERACIÓN")
print("=" * 70)

risk_status = manager.get_risk_status()

print(
    f"POSICIONES ABIERTAS: "
    f"{risk_status['open_positions']}"
)

print(
    f"MÁXIMO PERMITIDO: "
    f"{risk_status['max_open_positions']}"
)

print(
    f"PNL DIARIO: "
    f"{risk_status['daily_pnl']:.4f} USDT"
)


# ============================================================
# CERRAR CON TAKE PROFIT
# ============================================================

exit_price = ENTRY_PRICE * 1.02

print()
print("=" * 70)
print("CERRANDO LONG → TAKE PROFIT")
print("=" * 70)

close_result = manager.close_trade(
    trade=trade,
    exit_price=exit_price,
    exit_reason="TAKE_PROFIT",
    pnl=PROFIT_PNL,
)

print(
    f"RESULTADO: "
    f"{close_result['exit_reason']}"
)

print(
    f"PNL: "
    f"{close_result['pnl']:.4f} USDT"
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
    f"{close_result['can_open_new_trade']}"
)


# ============================================================
# VALIDACIÓN DEL CAPITAL
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN DEL CAPITAL")
print("=" * 70)

expected_capital = 102.50
expected_operating = 12.8125
expected_nominal = 128.125


if abs(
    manager.get_current_capital() - expected_capital
) < 0.000001:
    print("CAPITAL 102.50 USDT: OK")
else:
    print("CAPITAL 102.50 USDT: ERROR")


if abs(
    manager.get_operating_capital() - expected_operating
) < 0.000001:
    print("CAPITAL OPERATIVO 12.8125 USDT: OK")
else:
    print("CAPITAL OPERATIVO 12.8125 USDT: ERROR")


if abs(
    manager.get_nominal() - expected_nominal
) < 0.000001:
    print("NOMINAL 128.125 USDT: OK")
else:
    print("NOMINAL 128.125 USDT: ERROR")


# ============================================================
# VALIDACIÓN DE QUE PUEDE CONTINUAR OPERANDO
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN DESPUÉS DE LA GANANCIA")
print("=" * 70)

risk_check_after_profit = manager.can_open_trade()

print(
    f"PERMITIDA: "
    f"{risk_check_after_profit['allowed']}"
)

print(
    f"MOTIVO: "
    f"{risk_check_after_profit['reason']}"
)


if risk_check_after_profit["allowed"]:
    print("CONTINUAR OPERANDO: OK")
else:
    print("CONTINUAR OPERANDO: ERROR")


# ============================================================
# SIMULAR OBJETIVO DIARIO
# ============================================================

print()
print("=" * 70)
print("SIMULANDO OBJETIVO DIARIO +5%")
print("=" * 70)

manager.risk_manager.daily_pnl = 5.00

daily_target_check = manager.can_open_trade()

print(
    f"PNL DIARIO: "
    f"{manager.risk_manager.daily_pnl:.4f} USDT"
)

print(
    f"PERMITIDA: "
    f"{daily_target_check['allowed']}"
)

print(
    f"MOTIVO: "
    f"{daily_target_check['reason']}"
)


# ============================================================
# VALIDACIÓN DEL BLOQUEO POR OBJETIVO
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN DEL BLOQUEO POR OBJETIVO")
print("=" * 70)

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
    abs(manager.get_current_capital() - 102.50) < 0.000001,
    abs(manager.get_operating_capital() - 12.8125) < 0.000001,
    abs(manager.get_nominal() - 128.125) < 0.000001,
    risk_check_after_profit["allowed"] is True,
    daily_target_check["allowed"] is False,
]

if all(checks):
    print("CICLO COMPLETO DE GANANCIA: OK")
else:
    print("CICLO COMPLETO DE GANANCIA: ERROR")


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)

print()
print("NO SE ENVIÓ NINGUNA ORDEN REAL.")