from typing import Dict


class RiskManager:

    def __init__(
        self,
        initial_capital: float,
        daily_target_percent: float = 0.05,
        daily_loss_limit_percent: float = 0.05,
        max_open_positions: int = 10,
    ):
        if initial_capital <= 0:
            raise ValueError(
                "El capital inicial debe ser mayor que cero."
            )

        if daily_target_percent <= 0:
            raise ValueError(
                "El objetivo diario debe ser mayor que cero."
            )

        if daily_loss_limit_percent <= 0:
            raise ValueError(
                "El límite de pérdida diaria debe ser mayor que cero."
            )

        if max_open_positions <= 0:
            raise ValueError(
                "El máximo de posiciones debe ser mayor que cero."
            )

        self.initial_capital = float(initial_capital)

        self.daily_target_percent = float(
            daily_target_percent
        )

        self.daily_loss_limit_percent = float(
            daily_loss_limit_percent
        )

        self.max_open_positions = int(
            max_open_positions
        )

        self.daily_pnl = 0.0

        self.open_positions = 0

        self.trading_blocked = False

        self.block_reason = ""

    def calculate_daily_target(
        self,
        current_capital: float,
    ) -> float:

        return (
            current_capital
            * self.daily_target_percent
        )

    def calculate_daily_loss_limit(
        self,
        current_capital: float,
    ) -> float:

        return (
            current_capital
            * self.daily_loss_limit_percent
        )

    def register_open_position(self) -> Dict:

        if self.trading_blocked:

            return {
                "allowed": False,
                "reason": self.block_reason,
            }

        if (
            self.open_positions
            >= self.max_open_positions
        ):

            return {
                "allowed": False,
                "reason": (
                    "Máximo de posiciones "
                    "simultáneas alcanzado."
                ),
            }

        self.open_positions += 1

        return {
            "allowed": True,
            "open_positions": self.open_positions,
            "reason": "Posición registrada.",
        }

    def register_closed_position(
        self,
        pnl: float,
        current_capital: float,
    ) -> Dict:

        if self.open_positions > 0:
            self.open_positions -= 1

        self.daily_pnl += float(pnl)

        self._evaluate_daily_limits(
            current_capital=current_capital
        )

        return self.get_status(
            current_capital=current_capital
        )

    def _evaluate_daily_limits(
        self,
        current_capital: float,
    ) -> None:

        daily_target = self.calculate_daily_target(
            self.initial_capital
        )

        daily_loss_limit = self.calculate_daily_loss_limit(
            self.initial_capital
        )

        if self.daily_pnl >= daily_target:

            self.trading_blocked = True

            self.block_reason = (
                "Objetivo diario alcanzado. "
                "No se abrirán nuevas operaciones."
            )

        elif self.daily_pnl <= -daily_loss_limit:

            self.trading_blocked = True

            self.block_reason = (
                "Límite de pérdida diaria alcanzado. "
                "No se abrirán nuevas operaciones."
            )

    def can_open_new_trade(
        self,
        current_capital: float,
    ) -> Dict:

        self._evaluate_daily_limits(
            current_capital=current_capital
        )

        if self.trading_blocked:

            return {
                "allowed": False,
                "reason": self.block_reason,
            }

        if (
            self.open_positions
            >= self.max_open_positions
        ):

            return {
                "allowed": False,
                "reason": (
                    "Máximo de posiciones "
                    "simultáneas alcanzado."
                ),
            }

        return {
            "allowed": True,
            "reason": (
                "El riesgo permite abrir "
                "una nueva operación."
            ),
        }

    def get_status(
        self,
        current_capital: float,
    ) -> Dict:

        daily_target = self.calculate_daily_target(
            current_capital
        )

        daily_loss_limit = self.calculate_daily_loss_limit(
            current_capital
        )

        remaining_target = max(
            daily_target - self.daily_pnl,
            0.0,
        )

        remaining_loss_capacity = max(
            daily_loss_limit + self.daily_pnl,
            0.0,
        )

        return {
            "daily_pnl": self.daily_pnl,
            "daily_target": daily_target,
            "daily_loss_limit": daily_loss_limit,
            "remaining_target": remaining_target,
            "remaining_loss_capacity": (
                remaining_loss_capacity
            ),
            "open_positions": self.open_positions,
            "max_open_positions": (
                self.max_open_positions
            ),
            "trading_blocked": (
                self.trading_blocked
            ),
            "block_reason": self.block_reason,
        }

    def reset_daily(self) -> None:

        self.daily_pnl = 0.0

        self.open_positions = 0

        self.trading_blocked = False

        self.block_reason = ""