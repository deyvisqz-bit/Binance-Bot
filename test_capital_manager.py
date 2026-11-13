from src.capital_manager import CapitalManager


INITIAL_CAPITAL = 100.0
OPERATING_PERCENT = 0.125
LEVERAGE = 10


print("=" * 70)
print("PRUEBA DEL CAPITAL DINÁMICO")
print("=" * 70)


manager = CapitalManager(
    initial_capital=INITIAL_CAPITAL,
    operating_capital_percent=OPERATING_PERCENT,
    leverage=LEVERAGE,
)


print()
print("ESTADO INICIAL")
print("-" * 70)

state = manager.get_state()

print(
    f"CAPITAL TOTAL: "
    f"{state['current_capital']:.4f} USDT"
)

print(
    f"CAPITAL OPERATIVO: "
    f"{state['operating_capital']:.4f} USDT"
)

print(
    f"NOMINAL: "
    f"{state['nominal']:.4f} USDT"
)


print()
print("=" * 70)
print("DESPUÉS DE GANAR +2.50 USDT")
print("=" * 70)

result = manager.update_capital(
    pnl=2.50
)

print(
    f"CAPITAL TOTAL: "
    f"{result['capital_after']:.4f} USDT"
)

print(
    f"CAPITAL OPERATIVO: "
    f"{result['operating_capital']:.4f} USDT"
)

print(
    f"NOMINAL: "
    f"{result['nominal']:.4f} USDT"
)


print()
print("=" * 70)
print("DESPUÉS DE PERDER -6.25 USDT")
print("=" * 70)

result = manager.update_capital(
    pnl=-6.25
)

print(
    f"CAPITAL TOTAL: "
    f"{result['capital_after']:.4f} USDT"
)

print(
    f"CAPITAL OPERATIVO: "
    f"{result['operating_capital']:.4f} USDT"
)

print(
    f"NOMINAL: "
    f"{result['nominal']:.4f} USDT"
)


print()
print("=" * 70)
print("VALIDACIÓN")
print("=" * 70)

expected_capital = 96.25
expected_operating = 12.03125
expected_nominal = 120.3125

if abs(
    manager.current_capital - expected_capital
) < 0.000001:

    print("CAPITAL DINÁMICO: OK")

else:

    print("CAPITAL DINÁMICO: ERROR")


if abs(
    manager.calculate_operating_capital()
    - expected_operating
) < 0.000001:

    print("CAPITAL OPERATIVO: OK")

else:

    print("CAPITAL OPERATIVO: ERROR")


if abs(
    manager.calculate_nominal()
    - expected_nominal
) < 0.000001:

    print("NOMINAL DINÁMICO: OK")

else:

    print("NOMINAL DINÁMICO: ERROR")


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)