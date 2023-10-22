# region Imports
import datetime

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
# stock_list = ["INTC"]
stock_list = ["INTC", "CWH", "GBX", "SOFI", "SUZ", "AAL"]
stock_name = ["Intel Corporation", "Camping World Holdings", "The Greenbrier Companies", "SoFi Technologies",
              "Suzano S.A.", "American Airlines Group"]
# endregion

# region Set Up Database Connection
driver = 'ODBC Driver 17 for SQL Server'
server = 'MSI\SQLEXPRESS'
database = 'Stock_Information'
# endregion

# region Set Up Database Inserts
sql_insert_stock = "EXEC [Stock_Information].[dbo].[InsertStock] ?, ?"
sql_insert_price = "EXEC [Stock_Information].[dbo].[InsertPrice] ?, ?, ?, ?, ?, ?, ?, ?, ?"
sql_insert_indicators = "EXEC [Stock_Information].[dbo].[InsertIndicators] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
sql_insert_options = "EXEC [Stock_Information].[dbo].[InsertOptions] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
sql_insert_earnings_estimate = "EXEC [Stock_Information].[dbo].[InsertEarningsEstimate] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
sql_insert_earnings_history = "EXEC [Stock_Information].[dbo].[InsertEarningsHistory] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
sql_insert_revenue_estimate = "EXEC [Stock_Information].[dbo].[InsertRevenueEstimate] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
# endregion

# region Set Up Database Selects
sql_select_stock = "EXEC [Stock_Information].[dbo].[SelectStock]"
sql_select_stock_with_id = "EXEC [Stock_Information].[dbo].[SelectStockWithID] ?"
sql_select_stock_top = "EXEC [Stock_Information].[dbo].[SelectStockTop] ?"
# endregion

def initialize_stocks():
    connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    for i in range(len(stock_list)):
        params = (stock_list[i], stock_name[i])
        cursor.execute(sql_insert_stock, params)

    pull_all(cursor)

    cursor.commit()

    cursor.close()
    conn.close()


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

        calls = calls.replace('-', '0.00%')
        calls['volume'] = pd.to_numeric(calls['volume'], errors='coerce').fillna(0)
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
def pull_daily():
    connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    for stock in stock_list:
        # pull stock data:
        # open, high, low, close, adjusted close, volume
        # options chain

        today = dt.date.today()
        start_date = today.strftime('%Y-%m-%d')
        print(start_date)

        if (today.weekday() == 5 or today.weekday() == 6):
            print("Skip weekends.")
            cursor.commit()

            cursor.close()
            conn.close()
            return

        stock_data = sti.get_data(stock, start_date=start_date)
        print("**** STOCK DATA ****")
        print(stock_data)

        stock_time = stock_data.index[0].strftime('%Y-%m-%d')

        counter = 0
        while (start_date != stock_time):
            print("Nope. Try again.")
            counter += 1
            time.sleep(600)
            stock_data = sti.get_data(stock, start_date=start_date)

            if (counter >= 20):
                print("Was unable to pull data today.")
                cursor.commit()

                cursor.close()
                conn.close()
                return

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
        cursor.execute(sql_select_stock)
        stock_id = cursor.fetchone()
        stock_data['stock_id'] = stock_id[0]

        cursor.execute(sql_select_stock_top, stock_id[0])
        df = pd.DataFrame.from_records(cursor.fetchall(), columns=[col[0] for col in cursor.description])
        df = df.sort_values(by='date', ascending=True)

        df = df.reset_index(drop=True)

        p_change = (stock_data['adjusted_close_price'] - float(df.iloc[48]['adjusted_close_price'])) / float(df.iloc[48]['adjusted_close_price'])
        # print(p_change)

        stock_data['percent_change'] = p_change

        print(stock_data)

        df = df.append(stock_data)
        df['adjusted_close_price'] = df['adjusted_close_price'].astype(float)
        df = df.reset_index(drop=True)
        # print(df)
        # print("-----------")
        # print(df['adjusted_close_price'])
        # print("-----------")

        indicators_final = [stock_id[0], start_date]
        sma_50 = indicators.calculate_sma(df['adjusted_close_price'], days=50)
        # print("SMA 50")
        # print(sma_50['sma'].values[50])
        indicators_final.append(round(sma_50['sma'].values[50], 2))

        ema_26 = indicators.calculate_ema(df['adjusted_close_price'])
        # print("EMA 26")
        # print(ema_26['ema'].values[50])
        indicators_final.append(round(ema_26['ema'].values[50], 2))

        bb_20 = indicators.calculate_bb(df['adjusted_close_price'])
        # print("BB 20")
        # print(bb_20.values[50])
        indicators_final.append(round(bb_20["bb_middle"].values[50], 2))
        indicators_final.append(round(bb_20["bb_lower"].values[50], 2))
        indicators_final.append(round(bb_20["bb_upper"].values[50], 2))

        rsi_14 = indicators.calculate_rsi(df['adjusted_close_price'])
        # print("RSI 14")
        # print(rsi_14["rsi"].values[50])
        indicators_final.append(round(rsi_14["rsi"].values[50], 2))

        percent_r_14 = indicators.calculate_percent_r(df['adjusted_close_price'])
        # print("R 14")
        # print(percent_r_14["percent_r"].values[50])
        indicators_final.append(round(percent_r_14["percent_r"].values[50], 2))

        so_14 = indicators.calculate_so(df['adjusted_close_price'])
        # print("SO 14")
        # print(so_14["p_k"].values[50])
        # print(so_14["p_d"].values[50])
        indicators_final.append(round(so_14["p_k"].values[50], 2))
        indicators_final.append(round(so_14["p_d"].values[50], 2))

        percent_m_14 = indicators.calculate_roc(df['adjusted_close_price'])
        # print("%M 14")
        # print(percent_m_14["roc"].values[50])
        indicators_final.append(round(percent_m_14["roc"].values[50], 2))

        print(indicators_final)

        params = (str(stock_data['stock_id'].values[0]), stock_data['date'].values[0],
                  stock_data['open_price'].values[0], stock_data['close_price'].values[0],
                  stock_data['low_price'].values[0], stock_data['high_price'].values[0],
                  stock_data['percent_change'].values[0], stock_data['adjusted_close_price'].values[0],
                  str(stock_data['volume'].values[0]))
        cursor.execute(sql_insert_price, params)
        # cursor.execute(f"insert into price(stock_id, date, open_price, close_price, low_price, high_price, percent_change, adjusted_close_price, volume) values ('{stock_data['stock_id'].values[0]}', '{stock_data['date'].values[0]}', '{stock_data['open_price'].values[0]}', '{stock_data['close_price'].values[0]}','{stock_data['low_price'].values[0]}', '{stock_data['high_price'].values[0]}', '{stock_data['percent_change'].values[0]}', '{stock_data['adjusted_close_price'].values[0]}', '{stock_data['volume'].values[0]}')")

        params = (indicators_final[0], indicators_final[1], indicators_final[2], indicators_final[3],
                  indicators_final[4], indicators_final[5], indicators_final[6], indicators_final[11],
                  indicators_final[8], indicators_final[9], indicators_final[10], indicators_final[7])
        cursor.execute(sql_insert_indicators, params)
        # cursor.execute(f"insert into indicators(stock_id, date, sma, ema, bb_middle, bb_lower, bb_upper, roc, r_percent, si_k, si_d, rsi) values ('{indicators_final[0]}', '{indicators_final[1]}', '{indicators_final[2]}', '{indicators_final[3]}','{indicators_final[4]}', '{indicators_final[5]}', '{indicators_final[6]}', '{indicators_final[11]}', '{indicators_final[8]}', '{indicators_final[9]}', '{indicators_final[10]}', '{indicators_final[7]}')")

        # TODO: Add options here later.
        calls, puts = pull_options(start_date)

        calls['stock_id'] = stock_id[0]
        puts['stock_id'] = stock_id[0]

        for i in range(len(calls)):
            params = (calls['stock_id'][i], calls['date'][i], calls['expiration_date'][i], calls['option_type'][i],
                      calls['strike_price'][i], calls['bid'][i], calls['ask'][i], calls['change'][i],
                      calls['percent_change'][i], calls['volume'][i], calls['open_interest'][i],
                      calls['implied_volatility'][i])
            cursor.execute(sql_insert_options, params)

        for i in range(len(puts)):
            params = (puts['stock_id'][i], puts['date'][i], puts['expiration_date'][i], puts['option_type'][i],
                      puts['strike_price'][i], puts['bid'][i], puts['ask'][i], puts['change'][i],
                      puts['percent_change'][i], puts['volume'][i], puts['open_interest'][i],
                      puts['implied_volatility'][i])
            cursor.execute(sql_insert_options, params)

        earnings_estimate, revenue_estimate, earnings_history = pull_analyst()
        print(earnings_estimate)
        print(revenue_estimate)
        print(earnings_history)

        earnings_estimate['stock_id'] = stock_id[0]
        revenue_estimate['stock_id'] = stock_id[0]
        earnings_history['stock_id'] = stock_id[0]

        for i in range(len(earnings_estimate)):
            params = (earnings_estimate['stock_id'][i], earnings_estimate['data_type'][i], earnings_estimate['current_qtr'][i], earnings_estimate['current_qtr_name'][i], earnings_estimate['next_qtr'][i], earnings_estimate['next_qtr_name'][i], earnings_estimate['current_year'][i], earnings_estimate['current_year_name'][i], earnings_estimate['next_year'][i], earnings_estimate['next_year_name'][i])
            cursor.execute(sql_insert_earnings_estimate, params)

        for i in range(len(revenue_estimate)):
            params = (revenue_estimate['stock_id'][i], revenue_estimate['data_type'][i], revenue_estimate['current_qtr'][i], revenue_estimate['current_qtr_name'][i], revenue_estimate['next_qtr'][i], revenue_estimate['next_qtr_name'][i], revenue_estimate['current_year'][i], revenue_estimate['current_year_name'][i], revenue_estimate['next_year'][i], revenue_estimate['next_year_name'][i])
            cursor.execute(sql_insert_revenue_estimate, params)

        for i in range(len(earnings_history)):
            params = (earnings_history['stock_id'][i], earnings_history['data_type'][i], earnings_history['four_back'][i], earnings_history['four_date'][i], earnings_history['three_back'][i], earnings_history['three_date'][i], earnings_history['two_back'][i], earnings_history['two_date'][i], earnings_history['one_back'][i], earnings_history['one_date'][i])
            cursor.execute(sql_insert_earnings_history, params)

    # put all into database
    print("Daily pull done")
    cursor.commit()

    cursor.close()
    conn.close()

    return


def pull_all(cursor):

    # check if any data exists in database
    cursor.execute(sql_select_stock)
    any_data = cursor.fetchone()

    if (any_data):
        print(any_data)
        return

    # TODO: UNCOMMENT THIS LATER
    initialize_stocks()

    for stock in stock_list:
        # PRICE DATABASE
        yesterday = dt.date.today() - dt.timedelta(days=1)
        end_date = yesterday.strftime("%m/%d/%y")

        stock_data = sti.get_data(stock, start_date="01/01/2021", end_date=end_date)
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

        stock_data = stock_data.fillna('a')

        cursor.execute(sql_select_stock_with_id, stock_data['stock_id'][0])
        stock_id = cursor.fetchone()

        print(stock_data)
        print(stock_id)
        stock_data['stock_id'] = stock_id[0]

        print(stock_data)

        # ADD TO PRICE DATABASE
        for i in range(len(stock_data)):
            params = (str(stock_data['stock_id'][i]), stock_data['date'][i],
                      stock_data['open_price'][i], stock_data['close_price'][i],
                      stock_data['low_price'][i], stock_data['high_price'][i],
                      stock_data['percent_change'][i], stock_data['adjusted_close_price'][i],
                      str(stock_data['volume'][i]))
            cursor.execute(sql_insert_price, params)

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


        all_indicators = all_indicators.fillna('a')

        for i in range(len(all_indicators)):
            params = (str(all_indicators['stock_id'][i]), all_indicators['date'][i], all_indicators['sma'][i],
                      all_indicators['ema'][i], all_indicators['bb_middle'][i], all_indicators['bb_lower'][i],
                      all_indicators['bb_upper'][i], all_indicators['roc'][i], all_indicators['percent_r'][i],
                      all_indicators['p_k'][i], all_indicators['p_d'][i], all_indicators['rsi'][i])
            cursor.execute(sql_insert_indicators, params)

        # options, analyst ratings not available for past, pull most recent
        yesterday = dt.date.today() - dt.timedelta(days=1)
        start_date = yesterday.strftime("%m/%d/%y")

        calls, puts = pull_options(current_date=start_date)

        calls['stock_id'] = stock_id[0]
        puts['stock_id'] = stock_id[0]

        parsed_date = datetime.datetime.strptime(calls['date'][0], "%m/%d/%y")
        calls['date'] = parsed_date.strftime("%Y-%m-%d")
        puts['date'] = parsed_date.strftime("%Y-%m-%d")

        for i in range(len(calls)):
            params = (str(calls['stock_id'][i]), calls['date'][i], calls['expiration_date'][i], calls['option_type'][i],
                      calls['strike_price'][i], calls['bid'][i], calls['ask'][i], calls['change'][i],
                      calls['percent_change'][i], str(calls['volume'][i]), calls['open_interest'][i],
                      calls['implied_volatility'][i])
            cursor.execute(sql_insert_options, params)

        for i in range(len(puts)):
            params = (str(puts['stock_id'][i]), puts['date'][i], puts['expiration_date'][i], puts['option_type'][i],
                      puts['strike_price'][i], puts['bid'][i], puts['ask'][i], puts['change'][i],
                      puts['percent_change'][i], str(puts['volume'][i]), puts['open_interest'][i],
                      puts['implied_volatility'][i])
            cursor.execute(sql_insert_options, params)

        earnings_estimate, revenue_estimate, earnings_history = pull_analyst()

        earnings_estimate['stock_id'] = stock_id[0]
        revenue_estimate['stock_id'] = stock_id[0]
        earnings_history['stock_id'] = stock_id[0]

        for i in range(len(earnings_estimate)):
            params = (str(earnings_estimate['stock_id'][i]), earnings_estimate['data_type'][i],
                      earnings_estimate['current_qtr'][i], earnings_estimate['current_qtr_name'][i],
                      earnings_estimate['next_qtr'][i], earnings_estimate['next_qtr_name'][i],
                      earnings_estimate['current_year'][i], earnings_estimate['current_year_name'][i],
                      earnings_estimate['next_year'][i], earnings_estimate['next_year_name'][i])
            cursor.execute(sql_insert_earnings_estimate, params)

        for i in range(len(revenue_estimate)):
            params = (str(revenue_estimate['stock_id'][i]), revenue_estimate['data_type'][i],
                      revenue_estimate['current_qtr'][i], revenue_estimate['current_qtr_name'][i],
                      revenue_estimate['next_qtr'][i], revenue_estimate['next_qtr_name'][i],
                      revenue_estimate['current_year'][i], revenue_estimate['current_year_name'][i],
                      revenue_estimate['next_year'][i], revenue_estimate['next_year_name'][i])
            cursor.execute(sql_insert_revenue_estimate, params)

        for i in range(len(earnings_history)):
            params = (str(earnings_history['stock_id'][i]), earnings_history['data_type'][i],
                      earnings_history['four_back'][i], earnings_history['four_date'][i],
                      earnings_history['three_back'][i], earnings_history['three_date'][i],
                      earnings_history['two_back'][i], earnings_history['two_date'][i],
                      earnings_history['one_back'][i], earnings_history['one_date'][i])
            cursor.execute(sql_insert_earnings_history, params)

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

if __name__ == "__main__":
    connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    pull_all(cursor)

    cursor.commit()

    cursor.close()
    conn.close()

    # pull_daily()

    schedule.every().day.at("22:00").do(pull_daily)

    """
    while True:
        schedule.run_pending()
        time.sleep(600)
    """




