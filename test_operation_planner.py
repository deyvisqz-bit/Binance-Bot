from src.operation_planner import build_operation_plan


grid_plan = {
    "valid": True,
    "range_min": 1.5542,
    "range_max": 1.5804,
    "levels": [
        1.5542,
        1.55794286,
        1.56168571,
        1.56542857,
        1.56917143,
        1.57291429,
        1.57665714,
        1.5804,
    ],
    "grid_count": 8,
}


print("=" * 70)
print("PRUEBA DEL PLANIFICADOR DE OPERACIÓN")
print("=" * 70)


for direction in ["LONG", "SHORT"]:

    print()
    print("-" * 70)
    print(f"DIRECCIÓN: {direction}")
    print("-" * 70)

    result = build_operation_plan(
        symbol="XRPUSDT",
        direction=direction,
        current_price=1.5580,
        grid_plan=grid_plan,
        operating_capital=12.5,
        leverage=10,
    )

    print(f"VÁLIDO: {result['valid']}")
    print(f"PAR: {result['symbol']}")
    print(f"DIRECCIÓN: {result['direction']}")
    print(f"PRECIO ENTRADA: {result['entry_price']:.6f}")
    print(f"TAKE PROFIT: {result['take_profit']:.6f}")
    print(f"STOP LOSS: {result['stop_loss']:.6f}")
    print(f"TP %: {result['take_profit_percent'] * 100:.2f}%")
    print(f"SL %: {result['stop_loss_percent'] * 100:.2f}%")
    print(f"CAPITAL OPERATIVO: {result['operating_capital']:.2f} USDT")
    print(f"APALANCAMIENTO: {result['leverage']}x")
    print(f"NOMINAL: {result['notional']:.2f} USDT")
    print(f"GRID: {result['grid_count']} niveles")
    print(f"RANGO: {result['grid_range_min']} → {result['grid_range_max']}")


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)