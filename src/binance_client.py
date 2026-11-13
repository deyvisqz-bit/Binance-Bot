from binance.client import Client
import pandas as pd


def create_public_client():
    """
    Crea un cliente público de Binance.
    No utiliza API keys.
    """
    return Client(
        requests_params= {"timeout": 10}
    )


def get_futures_klines(
    client,
    symbol,
    interval,
    limit=500
):
    """
    Descarga velas históricas de Binance Futures USDT-M.

    Parámetros:
        symbol: par, por ejemplo BTCUSDT
        interval: intervalo, por ejemplo 4h o 15m
        limit: número de velas

    Devuelve:
        pandas.DataFrame
    """

    klines = client.futures_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )

    columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
        "ignore"
    ]

    df = pd.DataFrame(klines, columns=columns)

    # Convertir tiempo
    df["open_time"] = pd.to_datetime(
        df["open_time"],
        unit="ms"
    )

    df["close_time"] = pd.to_datetime(
        df["close_time"],
        unit="ms"
    )

    # Convertir datos numéricos
    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "quote_asset_volume",
        "taker_buy_base_volume",
        "taker_buy_quote_volume"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


if __name__ == "__main__":

    client = create_public_client()

    symbol = "BTCUSDT"

    # Datos 4H
    df_4h = get_futures_klines(
        client,
        symbol,
        "4h",
        500
    )

    # Datos 15M
    df_15m = get_futures_klines(
        client,
        symbol,
        "15m",
        500
    )

    print("=" * 50)
    print("DATOS DE BINANCE FUTURES")
    print("=" * 50)

    print(f"Par: {symbol}")
    print(f"Velas 4H: {len(df_4h)}")
    print(f"Velas 15M: {len(df_15m)}")

    print("\nÚltimas 5 velas 4H:")
    print(
        df_4h[
            ["open_time", "open", "high", "low", "close", "volume"]
        ].tail()
    )

    print("\nÚltimas 5 velas 15M:")
    print(
        df_15m[
            ["open_time", "open", "high", "low", "close", "volume"]
        ].tail()
    )