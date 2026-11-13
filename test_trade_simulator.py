from src.trade_simulator import simulate_trade


ENTRY = 83601.85
NOMINAL = 125.0


print("=" * 70)
print("SIMULADOR DEL CICLO DE VIDA DE UNA OPERACIÓN")
print("=" * 70)

print()
print("CONFIGURACIÓN")
print("-" * 70)
print(f"ENTRADA: {ENTRY}")
print("NOMINAL: 125.00 USDT")
print("TP: +2%")
print("SL: -5%")
print("ÓRDENES REALES: DESACTIVADAS")


print()
print("=" * 70)
print("PRUEBA 1: LONG CON TAKE PROFIT")
print("=" * 70)

long_tp_path = [
    83650,
    83750,
    84000,
    84500,
    85000,
    85280,
]

result = simulate_trade(
    entry_price=ENTRY,
    direction="LONG",
    nominal=NOMINAL,
    price_path=long_tp_path,
)

print(f"DIRECCIÓN: {result['direction']}")
print(f"ENTRADA: {result['entry_price']}")
print(f"SALIDA: {result['exit_price']}")
print(f"RESULTADO: {result['exit_reason']}")
print(f"PNL: {result['pnl']:.4f} USDT")
print(f"VELAS MONITOREADAS: {result['candles_monitored']}")

if result["exit_reason"] == "TAKE_PROFIT":
    print("LONG TP: OK")
else:
    print("LONG TP: ERROR")


print()
print("=" * 70)
print("PRUEBA 2: LONG CON STOP LOSS")
print("=" * 70)

long_sl_path = [
    83500,
    83000,
    82000,
    81000,
    80000,
    79000,
]

result = simulate_trade(
    entry_price=ENTRY,
    direction="LONG",
    nominal=NOMINAL,
    price_path=long_sl_path,
)

print(f"DIRECCIÓN: {result['direction']}")
print(f"ENTRADA: {result['entry_price']}")
print(f"SALIDA: {result['exit_price']}")
print(f"RESULTADO: {result['exit_reason']}")
print(f"PNL: {result['pnl']:.4f} USDT")
print(f"VELAS MONITOREADAS: {result['candles_monitored']}")

if result["exit_reason"] == "STOP_LOSS":
    print("LONG SL: OK")
else:
    print("LONG SL: ERROR")


print()
print("=" * 70)
print("PRUEBA 3: SHORT CON TAKE PROFIT")
print("=" * 70)

short_tp_path = [
    83500,
    83000,
    82800,
    82500,
    82000,
    81900,
]

result = simulate_trade(
    entry_price=ENTRY,
    direction="SHORT",
    nominal=NOMINAL,
    price_path=short_tp_path,
)

print(f"DIRECCIÓN: {result['direction']}")
print(f"ENTRADA: {result['entry_price']}")
print(f"SALIDA: {result['exit_price']}")
print(f"RESULTADO: {result['exit_reason']}")
print(f"PNL: {result['pnl']:.4f} USDT")
print(f"VELAS MONITOREADAS: {result['candles_monitored']}")

if result["exit_reason"] == "TAKE_PROFIT":
    print("SHORT TP: OK")
else:
    print("SHORT TP: ERROR")


print()
print("=" * 70)
print("PRUEBA 4: SHORT CON STOP LOSS")
print("=" * 70)

short_sl_path = [
    83800,
    84500,
    85000,
    86000,
    87000,
    87800,
]

result = simulate_trade(
    entry_price=ENTRY,
    direction="SHORT",
    nominal=NOMINAL,
    price_path=short_sl_path,
)

print(f"DIRECCIÓN: {result['direction']}")
print(f"ENTRADA: {result['entry_price']}")
print(f"SALIDA: {result['exit_price']}")
print(f"RESULTADO: {result['exit_reason']}")
print(f"PNL: {result['pnl']:.4f} USDT")
print(f"VELAS MONITOREADAS: {result['candles_monitored']}")

if result["exit_reason"] == "STOP_LOSS":
    print("SHORT SL: OK")
else:
    print("SHORT SL: ERROR")


print()
print("=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)
print("NO SE ENVIÓ NINGUNA ORDEN A BINANCE.")
print("NO SE ABRIÓ NINGUNA POSICIÓN REAL.")