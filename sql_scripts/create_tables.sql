-- DROP AND CLEAR EVERYTHING
DROP INDEX Price.price_stock_date;
DROP INDEX Price.price_stock;
DROP INDEX Price.price_date;

DROP INDEX Options.options_stock_date_expdate;
DROP INDEX Options.options_stock;

DROP INDEX Indicators.indicators_stock ;
DROP INDEX Indicators.indicators_date;
DROP INDEX Indicators.indicators_stock_date;

DROP INDEX EarningsEstimate.earnings_estimate_stock;
DROP INDEX EarningsHistory.earnings_stock;
DROP INDEX RevenueEstimate.revenue_estimate_stock;

DROP TABLE EarningsHistory;
DROP TABLE EarningsEstimate;
DROP TABLE RevenueEstimate;

DROP TABLE Indicators;
DROP TABLE Options;
DROP TABLE Price;
DROP TABLE Stock;


-- Create the Stock table
CREATE TABLE Stock (
    stock_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_name VARCHAR(16) UNIQUE,
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
    	percent_change DECIMAL(18, 2),
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
    	strike_price VARCHAR(10),
    	bid VARCHAR(10),
    	ask VARCHAR(10),
    	change VARCHAR(10),
    	percent_change VARCHAR(10),
    	volume VARCHAR(10),
    	open_interest VARCHAR(10),
    	implied_volatility VARCHAR(10),
    	CONSTRAINT FK_Options_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id)
);

CREATE INDEX options_stock 
ON Options(stock_id, date);

CREATE UNIQUE INDEX options_stock_date_expdate
ON Options(stock_id, date, option_type, expiration_date, strike_price);



-- Create the Indicators table
CREATE TABLE Indicators (
	indicators_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_id INT,
    date DATE,
    sma DECIMAL(18, 2) NULL,
    ema DECIMAL(18, 2) NULL,
    bb_middle DECIMAL(18, 2) NULL,
	bb_lower DECIMAL(18, 2) NULL,
	bb_upper DECIMAL(18, 2) NULL,
    roc DECIMAL(18, 2) NULL,
    r_percent DECIMAL(18, 2) NULL,
    si_k DECIMAL(18, 2) NULL,
	si_d DECIMAL(18, 2) NULL,
	rsi DECIMAL(18, 2) NULL,
	CONSTRAINT FK_Indicators_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id)
);

CREATE INDEX indicators_stock 
ON Indicators(stock_id);

CREATE INDEX indicators_date
ON Indicators(date);

CREATE UNIQUE INDEX indicators_stock_date
ON Indicators(stock_id, date);



-- Create the Analyst Data table
CREATE TABLE EarningsEstimate (
	earnings_estimate_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_id INT,
	data_order INT,
    date VARCHAR(32),
	average VARCHAR(16),
    low VARCHAR(16),
	high VARCHAR(16),
    CONSTRAINT FK_EarningsEstimate_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id),
);

CREATE INDEX earnings_estimate_stock 
ON EarningsEstimate(stock_id);


-- Create the Analyst Data table
CREATE TABLE RevenueEstimate (
	analyst_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_id INT,
	data_order INT,
    date VARCHAR(32),
	average VARCHAR(16),
    low VARCHAR(16),
	high VARCHAR(16),
	CONSTRAINT FK_RevenueEstimate_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id),
);

CREATE INDEX revenue_estimate_stock 
ON RevenueEstimate(stock_id);

-- Create the earnings history table
CREATE TABLE EarningsHistory (
	earnings_id INT IDENTITY(1,1) PRIMARY KEY,
    stock_id INT,
	data_order INT,
    year VARCHAR(32),
	average VARCHAR(16),
    actual VARCHAR(16),
	difference VARCHAR(16),
    CONSTRAINT FK_EarningsHistory_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id),
);

CREATE INDEX earnings_stock 
ON EarningsHistory(stock_id);