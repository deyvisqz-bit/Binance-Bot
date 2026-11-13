# Configuración principal del Binance Futures Bot - V1

# Capital
INITIAL_CAPITAL = 100.0
OPERATING_CAPITAL_PERCENT = 0.125

# Trading
LEVERAGE = 10
MAX_PAIRS = 10

# Grid
GRID_LEVELS = 30

# Riesgo por operación
TAKE_PROFIT_PERCENT = 0.02
STOP_LOSS_PERCENT = 0.05

# Objetivo y límite diario
DAILY_TARGET_PERCENT = 0.05
DAILY_LOSS_LIMIT_PERCENT = 0.05

# Timeframes
TREND_TIMEFRAME = "4h"
ENTRY_TIMEFRAME = "15m"

# Indicadores
EMA_FAST = 50
EMA_SLOW = 200
ADX_PERIOD = 14
ATR_PERIOD = 14

# Umbral inicial del ADX
ADX_THRESHOLD = 25

# Mercado
MARKET_TYPE = "USDT-M"
MARGIN_TYPE = "ISOLATED"

# Dirección permitida
ALLOW_LONG = True
ALLOW_SHORT = True

# Número máximo de operaciones simultáneas
MAX_OPEN_POSITIONS = 10