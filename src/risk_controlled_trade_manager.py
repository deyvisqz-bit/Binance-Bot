from src.risk_manager import RiskManager


class RiskControlledTradeManager:

    def __init__(
        self,
        trade_manager,
        initial_capital: float,
        daily_target_percent: float = 0.05,
        daily_loss_limit_percent: float = 0.05,
        max_open_positions: int = 10,
    ):

        self.trade_manager = trade_manager

        self.risk_manager = RiskManager(
            initial_capital=initial_capital,
            daily_target_percent=daily_target_percent,
            daily_loss_limit_percent=daily_loss_limit_percent,
            max_open_positions=max_open_positions,
        )

    def get_current_capital(self) -> float:

        return self.trade_manager.get_current_capital()

    def get_operating_capital(self) -> float:

        return self.trade_manager.get_operating_capital()

    def get_nominal(self) -> float:

        return self.trade_manager.get_nominal()

    def can_open_trade(self) -> dict:

        current_capital = (
            self.get_current_capital()
        )

        return self.risk_manager.can_open_new_trade(
            current_capital=current_capital
        )

    def open_trade(
        self,
        symbol: str,
        direction: str,
        entry_price: float,
    ) -> dict:

        risk_check = self.can_open_trade()

        if not risk_check["allowed"]:

            return {
                "allowed": False,
                "opened": False,
                "reason": risk_check["reason"],
            }

        risk_registration = (
            self.risk_manager
            .register_open_position()
        )

        if not risk_registration["allowed"]:

            return {
                "allowed": False,
                "opened": False,
                "reason": risk_registration["reason"],
            }

        trade = self.trade_manager.open_trade(
            symbol=symbol,
            direction=direction,
            entry_price=entry_price,
            nominal=self.get_nominal(),
        )

        return {
            "allowed": True,
            "opened": True,
            "trade": trade,
            "reason": "Operación abierta correctamente.",
        }

    def close_trade(
        self,
        trade: dict,
        exit_price: float,
        exit_reason: str,
        pnl: float,
    ) -> dict:

        result = self.trade_manager.close_trade(
            trade=trade,
            exit_price=exit_price,
            exit_reason=exit_reason,
            pnl=pnl,
        )

        current_capital = (
            self.get_current_capital()
        )

        risk_status = (
            self.risk_manager
            .register_closed_position(
                pnl=pnl,
                current_capital=current_capital,
            )
        )

        result["risk_status"] = risk_status

        result["can_open_new_trade"] = (
            risk_status["trading_blocked"] is False
            and risk_status["open_positions"]
            < risk_status["max_open_positions"]
        )

        return result

    def get_risk_status(self) -> dict:

        return self.risk_manager.get_status(
            current_capital=self.get_current_capital()
        )

    def reset_daily_risk(self) -> None:

        self.risk_manager.reset_daily()