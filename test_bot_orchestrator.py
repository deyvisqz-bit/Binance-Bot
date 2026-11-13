
from src.bot_orchestrator import BotOrchestrator


bot = BotOrchestrator(max_pairs=10)

print("INICIANDO ORQUESTADOR")
print(bot.start())

print("\nPROCESANDO ESCANEO SIMULADO")

candidates = [
    {
        "symbol": "BTCUSDT",
        "direction": "LONG",
        "reason": "Señal de prueba",
    },
    {
        "symbol": "ETHUSDT",
        "direction": "WAIT",
        "reason": "Marcos temporales no alineados",
    },
    {
        "symbol": "SOLUSDT",
        "direction": "SHORT",
        "reason": "Señal de prueba",
    },
]

result = bot.process_scan(candidates)

for decision in result["decisions"]:
    print(decision)

print("\nESTADO FINAL")
print(bot.get_status())

assert result["valid"] is True
assert result["candidates_processed"] == 3
assert result["decisions"][0]["decision"] == "READY_FOR_RISK_CHECK"
assert result["decisions"][1]["decision"] == "WAIT"
assert result["decisions"][2]["decision"] == "READY_FOR_RISK_CHECK"
assert bot.status.cycles_completed == 1

print("\nORQUESTADOR: PRUEBA CORRECTA")
print("No se enviaron órdenes reales.")
