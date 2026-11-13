
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class BotStatus:
    running: bool = False
    cycles_completed: int = 0
    trades_opened: int = 0
    trades_closed: int = 0
    last_cycle: str | None = None
    message: str = "Bot preparado"


class BotOrchestrator:
    """
    Coordina el ciclo principal del bot en modo simulación.
    No envía órdenes a Binance.
    """

    def __init__(self, max_pairs: int = 10):
        if max_pairs < 1:
            raise ValueError("max_pairs debe ser mayor que cero.")

        self.max_pairs = max_pairs
        self.status = BotStatus()
        self.open_positions: dict[str, dict[str, Any]] = {}

    def start(self) -> dict:
        self.status.running = True
        self.status.message = "Orquestador iniciado en simulación."

        return self.get_status()

    def process_scan(self, candidates: list[dict]) -> dict:
        if not self.status.running:
            return {
                "valid": False,
                "reason": "El orquestador no está iniciado.",
            }

        selected = candidates[:self.max_pairs]
        decisions = []

        for candidate in selected:
            symbol = candidate.get("symbol")
            direction = candidate.get("direction", "WAIT")

            if not symbol:
                decisions.append({
                    "symbol": None,
                    "decision": "REJECT",
                    "reason": "Candidato sin símbolo.",
                })
                continue

            if direction not in ("LONG", "SHORT"):
                decisions.append({
                    "symbol": symbol,
                    "decision": "WAIT",
                    "reason": candidate.get(
                        "reason",
                        "Sin señal válida.",
                    ),
                })
                continue

            if symbol in self.open_positions:
                decisions.append({
                    "symbol": symbol,
                    "decision": "WAIT",
                    "reason": "Ya existe una posición registrada.",
                })
                continue

            decisions.append({
                "symbol": symbol,
                "decision": "READY_FOR_RISK_CHECK",
                "direction": direction,
                "reason": "Señal pendiente de validación de riesgo.",
            })

        self.status.cycles_completed += 1
        self.status.last_cycle = datetime.now().isoformat(
            timespec="seconds"
        )
        self.status.message = "Escaneo procesado en simulación."

        return {
            "valid": True,
            "mode": "SIMULATION",
            "candidates_received": len(candidates),
            "candidates_processed": len(selected),
            "decisions": decisions,
            "status": self.get_status(),
        }

    def get_status(self) -> dict:
        return {
            "running": self.status.running,
            "cycles_completed": self.status.cycles_completed,
            "trades_opened": self.status.trades_opened,
            "trades_closed": self.status.trades_closed,
            "open_positions": len(self.open_positions),
            "last_cycle": self.status.last_cycle,
            "message": self.status.message,
            "mode": "SIMULATION",
        }

    def stop(self) -> dict:
        self.status.running = False
        self.status.message = "Orquestador detenido."

        return self.get_status()
