from typing import Dict, Optional

from src.capital_manager import CapitalManager


class TradeManager:

    def __init__(
        self,
        initial_capital: float,
        operating_capital_percent: float = 0.125,
        leverage: int = 10,
        capital_manager: Optional[CapitalManager] = None,
    ):
        if capital_manager is not None:
            self.capital_manager = capital_manager
        else:
            self.capital_manager = CapitalManager(
                initial_capital=initial_capital,
                operating_capital_percent=operating_capital_percent,
                leverage=leverage,
            )

        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0

        self.daily_pnl = 0.0

    def get_current_capital(self) -> float:
        return self.capital_manager.current_capital

    def get_operating_capital(self) -> float:
        return self.capital_manager.calculate_operating_capital()

    def get_nominal(self) -> float:
        return self.capital_manager.calculate_nominal()

    def open_trade(
        self,
        symbol: str,
        direction: str,
        entry_price: float,
        nominal: Optional[float] = None,
    ) -> Dict:

        if direction not in ("LONG", "SHORT"):
            return {
                "valid": False,
                "reason": "Dirección inválida.",
            }

        if entry_price <= 0:
            return {
                "valid": False,
                "reason": "Precio de entrada inválido.",
            }

        if nominal is None:
            nominal = self.get_nominal()

        if nominal <= 0:
            return {
                "valid": False,
                "reason": "Nominal inválido.",
            }

        return {
            "valid": True,
            "status": "OPEN",
            "symbol": symbol,
            "direction": direction,
            "entry_price": float(entry_price),
            "nominal": float(nominal),
            "capital_before": self.get_current_capital(),
            "operating_capital": self.get_operating_capital(),
            "leverage": self.capital_manager.leverage,
        }

    def close_trade(
        self,
        trade: Dict,
        exit_price: float,
        exit_reason: str,
        pnl: float,
    ) -> Dict:

        if not trade.get("valid"):
            return {
                "valid": False,
                "reason": "La operación no es válida.",
            }

        if exit_price <= 0:
            return {
                "valid": False,
                "reason": "Precio de salida inválido.",
            }

        if exit_reason not in (
            "TAKE_PROFIT",
            "STOP_LOSS",
            "MANUAL",
        ):
            return {
                "valid": False,
                "reason": "Motivo de cierre inválido.",
            }

        capital_before = self.get_current_capital()

        capital_update = self.capital_manager.update_capital(
            pnl=pnl
        )

        self.daily_pnl += pnl
        self.total_trades += 1

        if pnl > 0:
            self.winning_trades += 1

        elif pnl < 0:
            self.losing_trades += 1

        return {
            "valid": True,
            "status": "CLOSED",
            "symbol": trade["symbol"],
            "direction": trade["direction"],
            "entry_price": trade["entry_price"],
            "exit_price": float(exit_price),
            "exit_reason": exit_reason,
            "pnl": float(pnl),
            "capital_before": capital_before,
            "capital_after": capital_update["capital_after"],
            "operating_capital_after": (
                capital_update["operating_capital"]
            ),
            "nominal_after": capital_update["nominal"],
            "daily_pnl": self.daily_pnl,
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
        }

    def get_statistics(self) -> Dict:

        if self.total_trades > 0:
            win_rate = (
                self.winning_trades
                / self.total_trades
            ) * 100
        else:
            win_rate = 0.0

        initial_capital = (
            self.capital_manager.initial_capital
        )

        current_capital = (
            self.capital_manager.current_capital
        )

        capital_change = (
            current_capital - initial_capital
        )

        capital_change_percent = (
            capital_change / initial_capital
        ) * 100

        return {
            "initial_capital": initial_capital,
            "current_capital": current_capital,
            "operating_capital": self.get_operating_capital(),
            "nominal": self.get_nominal(),
            "capital_change": capital_change,
            "capital_change_percent": capital_change_percent,
            "daily_pnl": self.daily_pnl,
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": win_rate,
        }