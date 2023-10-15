import numpy as np
import pandas as pd

# region Indicators
# calculate once a day, after pull_daily
def calculate_daily_indicators():
    # calculate SMA, EMA, BB... RSI, %R, SO, M after daily pull
    return


def calculate_all_indicators():
    # calculate SMA, EMA, BB... RSI, %R, SO, M after all data is pulled
    return


# region Individual Indicators

# data will be the last 200 days/50 days (good for long term)
def calculate_sma(data, days=50):
    sma = data.rolling(window=days).mean()
    sma_dataframe = pd.DataFrame(sma)
    sma_dataframe = sma_dataframe.rename(columns={'adjusted_close_price': 'sma'})
    return sma_dataframe


# data will be the last ? days/? days depending
def calculate_ema(data, smooth=0.2, days=26):
    ema = data.ewm(com=smooth).mean()

    ema_dataframe = pd.DataFrame(ema)
    ema_dataframe = ema_dataframe.rename(columns={'adjusted_close_price': 'ema'})

    return ema_dataframe


def calculate_bb(data, window=20, std=2):
    middle = data.rolling(window=window).mean()

    std_value = data.rolling(window=window).std()

    upper = middle + (std * std_value)
    lower = middle - (std * std_value)

    bb_dataframe = pd.DataFrame(middle)
    bb_dataframe = bb_dataframe.rename(columns={'adjusted_close_price': 'bb_middle'})
    bb_dataframe = bb_dataframe.join(lower)
    bb_dataframe = bb_dataframe.rename(columns={'adjusted_close_price': 'bb_lower'})
    bb_dataframe = bb_dataframe.join(upper)
    bb_dataframe = bb_dataframe.rename(columns={'adjusted_close_price': 'bb_upper'})

    return bb_dataframe


def calculate_rsi(data, days=14):
    deltas = np.diff(data)
    up_values = deltas.copy()
    down_values = deltas.copy()
    up_values[up_values < 0] = 0
    down_values[down_values > 0] = 0

    avg_gain = np.mean(up_values[:days])
    avg_loss = -np.mean(down_values[:days])

    rsi = []

    for i in range(0, len(data)):

        if (i < days):
            rsi.append(np.NaN)
            continue

        delta = deltas[i - 1]

        if delta > 0:
            avg_gain = (avg_gain * (days - 1) + delta) / days
            avg_loss = (avg_loss * (days - 1)) / days
        else:
            avg_gain = (avg_gain * (days - 1)) / days
            avg_loss = (avg_loss * (days - 1) - delta) / days

        rs_value = np.divide(avg_gain, avg_loss, where=avg_loss != 0)
        rsi_value = 100 - (100 / (1 + rs_value))

        rsi.append(rsi_value)

    rsi = pd.DataFrame({'rsi': rsi})

    return rsi



def calculate_percent_r(data, days=14):
    highest_high = data.rolling(window=days).max()
    lowest_low = data.rolling(window=days).min()

    percent_r = ((highest_high - data) / (highest_high - lowest_low)) * -100

    result_df = pd.DataFrame({'percent_r': percent_r})

    return result_df


def calculate_so(data, days=14, smoothing=2):

    lowest_low = data.rolling(window=days, min_periods=1).min()
    highest_high = data.rolling(window=days, min_periods=1).max()

    p_k = ((data - lowest_low) / (highest_high - lowest_low)) * 100
    p_d = p_k.rolling(window=days).mean()

    # print(p_k)
    # print(p_d)
    so = pd.DataFrame({'p_k': p_k, 'p_d': p_d})

    so['p_k'].iloc[:days] = np.nan
    so['p_d'].iloc[:days] = np.nan

    return so


def calculate_roc(data, days=14):
    roc_values = []
    df = pd.DataFrame(data)  # Convert the data to a DataFrame
    roc_series = pd.Series(roc_values)

    for i in range(0, days):
        roc_series = roc_series.append(pd.Series(np.nan))

    for i in range(days, len(df)):
        prices = df.iloc[i - days: i]  # Extract 'days' number of prices
        roc = prices.iloc[-1] - prices.iloc[0]  # Calculate the difference between the current price and the price 'days' ago
        roc_series = roc_series.append(pd.Series(roc))

    roc_series.index = np.arange(len(roc_series))  # Reset the index
    roc_df = pd.DataFrame(roc_series, columns=['roc'])  # Convert roc_series to DataFrame

    return roc_df

# endregion
