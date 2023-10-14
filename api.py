# region Imports
import requests
import pandas as pd
import numpy as np
import time
import schedule
import datetime as dt
import re

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

    pull_all(cursor)

    cursor.commit()

    cursor.close()
    conn.close()
# endregion


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
                    'option_type': 'calls',
                    'strike_price': row['Strike'],
                    'bid': row['Bid'],
                    'ask': row['Ask'],
                    'change': row['Change'],
                    'percent_change': row['% Change'],
                    'volume': row['Volume'],
                    'open_interest': row['Open Interest'],
                    'implied_volatility': row['Implied Volatility']
                }, ignore_index=True)

            get_puts = ops.get_puts(stock, date)

            for index, row in get_puts.iterrows():
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

        # print(calls.to_string())

        grouped = calls.groupby(calls['expiration_date'])

        combo_calls = []
        for date, group in grouped:
            # print("expiration_date: ", date)
            # print(group)
            # print()

            index = group['volume'].idxmax()
            actual_index = group.index.get_loc(index)
            # print(actual_index)
            above_indices = actual_index - 3
            below_indices = actual_index + 4

            if (above_indices < 0):
                below_indices += (0 - above_indices)
                above_indices = 0

            if (below_indices >= len(group)):
                above_indices -= (below_indices - len(group))

            combo_calls.append(group.iloc[above_indices:below_indices])
            # print(group.iloc[above_indices:below_indices])
            # print("**********")

        combined_calls = pd.concat(combo_calls, ignore_index=True)
        combined_calls['expiration_date'] = pd.to_datetime(combined_calls['expiration_date'])
        combined_calls = combined_calls.sort_values(by='expiration_date')
        combined_calls = combined_calls.reset_index(drop=True)

        # print(combined_calls)


        calls = calls.replace('-', 0)
        calls['volume'] = pd.to_numeric(calls['volume'], errors='coerce').fillna(0).astype(int)

        # print(calls.to_string())

        grouped = calls.groupby(calls['expiration_date'])

        combo_calls = []
        for date, group in grouped:
            # print("expiration_date: ", date)
            # print(group)
            # print()

            index = group['volume'].idxmax()
            actual_index = group.index.get_loc(index)
            # print(actual_index)
            above_indices = actual_index - 3
            below_indices = actual_index + 4

            if (above_indices < 0):
                below_indices += (0 - above_indices)
                above_indices = 0

            if (below_indices >= len(group)):
                above_indices -= (below_indices - len(group))

            combo_calls.append(group.iloc[above_indices:below_indices])
            print(group.iloc[above_indices:below_indices])
            print("**********")

        combined_calls = pd.concat(combo_calls, ignore_index=True)
        combined_calls['expiration_date'] = pd.to_datetime(combined_calls['expiration_date'])
        combined_calls = combined_calls.sort_values(by=['expiration_date', 'strike_price'])

        # puts
        puts = puts.replace('-', 0)
        puts['volume'] = pd.to_numeric(puts['volume'], errors='coerce').fillna(0).astype(int)

        # print(puts.to_string())

        grouped = puts.groupby(puts['expiration_date'])

        combo_puts = []
        for date, group in grouped:
            # print("expiration_date: ", date)
            # print(group)
            # print()

            index = group['volume'].idxmax()
            actual_index = group.index.get_loc(index)
            # print(actual_index)
            above_indices = actual_index - 3
            below_indices = actual_index + 4

            if (above_indices < 0):
                below_indices += (0 - above_indices)
                above_indices = 0

            if (below_indices >= len(group)):
                above_indices -= (below_indices - len(group))

            combo_puts.append(group.iloc[above_indices:below_indices])
            print(group.iloc[above_indices:below_indices])
            print("**********")

        combined_puts = pd.concat(combo_puts, ignore_index=True)
        combined_puts['expiration_date'] = pd.to_datetime(combined_puts['expiration_date'])
        combined_puts['option_type'] = 'puts'
        combined_puts = combined_puts.sort_values(by=['expiration_date', 'strike_price'])

        print("CALLS: ")
        print(combined_calls)
        print("PUTS: ")
        print(combined_puts)

        return combined_calls, combined_puts

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
            'current_qtr_name': [],
            'next_qtr': [],
            'next_qtr_name': [],
            'current_year': [],
            'current_year_name': [],
            'next_year': [],
            'next_year_name': []
        }

        column_list = get_analyst['Earnings Estimate'].columns.tolist()
        # print("WAHHHH")
        dates = column_list[1:5]
        contents_in_parentheses = [re.search(r'\(([^)]+)\)', col).group(1) for col in dates]
        # print(contents_in_parentheses)

        # update the stock to stock ID later
        earnings_estimate = pd.DataFrame(data)
        earnings_estimate = earnings_estimate.append({
            'stock_id': stock,
            'data_type': 'earnings avg',
            'current_qtr': get_analyst['Earnings Estimate'][column_list[1]][1],
            'current_qtr_name': contents_in_parentheses[0],
            'next_qtr': get_analyst['Earnings Estimate'][column_list[2]][1],
            'next_qtr_name': contents_in_parentheses[1],
            'current_year': get_analyst['Earnings Estimate'][column_list[3]][1],
            'current_year_name': contents_in_parentheses[2],
            'next_year': get_analyst['Earnings Estimate'][column_list[4]][1],
            'next_year_name': contents_in_parentheses[3]
        }, ignore_index=True)

        earnings_estimate = earnings_estimate.append({
            'stock_id': stock,
            'data_type': 'earnings low',
            'current_qtr': get_analyst['Earnings Estimate'][column_list[1]][2],
            'current_qtr_name': contents_in_parentheses[0],
            'next_qtr': get_analyst['Earnings Estimate'][column_list[2]][2],
            'next_qtr_name': contents_in_parentheses[1],
            'current_year': get_analyst['Earnings Estimate'][column_list[3]][2],
            'current_year_name': contents_in_parentheses[2],
            'next_year': get_analyst['Earnings Estimate'][column_list[4]][2],
            'next_year_name': contents_in_parentheses[3]
        }, ignore_index=True)

        earnings_estimate = earnings_estimate.append({
            'stock_id': stock,
            'data_type': 'earnings high',
            'current_qtr': get_analyst['Earnings Estimate'][column_list[1]][3],
            'current_qtr_name': contents_in_parentheses[0],
            'next_qtr': get_analyst['Earnings Estimate'][column_list[2]][3],
            'next_qtr_name': contents_in_parentheses[1],
            'current_year': get_analyst['Earnings Estimate'][column_list[3]][3],
            'current_year_name': contents_in_parentheses[2],
            'next_year': get_analyst['Earnings Estimate'][column_list[4]][3],
            'next_year_name': contents_in_parentheses[3]
        }, ignore_index=True)

        print(earnings_estimate)

        print()
        print("**** Revenue Estimate ****")
        # print(get_analyst['Revenue Estimate'])

        column_list = get_analyst['Revenue Estimate'].columns.tolist()
        dates = column_list[1:5]
        contents_in_parentheses = [re.search(r'\(([^)]+)\)', col).group(1) for col in dates]

        revenue_estimate = pd.DataFrame(data)

        # update the stock to stock ID later
        revenue_estimate = revenue_estimate.append({
            'stock_id': stock,
            'data_type': 'revenue avg',
            'current_qtr': get_analyst['Revenue Estimate'][column_list[1]][1],
            'current_qtr_name': contents_in_parentheses[0],
            'next_qtr': get_analyst['Revenue Estimate'][column_list[2]][1],
            'next_qtr_name': contents_in_parentheses[1],
            'current_year': get_analyst['Revenue Estimate'][column_list[3]][1],
            'current_year_name': contents_in_parentheses[2],
            'next_year': get_analyst['Revenue Estimate'][column_list[4]][1],
            'next_year_name': contents_in_parentheses[3]
        }, ignore_index=True)

        revenue_estimate = revenue_estimate.append({
            'stock_id': stock,
            'data_type': 'revenue low',
            'current_qtr': get_analyst['Revenue Estimate'][column_list[1]][2],
            'current_qtr_name': contents_in_parentheses[0],
            'next_qtr': get_analyst['Revenue Estimate'][column_list[2]][2],
            'next_qtr_name': contents_in_parentheses[1],
            'current_year': get_analyst['Revenue Estimate'][column_list[3]][2],
            'current_year_name': contents_in_parentheses[2],
            'next_year': get_analyst['Revenue Estimate'][column_list[4]][2],
            'next_year_name': contents_in_parentheses[3]
        }, ignore_index=True)

        revenue_estimate = revenue_estimate.append({
            'stock_id': stock,
            'data_type': 'revenue high',
            'current_qtr': get_analyst['Revenue Estimate'][column_list[1]][3],
            'current_qtr_name': contents_in_parentheses[0],
            'next_qtr': get_analyst['Revenue Estimate'][column_list[2]][3],
            'next_qtr_name': contents_in_parentheses[1],
            'current_year': get_analyst['Revenue Estimate'][column_list[3]][3],
            'current_year_name': contents_in_parentheses[2],
            'next_year': get_analyst['Revenue Estimate'][column_list[4]][3],
            'next_year_name': contents_in_parentheses[3]
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

        return earnings_estimate, revenue_estimate, earnings_history


# pull once a day, 8pm est
# region Pulling Stock Data Methods
def pull_daily(cursor):
    for stock in stock_list:
        # pull stock data:
        # open, high, low, close, adjusted close, volume
        # options chain

        today = dt.date.today()
        start_date = today.strftime("%m/%d/%y")

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
        stock_data['date'] = stock_data['date'].dt.strftime('%Y-%m-%d')

        # print(stock_data.to_string())
        # print("********************")
        # print()

        # pull last 49 days of data
        cursor.execute(f"select stock_id from stock where stock_name = '{stock_data['stock_id'][0]}'")
        stock_id = cursor.fetchone()
        stock_data['stock_id'] = stock_id[0]

        cursor.execute(f"SELECT TOP 50 * FROM price WHERE stock_id = '{stock_id[0]}' ORDER BY date DESC")
        df = pd.DataFrame.from_records(cursor.fetchall(), columns=[col[0] for col in cursor.description])
        df = df.sort_values(by='date', ascending=True)

        df = df.reset_index(drop=True)

        p_change = (stock_data['adjusted_close_price'] - float(df.iloc[48]['adjusted_close_price'])) / float(df.iloc[48]['adjusted_close_price'])
        # print(p_change)

        stock_data['percent_change'] = p_change

        df = df.append(stock_data)
        df['adjusted_close_price'] = df['adjusted_close_price'].astype(float)
        df = df.reset_index(drop=True)
        print(df)
        print("-----------")
        print(df['adjusted_close_price'])
        print("-----------")

        # TODO: Do indicators here
        indicators_final = [stock_id[0], start_date]
        sma_50 = indicators.calculate_sma(df['adjusted_close_price'], days=50)
        print("SMA 50")
        print(sma_50.iloc[50])
        indicators_final.append(sma_50.iloc[50])

        ema_26 = indicators.calculate_ema(df['adjusted_close_price'])
        print("EMA 26")
        print(ema_26.iloc[50])
        indicators_final.append(ema_26.iloc[50])

        bb_20 = indicators.calculate_bb(df['adjusted_close_price'])
        print("BB 20")
        print(bb_20.iloc[50])
        indicators_final.append(bb_20.iloc[50]["bb_middle"])
        indicators_final.append(bb_20.iloc[50]["bb_lower"])
        indicators_final.append(bb_20.iloc[50]["bb_upper"])

        rsi_14 = indicators.calculate_rsi(df['adjusted_close_price'])
        print("RSI 14")
        print(rsi_14.iloc[50])
        indicators_final.append(rsi_14.iloc[50])

        percent_r_14 = indicators.calculate_percent_r(df['adjusted_close_price'])
        print("R 14")
        print(percent_r_14.iloc[50])
        indicators_final.append(percent_r_14.iloc[50])

        so_14 = indicators.calculate_so(df['adjusted_close_price'])
        print("SO 14")
        indicators_final.append(so_14.iloc[50]["p_k"])
        indicators_final.append(so_14.iloc[50]["p_d"])

        percent_m_14 = indicators.calculate_roc(df['adjusted_close_price'])
        print("%M 14")
        print(percent_m_14.iloc[50])
        indicators_final.append(percent_m_14.iloc[50])

        print(indicators_final)

        # TODO: Add options here later.
        # pull_options(yesterday)


    # put all into database
    print("Daily pull done")
    return


def pull_all(cursor):

    # check if any data exists in database
    cursor.execute(f"select top 1 * from Stock")
    any_data = cursor.fetchone()

    # if (any_data):
    #     print(any_data)
    #     return

    for stock in stock_list:
        # PRICE DATABASE
        stock_data = sti.get_data(stock, start_date="01/01/2021")
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

        # ADD TO PRICE DATABASE
        for i in range(len(stock_data)):
            cursor.execute(f"insert into price(stock_id, date, open_price, close_price, low_price, high_price, percent_change, adjusted_close_price, volume) values ('{stock_data['stock_id'][i]}', '{stock_data['date'][i]}', '{stock_data['open_price'][i]}', '{stock_data['close_price'][i]}','{stock_data['low_price'][i]}', '{stock_data['high_price'][i]}', '{stock_data['percent_change'][i]}', '{stock_data['adjusted_close_price'][i]}', '{stock_data['volume'][i]}')")

        # ADD INDICATORS
        # calculate SMA, EMA, BB, RSI, %R, SO, M
        date_id = stock_data[['stock_id', 'date']]
        all_indicators = date_id

        sma_50 = indicators.calculate_sma(stock_data['adjusted_close_price'], days=50)
        all_indicators = all_indicators.join(sma_50)

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
        yesterday = dt.date.today() - dt.timedelta(days=1)
        start_date = yesterday.strftime("%m/%d/%y")

        calls, puts = pull_options(current_date=start_date)

        calls['stock_id'] = stock_id[0]
        puts['stock_id'] = stock_id[0]

        for i in range(len(calls)):
            cursor.execute(f"insert into options(stock_id, date, expiration_date, option_type, strike_price, bid, ask, change, percent_change, volume, open_interest, implied_volatility) values ('{calls['stock_id'][i]}', '{calls['date'][i]}', '{calls['expiration_date'][i]}', '{calls['option_type'][i]}', '{calls['strike_price'][i]}', '{calls['bid'][i]}', '{calls['ask'][i]}', '{calls['change'][i]}', '{calls['percent_change'][i]}', '{calls['volume'][i]}', '{calls['open_interest'][i]}', '{calls['implied_volatility'][i]}')")

        for i in range(len(puts)):
            cursor.execute(f"insert into options(stock_id, date, expiration_date, option_type, strike_price, bid, ask, change, percent_change, volume, open_interest, implied_volatility) values ('{puts['stock_id'][i]}', '{puts['date'][i]}', '{puts['expiration_date'][i]}', '{puts['option_type'][i]}', '{puts['strike_price'][i]}', '{puts['bid'][i]}', '{puts['ask'][i]}', '{puts['change'][i]}', '{puts['percent_change'][i]}', '{puts['volume'][i]}', '{puts['open_interest'][i]}', '{puts['implied_volatility'][i]}')")


        earnings_estimate, revenue_estimate, earnings_history = pull_analyst()

        earnings_estimate['stock_id'] = stock_id[0]
        revenue_estimate['stock_id'] = stock_id[0]
        earnings_history['stock_id'] = stock_id[0]

        for i in range(len(earnings_estimate)):
            cursor.execute(f"insert into earningsestimate(stock_id, data_type, current_qtr, current_qtr_name, next_qtr, next_qtr_name, current_year, current_year_name, next_year, next_year_name) values ('{earnings_estimate['stock_id'][i]}', '{earnings_estimate['data_type'][i]}', '{earnings_estimate['current_qtr'][i]}', '{earnings_estimate['current_qtr_name'][i]}','{earnings_estimate['next_qtr'][i]}', '{earnings_estimate['next_qtr_name'][i]}', '{earnings_estimate['current_year'][i]}', '{earnings_estimate['current_year_name'][i]}', '{earnings_estimate['next_year'][i]}', '{earnings_estimate['next_year_name'][i]}')")

        for i in range(len(revenue_estimate)):
            cursor.execute(f"insert into revenueestimate(stock_id, data_type, current_qtr, current_qtr_name, next_qtr, next_qtr_name, current_year, current_year_name, next_year, next_year_name) values ('{revenue_estimate['stock_id'][i]}', '{revenue_estimate['data_type'][i]}', '{revenue_estimate['current_qtr'][i]}', '{revenue_estimate['current_qtr_name'][i]}','{revenue_estimate['next_qtr'][i]}', '{revenue_estimate['next_qtr_name'][i]}', '{revenue_estimate['current_year'][i]}', '{revenue_estimate['current_year_name'][i]}', '{revenue_estimate['next_year'][i]}', '{revenue_estimate['next_year_name'][i]}')")

        for i in range(len(earnings_history)):
            cursor.execute(f"insert into earningshistory(stock_id, data_type, four_back, four_date, three_back, three_date, two_back, two_date, one_back, one_date) values ('{earnings_history['stock_id'][i]}', '{earnings_history['data_type'][i]}', '{earnings_history['four_back'][i]}', '{earnings_history['four_date'][i]}','{earnings_history['three_back'][i]}', '{earnings_history['three_date'][i]}', '{earnings_history['two_back'][i]}', '{earnings_history['two_date'][i]}', '{earnings_history['one_back'][i]}', '{earnings_history['one_date'][i]}')")

    return
# endregion


"""
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
"""



# today = dt.date.today()
# start_date = today.strftime("%m/%d/%y")
# pull_options(start_date)

# pull_all()

# pull_analyst()

# do_indicators()

# initialize_stocks()

connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
print(connection_string)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

pull_daily(cursor)

cursor.commit()

cursor.close()
conn.close()



