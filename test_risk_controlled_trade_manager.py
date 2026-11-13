from src.capital_manager import CapitalManager
from src.trade_manager import TradeManager
from src.risk_controlled_trade_manager import (
    RiskControlledTradeManager,
)


INITIAL_CAPITAL = 100.0
OPERATING_PERCENT = 0.125
LEVERAGE = 10

SYMBOL = "BTCUSDT"
ENTRY_PRICE = 83601.85


print("=" * 70)
print("PRUEBA DEL TRADE MANAGER CON CONTROL DE RIESGO")
print("=" * 70)


# ============================================================
# CAPITAL
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
# RISK CONTROLLED MANAGER
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
    f"{manager.get_current_capital():.4f}"
)

print(
    f"CAPITAL OPERATIVO: "
    f"{manager.get_operating_capital():.4f}"
)

print(
    f"NOMINAL: "
    f"{manager.get_nominal():.4f}"
)


# ============================================================
# COMPROBAR SI SE PUEDE ABRIR
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


# ============================================================
# ABRIR OPERACIÓN
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
# ESTADO DE RIESGO
# ============================================================

print()
print("=" * 70)
print("RIESGO DESPUÉS DE LA ENTRADA")
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
    f"{risk_status['daily_pnl']:.4f}"
)


# ============================================================
# CERRAR CON TAKE PROFIT
# ============================================================

exit_price = ENTRY_PRICE * 1.02

pnl = 2.50


print()
print("=" * 70)
print("CERRANDO LONG → TAKE PROFIT")
print("=" * 70)

close_result = manager.close_trade(
    trade=trade,
    exit_price=exit_price,
    exit_reason="TAKE_PROFIT",
    pnl=pnl,
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
# SIMULAR OBJETIVO DIARIO
# ============================================================

print()
print("=" * 70)
print("SIMULANDO OBJETIVO DIARIO")
print("=" * 70)

manager.risk_manager.daily_pnl = 5.00

risk_check = manager.can_open_trade()

print(
    f"PERMITIDA: "
    f"{risk_check['allowed']}"
)

print(
    f"MOTIVO: "
    f"{risk_check['reason']}"
)


# ============================================================
# VALIDACIÓN
# ============================================================

print()
print("=" * 70)
print("VALIDACIÓN")
print("=" * 70)

if open_result["opened"]:
    print("ENTRADA CONTROLADA POR RIESGO: OK")
else:
    print("ENTRADA CONTROLADA POR RIESGO: ERROR")


if close_result["exit_reason"] == "TAKE_PROFIT":
    print("CIERRE CONTROLADO: OK")
else:
    print("CIERRE CONTROLADO: ERROR")


if (
    abs(
        manager.get_current_capital()
        - 102.50
    )
    < 0.000001
):
    print("CAPITAL ACTUALIZADO: OK")
else:
    print("CAPITAL ACTUALIZADO: ERROR")


if (
    abs(
        manager.get_nominal()
        - 128.125
    )
    < 0.000001
):
    print("NOMINAL DINÁMICO: OK")
else:
    print("NOMINAL DINÁMICO: ERROR")


if not risk_check["allowed"]:
    print("BLOQUEO POR OBJETIVO DIARIO: OK")
else:
    print("BLOQUEO POR OBJETIVO DIARIO: ERROR")


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)

print(
    "NO SE ENVIO NINGUNA ORDEN REAL."
)