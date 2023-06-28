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
def calculate_sma(data, days=200):
    total_price = data.rolling(window=days).mean()
    return total_price


# data will be the last ? days/? days depending
def calculate_ema(data, smooth=0.2):
    ema = data.ewm(com=smooth).mean()

    return ema


def calculate_bb(data, window=20, std=2):
    middle = data.rolling(window=window).mean()

    std_value = data.rolling(window=window).std()

    upper = middle + std * std_value
    lower = middle - std * std_value

    return upper, lower


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

    current_close = data.iloc[-1]
    percent_r = ((highest_high - current_close) / (highest_high - lowest_low)) * -100

    result_df = pd.DataFrame({'percent_r': percent_r})
    return result_df


def calculate_so(data, days=14, smoothing=2):
    highs = data['high_price']
    lows = data['low_price']
    closes = data['adjusted_close_price']

    lowest_low = lows.rolling(window=days, min_periods=1).min()
    highest_high = highs.rolling(window=days, min_periods=1).max()

    p_k = ((closes - lowest_low) / (highest_high - lowest_low)) * 100
    p_d = p_k.rolling(window=smoothing).mean()

    so = pd.DataFrame({'p_k': p_k, 'p_d': p_d})

    so['p_k'].iloc[:days] = np.nan
    so['p_d'].iloc[:days] = np.nan

    return so


def calculate_momentum(data, days=14):
    prices = data[-days:]  # Extract the last 'periods' number of prices
    momentum = prices[-1] - prices[0]  # Calculate the difference between the current price and the price 'n' periods ago

    return momentum

# endregion
# endregion