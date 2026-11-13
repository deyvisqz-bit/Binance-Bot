import pandas as pd
from ta.volatility import AverageTrueRange


# ============================================================
# CONFIGURACIÓN
# ============================================================

MIN_GRID_LEVELS = 6
DEFAULT_GRID_LEVELS = 8
MAX_GRID_LEVELS = 12

ATR_PERIOD = 14

# Distancia objetivo entre niveles expresada
# como fracción del ATR.
TARGET_ATR_SPACING = 0.75


# ============================================================
# MÉTRICAS DE GRID
# ============================================================

def calculate_grid_metrics(
    df: pd.DataFrame,
    lookback: int = 50,
) -> dict:
    """
    Calcula las métricas necesarias para construir
    una Grid dinámica.

    No ejecuta operaciones.
    """

    minimum_required = max(
        lookback,
        ATR_PERIOD + 5
    )

    if len(df) < minimum_required:
        raise ValueError(
            f"Datos insuficientes. "
            f"Se necesitan al menos {minimum_required} velas."
        )

    data = df.copy()

    # --------------------------------------------------------
    # ATR
    # --------------------------------------------------------

    atr_indicator = AverageTrueRange(
        high=data["high"],
        low=data["low"],
        close=data["close"],
        window=ATR_PERIOD,
    )

    data["atr"] = (
        atr_indicator.average_true_range()
    )

    # --------------------------------------------------------
    # RANGO RECIENTE
    # --------------------------------------------------------

    recent = data.tail(lookback)

    range_low = float(
        recent["low"].min()
    )

    range_high = float(
        recent["high"].max()
    )

    current_price = float(
        data["close"].iloc[-1]
    )

    atr = float(
        data["atr"].iloc[-1]
    )

    # --------------------------------------------------------
    # VALIDACIONES
    # --------------------------------------------------------

    if range_low <= 0:
        raise ValueError(
            "El mínimo del rango debe ser mayor que cero."
        )

    if range_high <= range_low:
        raise ValueError(
            "El máximo del rango debe ser mayor que el mínimo."
        )

    if atr <= 0:
        raise ValueError(
            "ATR inválido o igual a cero."
        )

    # --------------------------------------------------------
    # MÉTRICAS
    # --------------------------------------------------------

    range_size = (
        range_high - range_low
    )

    range_percent = (
        range_size / range_low
    ) * 100

    atr_percent = (
        atr / current_price
    ) * 100

    range_in_atr = (
        range_size / atr
    )

    return {
        "range_low": range_low,
        "range_high": range_high,
        "range_size": range_size,
        "range_percent": range_percent,
        "current_price": current_price,
        "atr": atr,
        "atr_percent": atr_percent,
        "range_in_atr": range_in_atr,
        "lookback": lookback,
    }


# ============================================================
# NÚMERO DINÁMICO DE NIVELES
# ============================================================

def determine_grid_levels(
    range_size: float,
    atr: float,
) -> int:
    """
    Determina automáticamente el número de niveles
    de la Grid según el rango y el ATR.
    """

    if range_size <= 0:
        raise ValueError(
            "El tamaño del rango debe ser mayor que cero."
        )

    if atr <= 0:
        raise ValueError(
            "El ATR debe ser mayor que cero."
        )

    target_spacing = (
        atr * TARGET_ATR_SPACING
    )

    if target_spacing <= 0:
        return DEFAULT_GRID_LEVELS

    number_of_spaces = (
        range_size / target_spacing
    )

    calculated_levels = (
        int(number_of_spaces) + 1
    )

    levels = max(
        MIN_GRID_LEVELS,
        min(
            calculated_levels,
            MAX_GRID_LEVELS
            if "MAX_GRID_LEVELS" in globals()
            else MAX_GRID_LEVELS,
        ),
    )

    return levels


# ============================================================
# GRID ARITMÉTICA
# ============================================================

def generate_arithmetic_grid(
    range_low: float,
    range_high: float,
    levels: int,
) -> list:
    """
    Genera una Grid aritmética.

    Todos los niveles tienen la misma distancia
    absoluta entre sí.
    """

    if levels < 2:
        raise ValueError(
            "La Grid necesita al menos 2 niveles."
        )

    if range_high <= range_low:
        raise ValueError(
            "El máximo debe ser mayor que el mínimo."
        )

    step = (
        range_high - range_low
    ) / (levels - 1)

    grid = []

    for index in range(levels):

        price = (
            range_low
            + (step * index)
        )

        grid.append(
            float(price)
        )

    return grid


# ============================================================
# CONSTRUCCIÓN DINÁMICA
# ============================================================

def build_dynamic_grid(
    df: pd.DataFrame,
    lookback: int = 50,
) -> dict:
    """
    Construye una Grid dinámica completa.

    Flujo:

        Datos
          ↓
        Máximo / mínimo
          ↓
        ATR
          ↓
        Volatilidad
          ↓
        Número de niveles
          ↓
        Grid aritmética
    """

    metrics = calculate_grid_metrics(
        df=df,
        lookback=lookback,
    )

    levels = determine_grid_levels(
        range_size=metrics["range_size"],
        atr=metrics["atr"],
    )

    grid = generate_arithmetic_grid(
        range_low=metrics["range_low"],
        range_high=metrics["range_high"],
        levels=levels,
    )

    spacing = (
        metrics["range_high"]
        - metrics["range_low"]
    ) / (levels - 1)

    return {
        "valid": True,
        "range_low": metrics["range_low"],
        "range_high": metrics["range_high"],
        "range_size": metrics["range_size"],
        "range_percent": metrics["range_percent"],
        "current_price": metrics["current_price"],
        "atr": metrics["atr"],
        "atr_percent": metrics["atr_percent"],
        "range_in_atr": metrics["range_in_atr"],
        "levels": levels,
        "grid_levels": levels,
        "grid": grid,
        "spacing": spacing,
        "lookback": lookback,
        "target_atr_spacing": TARGET_ATR_SPACING,
    }


# ============================================================
# DIRECCIÓN DE LA GRID
# ============================================================

def determine_grid_side(
    direction: str,
) -> dict:
    """
    Traduce la dirección de la operación
    al lado correspondiente.

    LONG  -> BUY
    SHORT -> SELL
    WAIT  -> inválido
    """

    if not isinstance(direction, str):
        return {
            "valid": False,
            "side": None,
            "reason": "La dirección debe ser un texto.",
        }

    direction = direction.upper().strip()

    if direction == "LONG":
        return {
            "valid": True,
            "side": "BUY",
            "reason": "LONG utiliza lado BUY.",
        }

    if direction == "SHORT":
        return {
            "valid": True,
            "side": "SELL",
            "reason": "SHORT utiliza lado SELL.",
        }

    if direction == "WAIT":
        return {
            "valid": False,
            "side": None,
            "reason": "WAIT no permite construir una operación.",
        }

    return {
        "valid": False,
        "side": None,
        "reason": (
            f"Dirección no reconocida: {direction}"
        ),
    }


# ============================================================
# COMPATIBILIDAD CON EL PLANIFICADOR ANTIGUO
# ============================================================

def build_grid_plan(
    direction: str,
    range_low: float = 1.0,
    range_high: float = 2.0,
    levels: int = DEFAULT_GRID_LEVELS,
    **kwargs,
) -> dict:
    """
    Construye un plan básico de Grid para LONG, SHORT o WAIT.

    Esta función mantiene compatibilidad con los tests
    y módulos anteriores del proyecto.

    No ejecuta órdenes.
    """

    direction = direction.upper().strip()

    side_result = determine_grid_side(
        direction
    )

    if not side_result["valid"]:
        return {
            "valid": False,
            "direction": direction,
            "side": None,
            "range_low": range_low,
            "range_high": range_high,
            "levels": 0,
            "grid_levels": [],
            "spacing": 0.0,
            "reason": side_result["reason"],
        }

    if range_high <= range_low:
        return {
            "valid": False,
            "direction": direction,
            "side": side_result["side"],
            "range_low": range_low,
            "range_high": range_high,
            "levels": 0,
            "grid_levels": [],
            "spacing": 0.0,
            "reason": (
                "El máximo del rango debe ser "
                "mayor que el mínimo."
            ),
        }

    if levels < 2:
        return {
            "valid": False,
            "direction": direction,
            "side": side_result["side"],
            "range_low": range_low,
            "range_high": range_high,
            "levels": 0,
            "grid_levels": [],
            "spacing": 0.0,
            "reason": (
                "La Grid necesita al menos "
                "2 niveles."
            ),
        }

    grid = generate_arithmetic_grid(
        range_low=range_low,
        range_high=range_high,
        levels=levels,
    )

    spacing = (
        range_high - range_low
    ) / (levels - 1)

    return {
        "valid": True,
        "direction": direction,
        "side": side_result["side"],
        "range_low": float(range_low),
        "range_high": float(range_high),
        "levels": levels,
        "grid_levels": grid,
        "spacing": float(spacing),
        "reason": (
            f"Plan Grid {direction} construido correctamente."
        ),
    }