-- DROP AND CLEAR EVERYTHING
DROP INDEX Price.price_stock_date;
DROP INDEX Price.price_stock;
DROP INDEX Price.price_date;

DROP INDEX Options.options_stock_date_expdate;
DROP INDEX Options.options_stock;

DROP INDEX Indicators.indicators_stock ;
DROP INDEX Indicators.indicators_date;
DROP INDEX Indicators.indicators_stock_date;

DROP INDEX AnalystData.analyst_stock;
DROP INDEX EarningsHistory.earnings_stock;


DROP TABLE AnalystData;
DROP TABLE EarningsHistory;
DROP TABLE Indicators;
DROP TABLE Options;
DROP TABLE Price;
DROP TABLE Stock;

-- Create the Stock table
CREATE TABLE Stock (
    stock_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_name VARCHAR(16),
	stock_long_name VARCHAR(255),
);


-- Create the Price table
CREATE TABLE Price (
	price_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_id INT,
    date DATE,
    open_price DECIMAL(18, 2),
    close_price DECIMAL(18, 2),
    low_price DECIMAL(18, 2),
    high_price DECIMAL(18, 2),
    adjusted_close_price DECIMAL(18, 2),
    volume INT,
	CONSTRAINT FK_Price_Stock FOREIGN KEY (stock_id) REFERENCES Stock(stock_id),
);

CREATE INDEX price_stock 
ON Price(stock_id);

CREATE INDEX price_date
ON Price(date);

CREATE UNIQUE INDEX price_stock_date
ON Price(stock_id, date);



-- Create Options table
CREATE TABLE Options (
	options_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_id INT,
    date DATE,
    expiration_date DATE,
    option_type VARCHAR(10),
    strike_price DECIMAL(18, 2),
    last_price DECIMAL(18, 2),
    bid DECIMAL(18, 2),
    ask DECIMAL(18, 2),
    change DECIMAL(18, 2),
    percent_change DECIMAL(18, 2),
    volume INT,
    open_interest INT,
    implied_volatility DECIMAL(18, 2),
    CONSTRAINT FK_Options_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id)
);

CREATE INDEX options_stock 
ON Options(stock_id, date);

CREATE UNIQUE INDEX options_stock_date_expdate
ON Options(stock_id, date, expiration_date);



-- Create the Indicators table
CREATE TABLE Indicators (
	indicators_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_id INT,
    date DATE,
    sma DECIMAL(18, 2),
    ema DECIMAL(18, 2),
    bollinger_bands VARCHAR(255),
    momentum DECIMAL(18, 2),
    r_percent DECIMAL(18, 2),
    stochastic_indicator DECIMAL(18, 2),
	CONSTRAINT FK_Indicators_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id)
);

CREATE INDEX indicators_stock 
ON Indicators(stock_id);

CREATE INDEX indicators_date
ON Indicators(date);

CREATE UNIQUE INDEX indicators_stock_date
ON Indicators(stock_id, date);



-- Create the Analyst Data table
CREATE TABLE AnalystData (
	analyst_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_id INT,
    data_type VARCHAR(50),
    current_qtr VARCHAR(10),
    next_qtr VARCHAR(10),
    current_year VARCHAR(10),
    next_year VARCHAR(10),
    CONSTRAINT FK_AnalystData_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id),
);

CREATE INDEX analyst_stock 
ON AnalystData(stock_id);



-- Create the earnings history table
CREATE TABLE EarningsHistory (
	earnings_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_id INT,
    data_type VARCHAR(16),
    four_back DECIMAL(8, 2),
	four_date DATE,
    three_back DECIMAL(8, 2),
	three_date DATE,
    two_back DECIMAL(8, 2),
	two_date DATE,
    one_back DECIMAL(8, 2),
	one_date DATE,
    CONSTRAINT FK_EarningsHistory_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id),
);

CREATE INDEX earnings_stock 
ON EarningsHistory(stock_id);

-- Create the outside trends??
CREATE TABLE TrendHistory (
	trend_id INT,

)
