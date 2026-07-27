import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create ML features for stock price prediction.

    Parameters
    ----------
    df : Company specific stock dataframe

    Returns
    -------
    DataFrame with engineered features
    """

    df = df.copy()

    # ---------------------------------------------------
    # Lag Features
    # ---------------------------------------------------

    df["Close_Lag_1"] = df["Close"].shift(1)
    df["Close_Lag_2"] = df["Close"].shift(2)
    df["Close_Lag_3"] = df["Close"].shift(3)

    # ---------------------------------------------------
    # Moving Averages
    # ---------------------------------------------------

    df["SMA_5"] = SMAIndicator(
        close=df["Close"],
        window=5
    ).sma_indicator()

    df["SMA_10"] = SMAIndicator(
        close=df["Close"],
        window=10
    ).sma_indicator()

    df["SMA_20"] = SMAIndicator(
        close=df["Close"],
        window=20
    ).sma_indicator()

    # ---------------------------------------------------
    # Exponential Moving Average
    # ---------------------------------------------------

    df["EMA_10"] = EMAIndicator(
        close=df["Close"],
        window=10
    ).ema_indicator()

    # ---------------------------------------------------
    # RSI
    # ---------------------------------------------------

    df["RSI_14"] = RSIIndicator(
        close=df["Close"],
        window=14
    ).rsi()

    # ---------------------------------------------------
    # Rolling Statistics
    # ---------------------------------------------------

    df["Volume_Mean_5"] = (
        df["Volume"]
        .rolling(window=5)
        .mean()
    )

    df["Volatility_10"] = (
        df["Close"]
        .rolling(window=10)
        .std()
    )

    # ---------------------------------------------------
    # Target Variable
    # ---------------------------------------------------

    df["Target"] = df["Close"].shift(-1)

    # ---------------------------------------------------
    # Remove rows containing NaN
    # ---------------------------------------------------

    df.dropna(inplace=True)

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df


FEATURE_COLUMNS = [

    "Open",
    "High",
    "Low",
    "Close",
    "Volume",

    "Close_Lag_1",
    "Close_Lag_2",
    "Close_Lag_3",

    "SMA_5",
    "SMA_10",
    "SMA_20",

    "EMA_10",

    "RSI_14",

    "Volume_Mean_5",

    "Volatility_10",

]