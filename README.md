# Financial Data Dashboard

![Dashboard Screenshot](/images/sofi-basic.png)
![Dashboard Screenshot](/images/intc-basic.png)
![Dashboard Screenshot](/images/aal-indicators.png)
![Dashboard Screenshot](/images/cwh-indicators.png)

Welcome to the Financial Data Dashboard project! This project was conceived and developed as a solo effort to provide a comprehensive and interactive platform for visualizing various financial indicators and data, including candle charts, line charts, Bollinger Bands, Simple Moving Averages (SMA), Exponential Moving Averages (EMA), volume, Relative Strength Index (RSI), %R, Stochastic Oscillator, Rate of Change (ROC), earnings estimates, revenue estimates, earnings history, and options chain data.

## Features

- **Candle Chart:** Visualize the historical price movements of a financial instrument with candlestick charts. They provide insights into price open, close, high, and low for a specific time period. Traders and investors use candlestick patterns to identify potential trend reversals and market sentiment.

- **Line Chart:** Plot financial data over time using line charts to spot trends and patterns.

- **Bollinger Bands:** Bollinger Bands are essential for analyzing volatility and price levels. They consist of a simple moving average (SMA) and upper and lower bands based on standard deviations. When prices move outside these bands, it can signal potential price reversals or breakouts, aiding in timing investment decisions.

- **SMA and EMA:** Simple Moving Averages (SMA) and Exponential Moving Averages (EMA) are key indicators for understanding price trends. They smooth out price data over a specified period, making it easier to identify trend direction and potential trend changes.

- **Volume:** Trading volume is crucial in determining the liquidity and interest in a financial instrument. High volume often indicates increased market participation and potentially more accurate price movements.

- **RSI, %R, Stochastic Oscillator, ROC:** These technical indicators are valuable tools for assessing overbought or oversold conditions and identifying potential price reversals. They help traders and investors make informed decisions by analyzing the momentum and strength of a trend.

- **Earnings Estimate:** Earnings estimates are essential for assessing the future profitability of a company. They are used by investors to gauge the potential returns on their investments and make decisions about buying or selling stocks.

- **Revenue Estimate:** Revenue estimates provide insight into a company's expected sales and income. They are crucial for understanding a company's financial health and growth potential.

- **Earnings History:** Historical earnings data is valuable for evaluating a company's performance over time. It allows investors to track how a company has met or missed earnings expectations and make investment decisions based on this track record.

- **Options Chain:** The options chain data is critical for options traders and investors. It provides information about available options contracts, their strike prices, and expiration dates. Knowing which options have the most volume can be essential for understanding market sentiment and potential trading opportunities. The website displays not only the option with the highest trading volume but also the three options with strike prices both above and below this prominent option.

## Data Source

This financial data dashboard utilizes the `yahoo_fin` library to fetch data from Yahoo Finance. The `yahoo_fin` library allowed me to obtain financial data, including stock prices, options, and analyst data.

## Technology Stack

- **Front-end:** This dashboard is built using Angular.

- **Back-end:** The back-end is powered by SQL Server.

- **RESTful Python API:** A custom Python API was developed to communicate with the normalized SQL database via T-SQL stored procedures. This API serves as a bridge between the front-end and the database, ensuring seamless data retrieval and interaction.
