# region Imports
import requests
import pandas as pd
import time
import schedule
from datetime import date, timedelta

import yahoo_fin.options as ops
import yahoo_fin.stock_info as sti

import pyodbc
# endregion

# region Variables
pd.set_option('display.max_columns', None)
# medium (monthly plays) to medium/large-cap stocks
# analyst rating
# insider trading/purchases

# get list of all stocks to compare
# INTC (large), CWH (small-med), GBX (small), SOFI (medium), SUZ (medium), AAL (medium)
stock_list = ["INTC"]
# stock_list = ["INTC", "CWH", "GBX", "SOFI", "SUZ", "AAL"]
# endregion

# region Set Up Database Connection
server = 'localhost'
database = 'Stock_Information'
username = 'python_access'
password = 'admin 123!'
driver = 'ODBC Driver 17 for SQL Server'

# conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# conn = pyodbc.connect(conn_str)
# cursor = conn.cursor()

# cursor.execute('SELECT * FROM Stock')
# rows = cursor.fetchall()

# print("connected!")
# for row in rows:
#     print(row)


# cursor.close()
# conn.close()
# endregion


# pull once a day, 8pm est
# region Pulling Stock Data Methods
def pull_daily():
    for stock in stock_list:
        # pull stock data:
        # open, high, low, close, adjusted close, volume
        # options chain

        yesterday = date.today() - timedelta(days=1)
        start_date = yesterday.strftime("%m/%d/%y")

        stock_data = sti.get_data(stock, start_date)
        print("**** STOCK DATA ****")
        # print(stock_data)

        # retrieve stock ID from stock_ticker
        # stock_data['stock_id'] = stock_id
        stock_data['date'] = stock_data.index
        stock_data = stock_data[['ticker', 'date', 'open', 'close', 'low', 'high', 'adjclose', 'volume']]
        stock_data.columns = ['stock_id', 'date', 'open_price', 'close_price', 'low_price', 'high_price', 'adjusted_close_price', 'volume']

        # round everything to 2 decimal points
        stock_data['open_price'] = stock_data['open_price'].round(2)
        stock_data['close_price'] = stock_data['close_price'].round(2)
        stock_data['low_price'] = stock_data['low_price'].round(2)
        stock_data['high_price'] = stock_data['high_price'].round(2)
        stock_data['adjusted_close_price'] = stock_data['adjusted_close_price'].round(2)

        # drop index
        stock_data.reset_index(drop=True, inplace=True)

        print(stock_data.to_string())
        print("********************")

        get_all = ops.get_options_chain(stock)
        print(get_all)


    # put all into database
    print("Daily pull done")
    return


# pull once a week, only update if changed?
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


pull_daily()

pull_all()