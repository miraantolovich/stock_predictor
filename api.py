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
        # Add more specific assertions based on the expected data format

if __name__ == '__main__':
    app.run(debug=True)
    unittest.main()