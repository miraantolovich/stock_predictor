import numpy as np

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
    total_price = 0

    # get adjusted close
    for row in data:
        date = row[0]
        adjusted_close = row[1]
        total_price += adjusted_close
        print(date, adjusted_close)

    return total_price/days


# data will be the last ? days/? days depending
def calculate_ema(data, smoothing=2, days=26):
    multiplier = smoothing / (days + 1)

    ema = []
    ema.append(data[0])  # Initial EMA is the same as the first data point

    for i in range(1, len(data)):
        current_ema = (data[i] - ema[i-1]) * multiplier + ema[i-1]
        ema.append(current_ema)

    return ema


def calculate_bb(data, std=2):
    middle = np.mean(data)

    std_value = np.std(data)

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

    delta = deltas[-1]
    if delta > 0:
        avg_gain = (avg_gain * (days - 1) + delta) / days
        avg_loss = (avg_loss * (days - 1)) / days
    else:
        avg_gain = (avg_gain * (days - 1)) / days
        avg_loss = (avg_loss * (days - 1) - delta) / days

    rs_value = np.divide(avg_gain, avg_loss, where=avg_loss!=0)
    rsi_value = 100 - (100 / (1 + rs_value))

    return rsi_value


def calculate_percent_r(data, days=14):
    highest_high = np.max(data[:days])
    lowest_low = np.min(data[:days])

    current_close = data[-1]
    percent_r = ((highest_high - current_close) / (highest_high - lowest_low)) * -100

    return percent_r


def calculate_so(data, days=14, smoothing=2):
    highs = data[:, 0]
    lows = data[:, 1]

    lowest_low = np.min(lows[-days:])
    highest_high = np.max(highs[-days:])

    current_close = data[-1, 3]

    p_k = ((current_close - lowest_low) / (highest_high - lowest_low)) * 100
    p_d = np.mean(p_k[-smoothing:])

    return p_k, p_d


def calculate_momentum(data, days=14):
    prices = data[-days:]  # Extract the last 'periods' number of prices
    momentum = prices[-1] - prices[0]  # Calculate the difference between the current price and the price 'n' periods ago

    return momentum

# endregion
# endregion