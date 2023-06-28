-- Create the Stock table
CREATE TABLE Stock (
    stock_id INT PRIMARY KEY,
    stock_name VARCHAR(255)
);


-- Create the Price table
CREATE TABLE Price (
    stock_id INT,
    date DATE,
    open_price DECIMAL(18, 2),
    close_price DECIMAL(18, 2),
    low_price DECIMAL(18, 2),
    high_price DECIMAL(18, 2),
    adjusted_close_price DECIMAL(18, 2),
    volume INT,
    CONSTRAINT FK_Price_Stock FOREIGN KEY (stock_id) REFERENCES Stock(stock_id),
    CONSTRAINT PK_Price PRIMARY KEY (stock_id, date)
);


-- Create Options table
CREATE TABLE Options (
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
    CONSTRAINT FK_Options_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id),
    CONSTRAINT PK_Options PRIMARY KEY (stock_id, date, expiration_date, option_type)
);


-- Create the Indicators table
CREATE TABLE Indicators (
    stock_id INT,
    date DATE,
    sma DECIMAL(18, 2),
    ema DECIMAL(18, 2),
    bollinger_bands VARCHAR(255),
    momentum DECIMAL(18, 2),
    r_percent DECIMAL(18, 2),
    stochastic_indicator DECIMAL(18, 2),
    CONSTRAINT FK_Indicators_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id),
    CONSTRAINT PK_Indicators PRIMARY KEY (stock_id, date)
);


-- Create the Analysts table
CREATE TABLE AnalystData (
    stock_id INT,
    data_type VARCHAR(50),
    current_qtr VARCHAR(10),
    next_qtr VARCHAR(10),
    current_year VARCHAR(10),
    next_year VARCHAR(10),
    CONSTRAINT FK_AnalystData_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id),
    CONSTRAINT PK_AnalystData PRIMARY KEY (stock_id, data_type)
);


-- Create the earnings history table
CREATE TABLE EarningsHistory (
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
    CONSTRAINT FK_AnalystData_Stock FOREIGN KEY (stock_id) REFERENCES Stock (stock_id),
    CONSTRAINT PK_AnalystHistory PRIMARY KEY (stock_id)
);