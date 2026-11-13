from typing import Dict


class CapitalManager:

    def __init__(
        self,
        initial_capital: float,
        operating_capital_percent: float = 0.125,
        leverage: int = 10,
    ):
        if initial_capital <= 0:
            raise ValueError(
                "El capital inicial debe ser mayor que cero."
            )

        if operating_capital_percent <= 0:
            raise ValueError(
                "El porcentaje de capital operativo debe ser mayor que cero."
            )

        if operating_capital_percent > 1:
            raise ValueError(
                "El porcentaje de capital operativo debe estar entre 0 y 1."
            )

        if leverage <= 0:
            raise ValueError(
                "El apalancamiento debe ser mayor que cero."
            )

        self.initial_capital = float(initial_capital)
        self.current_capital = float(initial_capital)
        self.operating_capital_percent = float(
            operating_capital_percent
        )
        self.leverage = int(leverage)

    def calculate_operating_capital(self) -> float:
        return (
            self.current_capital
            * self.operating_capital_percent
        )

    def calculate_nominal(self) -> float:
        operating_capital = (
            self.calculate_operating_capital()
        )

        return operating_capital * self.leverage

    def update_capital(self, pnl: float) -> Dict:

        capital_before = self.current_capital

        self.current_capital += float(pnl)

        if self.current_capital <= 0:
            self.current_capital = 0.0

        operating_capital = (
            self.calculate_operating_capital()
        )

        nominal = self.calculate_nominal()

        return {
            "capital_before": capital_before,
            "pnl": float(pnl),
            "capital_after": self.current_capital,
            "operating_capital": operating_capital,
            "operating_capital_percent": (
                self.operating_capital_percent
            ),
            "leverage": self.leverage,
            "nominal": nominal,
        }

    def get_state(self) -> Dict:

        operating_capital = (
            self.calculate_operating_capital()
        )

        nominal = self.calculate_nominal()

        return {
            "initial_capital": self.initial_capital,
            "current_capital": self.current_capital,
            "operating_capital": operating_capital,
            "operating_capital_percent": (
                self.operating_capital_percent
            ),
            "leverage": self.leverage,
            "nominal": nominal,
        }