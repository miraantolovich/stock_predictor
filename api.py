# region Imports
import requests
import pandas as pd
import numpy as np
import time
import schedule
import datetime as dt

import yahoo_fin.options as ops
import yahoo_fin.stock_info as sti

import pyodbc

import indicators

# endregion

# region Variables
pd.set_option('display.max_columns', None)
# medium (monthly plays) to medium/large-cap stocks
# analyst rating
# insider trading/purchases

# get list of all stocks to compare
# INTC (large), CWH (small-med), GBX (small), SOFI (medium), SUZ (medium), AAL (medium)
stock_list = ["INTC"]
# stock_list = ["INTC", "CWH", "GBX", "SOFI", "SUZ", "AAL", "^GSPC", "^TNX"]
stock_name = ["Intel Corporation", "Camping World Holdings", "The Greenbrier Companies", "SoFi Technologies",
              "Suzano S.A.", "American Airlines Group", "S&P 500", "Treasury Yield 10 Years"]
# endregion

# region Set Up Database Connection
driver = 'ODBC Driver 17 for SQL Server'
server = 'MSI\SQLEXPRESS'
database = 'Stock_Information'


def initialize_stocks():
    connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
    print(connection_string)

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    for i in range(len(stock_list)):
        cursor.execute(f"insert into stock(stock_name, stock_long_name) values ('{stock_list[i]}', '{stock_name[i]}')")


    # TODO: PULL ALL THE DATA HERE
    pull_all(cursor)

    cursor.commit()

    cursor.close()
    conn.close()
# endregion


# pull once a day, 8pm est
# region Pulling Stock Data Methods
def pull_daily():
    for stock in stock_list:
        # pull stock data:
        # open, high, low, close, adjusted close, volume
        # options chain

        yesterday = dt.date.today() - dt.timedelta(days=1)
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
        print()

        # TODO: Do indicators here

        # TODO: Add options here later.
        pull_options(yesterday)


    # put all into database
    print("Daily pull done")
    return


def pull_options(current_date):
    data = {
        'stock_id': [],
        'date': [],
        'expiration_date': [],
        'option_type': [],
        'strike_price': [],
        'bid': [],
        'ask': [],
        'change': [],
        'percent_change': [],
        'volume': [],
        'open_interest': [],
        'implied_volatility': []
    }

    calls = pd.DataFrame(data)
    puts = pd.DataFrame(data)

    for stock in stock_list:
        get_dates = ops.get_expiration_dates(stock)
        print(get_dates)

        for date in get_dates:
            get_calls = ops.get_calls(stock, date)
            # print(get_all)

            for index, row in get_calls.iterrows():
                # print(row)
                calls = calls.append({
                    'stock_id': stock,
                    'date': current_date,
                    'expiration_date': date,
                    'option_type': 'call',
                    'strike_price': row['Strike'],
                    'bid': row['Bid'],
                    'ask': row['Ask'],
                    'change': row['Change'],
                    'percent_change': row['% Change'],
                    'volume': row['Volume'],
                    'open_interest': row['Open Interest'],
                    'implied_volatility': row['Implied Volatility']
                }, ignore_index=True)

            get_calls = ops.get_puts(stock, date)

            for index, row in get_calls.iterrows():
                # print(row)
                puts = calls.append({
                    'stock_id': stock,
                    'date': current_date,
                    'expiration_date': date,
                    'option_type': 'puts',
                    'strike_price': row['Strike'],
                    'bid': row['Bid'],
                    'ask': row['Ask'],
                    'change': row['Change'],
                    'percent_change': row['% Change'],
                    'volume': row['Volume'],
                    'open_interest': row['Open Interest'],
                    'implied_volatility': row['Implied Volatility']
                }, ignore_index=True)

        calls = calls.replace('-', 0)
        calls['volume'] = pd.to_numeric(calls['volume'], errors='coerce').fillna(0).astype(int)
        calls['expiration_date'] = pd.to_datetime(calls['expiration_date'], format='%B %d, %Y').dt.strftime('%m/%d/%y')

        print(calls.to_string())

        grouped = calls.groupby(calls['expiration_date'])

        for date, group in grouped:
            print("expiration_date: ", date)
            print(group)
            print()

            index = group['volume'].idxmax()
            print(index)
            above_indices = index - 3
            below_indices = index + 4

            print(group.iloc[above_indices:below_indices])
            print("**********")

        # print(puts.to_string())


# pull once a week, only update if changed?
def pull_analyst():
    for stock in stock_list:
        get_analyst = sti.get_analysts_info(stock)
        # print(get_analyst)

        print("**** Earnings Estimate ****")
        # print(get_analyst['Earnings Estimate'])

        data = {
            'stock_id': [],
            'data_type': [],
            'current_qtr': [],
            'next_qtr': [],
            'current_year': [],
            'next_year': []
        }

        column_list = get_analyst['Earnings Estimate'].columns.tolist()

        # update the stock to stock ID later
        earnings_estimate = pd.DataFrame(data)
        earnings_estimate = earnings_estimate.append({
            'stock_id': stock,
            'data_type': 'earnings avg',
            'current_qtr': get_analyst['Earnings Estimate'][column_list[1]][1],
            'next_qtr': get_analyst['Earnings Estimate'][column_list[2]][1],
            'current_year': get_analyst['Earnings Estimate'][column_list[3]][1],
            'next_year': get_analyst['Earnings Estimate'][column_list[4]][1]
        }, ignore_index=True)

        earnings_estimate = earnings_estimate.append({
            'stock_id': stock,
            'data_type': 'earnings low',
            'current_qtr': get_analyst['Earnings Estimate'][column_list[1]][2],
            'next_qtr': get_analyst['Earnings Estimate'][column_list[2]][2],
            'current_year': get_analyst['Earnings Estimate'][column_list[3]][2],
            'next_year': get_analyst['Earnings Estimate'][column_list[4]][2]
        }, ignore_index=True)

        earnings_estimate = earnings_estimate.append({
            'stock_id': stock,
            'data_type': 'earnings high',
            'current_qtr': get_analyst['Earnings Estimate'][column_list[1]][3],
            'next_qtr': get_analyst['Earnings Estimate'][column_list[2]][3],
            'current_year': get_analyst['Earnings Estimate'][column_list[3]][3],
            'next_year': get_analyst['Earnings Estimate'][column_list[4]][3]
        }, ignore_index=True)

        print(earnings_estimate)

        print()
        print("**** Revenue Estimate ****")
        # print(get_analyst['Revenue Estimate'])

        column_list = get_analyst['Revenue Estimate'].columns.tolist()

        revenue_estimate = pd.DataFrame(data)

        # update the stock to stock ID later
        revenue_estimate = revenue_estimate.append({
            'stock_id': stock,
            'data_type': 'revenue avg',
            'current_qtr': get_analyst['Revenue Estimate'][column_list[1]][1],
            'next_qtr': get_analyst['Revenue Estimate'][column_list[2]][1],
            'current_year': get_analyst['Revenue Estimate'][column_list[3]][1],
            'next_year': get_analyst['Revenue Estimate'][column_list[4]][1]
        }, ignore_index=True)

        revenue_estimate = revenue_estimate.append({
            'stock_id': stock,
            'data_type': 'revenue low',
            'current_qtr': get_analyst['Revenue Estimate'][column_list[1]][2],
            'next_qtr': get_analyst['Revenue Estimate'][column_list[2]][2],
            'current_year': get_analyst['Revenue Estimate'][column_list[3]][2],
            'next_year': get_analyst['Revenue Estimate'][column_list[4]][2]
        }, ignore_index=True)

        revenue_estimate = revenue_estimate.append({
            'stock_id': stock,
            'data_type': 'revenue high',
            'current_qtr': get_analyst['Revenue Estimate'][column_list[1]][3],
            'next_qtr': get_analyst['Revenue Estimate'][column_list[2]][3],
            'current_year': get_analyst['Revenue Estimate'][column_list[3]][3],
            'next_year': get_analyst['Revenue Estimate'][column_list[4]][3]
        }, ignore_index=True)

        print(revenue_estimate)

        data = {
            'stock_id': [],
            'data_type': [],
            'four_back': [],
            'four_date': [],
            'three_back': [],
            'three_date': [],
            'two_back': [],
            'two_date': [],
            'one_back': [],
            'one_date': []
        }

        print()
        print("**** Earnings History ****")
        # print(get_analyst['Earnings History'])

        column_list = get_analyst['Earnings History'].columns.tolist()

        earnings_history = pd.DataFrame(data)

        # update the stock to stock ID later
        earnings_history = earnings_history.append({
            'stock_id': stock,
            'data_type': 'estimated',
            'four_back': get_analyst['Earnings History'][column_list[1]][0],
            'four_date': column_list[1],
            'three_back': get_analyst['Earnings History'][column_list[2]][0],
            'three_date': column_list[2],
            'two_back': get_analyst['Earnings History'][column_list[3]][0],
            'two_date': column_list[3],
            'one_back': get_analyst['Earnings History'][column_list[4]][0],
            'one_date': column_list[4]
        }, ignore_index=True)

        earnings_history = earnings_history.append({
            'stock_id': stock,
            'data_type': 'actual',
            'four_back': get_analyst['Earnings History'][column_list[1]][1],
            'four_date': column_list[1],
            'three_back': get_analyst['Earnings History'][column_list[2]][1],
            'three_date': column_list[2],
            'two_back': get_analyst['Earnings History'][column_list[3]][1],
            'two_date': column_list[3],
            'one_back': get_analyst['Earnings History'][column_list[4]][1],
            'one_date': column_list[4]
        }, ignore_index=True)

        earnings_history = earnings_history.append({
            'stock_id': stock,
            'data_type': 'difference',
            'four_back': get_analyst['Earnings History'][column_list[1]][2],
            'four_date': column_list[1],
            'three_back': get_analyst['Earnings History'][column_list[2]][2],
            'three_date': column_list[2],
            'two_back': get_analyst['Earnings History'][column_list[3]][2],
            'two_date': column_list[3],
            'one_back': get_analyst['Earnings History'][column_list[4]][2],
            'one_date': column_list[4]
        }, ignore_index=True)

        print(earnings_history)
        print()
    # TODO: Add all to database


def pull_all(cursor):

    # check if any data exists in database
    cursor.execute(f"select top 1 * from Stock")
    any_data = cursor.fetchone()

    # if (any_data):
    #     print(any_data)
    #     return

    for stock in stock_list:
        stock_data = sti.get_data(stock, start_date="01/01/2019")
        print(stock_data)

        stock_data['date'] = stock_data.index
        stock_data['percent_change'] = stock_data['adjclose'].pct_change() * 100

        stock_data = stock_data[['ticker', 'date', 'open', 'close', 'low', 'high', 'percent_change', 'adjclose', 'volume']]
        stock_data.columns = ['stock_id', 'date', 'open_price', 'close_price', 'low_price', 'high_price', 'percent_change', 'adjusted_close_price', 'volume']

        # round everything to 2 decimal points
        stock_data['open_price'] = stock_data['open_price'].round(2)
        stock_data['close_price'] = stock_data['close_price'].round(2)
        stock_data['low_price'] = stock_data['low_price'].round(2)
        stock_data['high_price'] = stock_data['high_price'].round(2)
        stock_data['adjusted_close_price'] = stock_data['adjusted_close_price'].round(2)

        # drop index
        stock_data.reset_index(drop=True, inplace=True)

        stock_data = stock_data.fillna(-3012)

        cursor.execute(f"select stock_id from stock where stock_name = '{stock_data['stock_id'][0]}'")
        stock_id = cursor.fetchone()

        stock_data['stock_id'] = stock_id[0]

        print(stock_data)

        # TODO: Add to database
        for i in range(len(stock_data)):
            cursor.execute(f"insert into price(stock_id, date, open_price, close_price, low_price, high_price, percent_change, adjusted_close_price, volume) values ('{stock_data['stock_id'][i]}', '{stock_data['date'][i]}', '{stock_data['open_price'][i]}', '{stock_data['close_price'][i]}','{stock_data['low_price'][i]}', '{stock_data['high_price'][i]}', '{stock_data['percent_change'][i]}', '{stock_data['adjusted_close_price'][i]}', '{stock_data['volume'][i]}')")

        # TODO: Add indicators
        # calculate SMA, EMA, BB, RSI, %R, SO, M
        date_id = stock_data[['stock_id', 'date']]
        all_indicators = date_id

        sma_200 = indicators.calculate_sma(stock_data['adjusted_close_price'], days=50)
        all_indicators = all_indicators.join(sma_200)

        ema_26 = indicators.calculate_ema(stock_data['adjusted_close_price'])
        all_indicators = all_indicators.join(ema_26)

        bb_20 = indicators.calculate_bb(stock_data['adjusted_close_price'])
        all_indicators = all_indicators.join(bb_20)

        rsi_14 = indicators.calculate_rsi(stock_data['adjusted_close_price'])
        all_indicators = all_indicators.join(rsi_14)

        percent_r_14 = indicators.calculate_percent_r(stock_data['adjusted_close_price'])
        all_indicators = all_indicators.join(percent_r_14)

        so_14 = indicators.calculate_so(stock_data['adjusted_close_price'])
        all_indicators = all_indicators.join(so_14)

        percent_m_14 = indicators.calculate_roc(stock_data['adjusted_close_price'])
        all_indicators = all_indicators.join(percent_m_14)


        all_indicators = all_indicators.fillna(-3012)
        print(all_indicators)

        for i in range(len(all_indicators)):
            cursor.execute(f"insert into indicators(stock_id, date, sma, ema, bb_middle, bb_lower, bb_upper, roc, r_percent, si_k, si_d, rsi) values ('{all_indicators['stock_id'][i]}', '{all_indicators['date'][i]}', '{all_indicators['sma'][i]}', '{all_indicators['ema'][i]}','{all_indicators['bb_middle'][i]}', '{all_indicators['bb_lower'][i]}', '{all_indicators['bb_upper'][i]}', '{all_indicators['roc'][i]}', '{all_indicators['percent_r'][i]}', '{all_indicators['p_k'][i]}', '{all_indicators['p_d'][i]}', '{all_indicators['rsi'][i]}')")

        # options, analyst ratings not available for past, pull most recent

    return
# endregion

def do_indicators():
    stock_data = sti.get_data("INTC", start_date="01/01/2019")

    stock_data['date'] = stock_data.index
    stock_data = stock_data[['ticker', 'date', 'open', 'close', 'low', 'high', 'adjclose', 'volume']]
    stock_data.columns = ['stock_id', 'date', 'open_price', 'close_price', 'low_price', 'high_price',
                          'adjusted_close_price', 'volume']

    # round everything to 2 decimal points
    stock_data['open_price'] = stock_data['open_price'].round(2)
    stock_data['close_price'] = stock_data['close_price'].round(2)
    stock_data['low_price'] = stock_data['low_price'].round(2)
    stock_data['high_price'] = stock_data['high_price'].round(2)
    stock_data['adjusted_close_price'] = stock_data['adjusted_close_price'].round(2)

    # drop index
    stock_data.reset_index(drop=True, inplace=True)

    date_id = stock_data[['stock_id', 'date']]
    all_indicators = date_id

    sma_200 = indicators.calculate_sma(stock_data['adjusted_close_price'], days=50)
    all_indicators = all_indicators.join(sma_200)

    ema_26 = indicators.calculate_ema(stock_data['adjusted_close_price'])
    all_indicators = all_indicators.join(ema_26)

    bb_20 = indicators.calculate_bb(stock_data['adjusted_close_price'])
    all_indicators = all_indicators.join(bb_20)

    rsi_14 = indicators.calculate_rsi(stock_data['adjusted_close_price'])
    all_indicators = all_indicators.join(rsi_14)

    percent_r_14 = indicators.calculate_percent_r(stock_data['adjusted_close_price'])
    all_indicators = all_indicators.join(percent_r_14)

    so_14 = indicators.calculate_so(stock_data['adjusted_close_price'])
    all_indicators = all_indicators.join(so_14)

    percent_roc_14 = indicators.calculate_roc(stock_data['adjusted_close_price'])
    all_indicators = all_indicators.join(percent_roc_14)

    print(all_indicators.to_string())


today = dt.date.today()
start_date = today.strftime("%m/%d/%y")

# pull_daily()

pull_options(start_date)

# pull_all()

# pull_analyst()

# do_indicators()

# initialize_stocks()

