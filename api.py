from flask import Flask, jsonify
import unittest
import json
import pyodbc
import datetime
import pandas as pd
import numpy as np
import time
import schedule
import datetime as dt
import re

app = Flask(__name__)

# region Set Up Database Connection
driver = 'ODBC Driver 17 for SQL Server'
server = 'MSI\SQLEXPRESS'
database = 'Stock_Information'
# endregion

# region Set Up Database Selects
sql_select_stock = "EXEC [Stock_Information].[dbo].[SelectStock]"
sql_select_price = "EXEC [Stock_Information].[dbo].[SelectPriceID] ?"
sql_select_indicator = "EXEC [Stock_Information].[dbo].[SelectIndicatorID] ?"
sql_select_option = "EXEC [Stock_Information].[dbo].[SelectOptionID] ?"
sql_select_earningsestimate = "EXEC [Stock_Information].[dbo].[SelectEarningsEstimateID] ?"
sql_select_earningshistory = "EXEC [Stock_Information].[dbo].[SelectEarningsHistoryID] ?"
sql_select_revenueestimate = "EXEC [Stock_Information].[dbo].[SelectRevenueEstimateID] ?"
# endregion


@app.route('/api/stock', methods=['GET'])
def get_stock():
    try:
        connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute(sql_select_stock)
        result = cursor.fetchall()

        # Fetch all rows as a list of dictionaries
        data = []
        for row in result:
            data.append({
                'stock_id': row.stock_id,
                'stock_name': row.stock_name,
                'stock_long_name': row.stock_long_name
            })

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/price/<stock_id>', methods=['GET'])
def get_price_id(stock_id):
    try:
        connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute(sql_select_price, stock_id)
        result = cursor.fetchall()

        # Fetch all rows as a list of dictionaries
        data = []
        for row in result:
            data.append({
                'stock_id': row.stock_id,
                'date': row.date,
                'open_price': row.open_price,
                'close_price': row.close_price,
                'low_price': row.low_price,
                'high_price': row.high_price,
                'percent_change': row.percent_change,
                'adjusted_close_price': row.adjusted_close_price,
                'volume': row.volume
            })

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/indicator/<stock_id>', methods=['GET'])
def get_indicator_id(stock_id):
    try:
        connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute(sql_select_indicator, stock_id)
        result = cursor.fetchall()

        # Fetch all rows as a list of dictionaries
        data = []
        for row in result:
            data.append({
                'stock_id': row.stock_id,
                'date': row.date,
                'sma': row.sma,
                'ema': row.ema,
                'bb_middle': row.bb_middle,
                'bb_lower': row.bb_lower,
                'bb_upper': row.bb_upper,
                'roc': row.roc,
                'r_percent': row.r_percent,
                'si_k': row.si_k,
                'si_d': row.si_d,
                'rsi': row.rsi
            })

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/option/<stock_id>', methods=['GET'])
def get_option_id(stock_id):
    try:
        connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute(sql_select_option, stock_id)
        result = cursor.fetchall()

        # Fetch all rows as a list of dictionaries
        data = []
        for row in result:
            data.append({
                'stock_id': row.stock_id,
                'date': row.date,
                'expiration_date': row.expiration_date,
                'option_type': row.option_type,
                'strike_price': row.strike_price,
                'bid': row.bid,
                'ask': row.ask,
                'change': row.change,
                'percent_change': row.percent_change,
                'volume': row.volume,
                'open_interest': row.open_interest,
                'implied_volatility': row.implied_volatility
            })

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/earningsestimate/<stock_id>', methods=['GET'])
def get_earningsestimate_id(stock_id):
    try:
        connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute(sql_select_earningsestimate, stock_id)
        result = cursor.fetchall()

        # Fetch all rows as a list of dictionaries
        data = []
        for row in result:
            data.append({
                'stock_id': row.stock_id,
                'data_type': row.data_type,
                'current_qtr': row.current_qtr,
                'current_qtr_name': row.current_qtr_name,
                'next_qtr': row.next_qtr,
                'next_qtr_name': row.next_qtr_name,
                'current_year': row.current_year,
                'current_year_name': row.current_year_name,
                'next_year': row.next_year,
                'next_year_name': row.next_year_name
            })

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/earningshistory/<stock_id>', methods=['GET'])
def get_earningshistory_id(stock_id):
    try:
        connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute(sql_select_earningshistory, stock_id)
        result = cursor.fetchall()

        # Fetch all rows as a list of dictionaries
        data = []
        for row in result:
            data.append({
                'stock_id': row.stock_id,
                'data_type': row.data_type,
                'four_back': row.four_back,
                'four_date': row.four_date,
                'three_back': row.three_back,
                'three_date': row.three_date,
                'two_back': row.two_back,
                'two_date': row.two_date,
                'one_back': row.one_back,
                'one_date': row.one_date
            })

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/revenueestimate/<stock_id>', methods=['GET'])
def get_revenueestimate_id(stock_id):
    try:
        connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute(sql_select_revenueestimate, stock_id)
        result = cursor.fetchall()

        # Fetch all rows as a list of dictionaries
        data = []
        for row in result:
            data.append({
                'stock_id': row.stock_id,
                'data_type': row.data_type,
                'current_qtr': row.current_qtr,
                'current_qtr_name': row.current_qtr_name,
                'next_qtr': row.next_qtr,
                'next_qtr_name': row.next_qtr_name,
                'current_year': row.current_year,
                'current_year_name': row.current_year_name,
                'next_year': row.next_year,
                'next_year_name': row.next_year_name
            })

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


class APITesting(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_stock(self):
        response = self.app.get('/api/stock')
        print(response)
        data = json.loads(response.data.decode('utf-8'))
        print(data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))

    def test_get_price(self):
        stock_id = 1
        response = self.app.get(f'/api/price/{stock_id}')
        print(response)
        data = json.loads(response.data.decode('utf-8'))
        print(data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        # Add more specific assertions based on the expected data format

    def test_get_indicator(self):
        stock_id = 1
        response = self.app.get(f'/api/indicator/{stock_id}')
        print(response)
        data = json.loads(response.data.decode('utf-8'))
        print(data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        # Add more specific assertions based on the expected data format

    def test_get_option(self):
        stock_id = 1
        response = self.app.get(f'/api/option/{stock_id}')
        print(response)
        data = json.loads(response.data.decode('utf-8'))
        print(data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        # Add more specific assertions based on the expected data format

    def test_get_earningsestimate(self):
        stock_id = 1
        response = self.app.get(f'/api/earningsestimate/{stock_id}')
        print(response)
        data = json.loads(response.data.decode('utf-8'))
        print(data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        # Add more specific assertions based on the expected data format

    def test_get_earningshistory(self):
        stock_id = 1
        response = self.app.get(f'/api/earningshistory/{stock_id}')
        print(response)
        data = json.loads(response.data.decode('utf-8'))
        print(data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        # Add more specific assertions based on the expected data format

    def test_get_revenueestimate(self):
        stock_id = 1
        response = self.app.get(f'/api/revenueestimate/{stock_id}')
        print(response)
        data = json.loads(response.data.decode('utf-8'))
        print(data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        # Add more specific assertions based on the expected data format


if __name__ == '__main__':
    app.run(debug=True)
    unittest.main()