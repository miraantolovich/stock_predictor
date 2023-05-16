import requests
import pandas as pd

import yahoo_fin.options as ops
import yahoo_fin.stock_info as sti

# medium (monthly plays) to medium/large-cap stocks

# analyst rating
# insider trading/purchases

api_key = "D24NAEA1UVN44M2E"
symbol = "AAPL"

url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
    print(data['Time Series (Daily)'])
else:
    print("Error occurred while retrieving stock information.")



# expiration_dates = ops.get_expiration_dates("aapl")
# print(expiration_dates)
# 
# get_calls = ops.get_calls("aapl")
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# print(get_calls)
# 
# get_calls = ops.get_puts("aapl")
# print(get_calls)

get_all = ops.get_options_chain("aapl")
print(get_all)


get_analyst = sti.get_analysts_info("aapl")
print(get_analyst)


# get list of all stocks to compare

# for each stock, every 24 hours:
    # pull stock data:
    # open, high, low, close, adjusted close, volume
    # options chain
    #
    # calculate SMA, EMA, BB... RSI, %R, SO, M
    # 
    # put all into database