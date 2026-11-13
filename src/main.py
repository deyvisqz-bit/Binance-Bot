from config import (
    INITIAL_CAPITAL,
    OPERATING_CAPITAL_PERCENT,
    LEVERAGE,
    MAX_PAIRS,
    GRID_LEVELS,
    TREND_TIMEFRAME,
    ENTRY_TIMEFRAME,
)


def main():
    print("=" * 50)
    print("BINANCE FUTURES BOT - V1")
    print("=" * 50)

    print(f"Capital inicial: {INITIAL_CAPITAL:.2f} USDT")
    print(f"Capital operativo: {OPERATING_CAPITAL_PERCENT * 100:.1f}%")
    print(f"Apalancamiento: {LEVERAGE}x")
    print(f"Máximo de pares: {MAX_PAIRS}")
    print(f"Niveles de Grid: {GRID_LEVELS}")
    print(f"Marco de tendencia: {TREND_TIMEFRAME}")
    print(f"Marco de entrada: {ENTRY_TIMEFRAME}")

    operating_capital = INITIAL_CAPITAL * OPERATING_CAPITAL_PERCENT

    print(f"Capital operativo actual: {operating_capital:.3f} USDT")
    print("=" * 50)
    print("Configuración cargada correctamente.")


if __name__ == "__main__":
    main()