# region Imports
import requests
import pandas as pd
import time
import schedule
from datetime import date

import yahoo_fin.options as ops
import yahoo_fin.stock_info as sti
# endregion

# region Variables

# medium (monthly plays) to medium/large-cap stocks
# analyst rating
# insider trading/purchases

# get list of all stocks to compare
stock_list = ["AAPL", "GOOG"]

symbol = "AAPL"
# endregion

# api_key = "D24NAEA1UVN44M2E"
#
# url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
#
# response = requests.get(url)
#
# if response.status_code == 200:
#     data = response.json()
#     print(data)
#     print(data['Time Series (Daily)'])
# else:
#     print("Error occurred while retrieving stock information.")
# pd.set_option('display.max_columns', None)
#
# stock_data = sti.get_data(symbol, start_date="01/01/2019")
# print(stock_data)

# expiration_dates = ops.get_expiration_dates("aapl")
# print(expiration_dates)
# 
# get_calls = ops.get_calls("aapl")
# print(get_calls)
# 
# get_calls = ops.get_puts("aapl")
# print(get_calls)

# get_all = ops.get_options_chain("aapl")
# print(get_all)
#
# get_analyst = sti.get_analysts_info("aapl")
# print(get_analyst)

# pull once a day, 8pm est

# region Pulling Stock Data Methods
def pull_daily():
    for stock in stock_list:
        # pull stock data:
        # open, high, low, close, adjusted close, volume
        # options chain

        start_date = date.today.strftime("%m/%d/%y")
        stock_data = sti.get_data(stock, start_date)
        print(stock_data)

        get_all = ops.get_options_chain(stock)
        print(get_all)


    # put all into database
    print("Daily pull done")
    return


# pull once every 3 months?
def pull_analyst():
    for stock in stock_list:
        get_analyst = sti.get_analysts_info(stock)
        print(get_analyst)


def pull_all():

    # check if any data exists in database

    for stock in stock_list:
        # options, analyst ratings not available for past

        stock_data = sti.get_data(stock, start_date="01/01/2019")
        print(stock_data)

        # calculate SMA, EMA, BB, RSI, %R, SO, M

        # store all the data to SQL
        return
# endregion

# region Indicators
# calculate once a day, after pull_daily
def calculate_daily_indicators():
    # calculate SMA, EMA, BB... RSI, %R, SO, M after daily pull
    return


def calculate_all_indicators():
    # calculate SMA, EMA, BB... RSI, %R, SO, M after all data is pulled
    return


# region Individual Indicators
def calculate_sma():
    return


def calculate_ema():
    return


def calculate_bb():
    return


def calculate_rsi():
    return


def calculate_percent_r():
    return


def calculate_so():
    return


def calculate_momentum():
    return
# endregion
# endregion