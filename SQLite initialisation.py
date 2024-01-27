import sqlite3

connection = sqlite3.connect("WMGZON.db")

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS PRODUCTS (product_id INTEGER NOT NULL PRIMARY KEY, product_name VARCHAR(64),\
               product_base_price FLOAT, product_description CLOB, product_category VARCHAR(64),\
               product_quantity_in_stock INTEGER, product_image_url CLOB, product_date_added DATETIME,\
               product_price FLOAT, product_quantity_sold INTEGER, product_discount FLOAT)")

cursor.execute("INSERT INTO PRODUCTS VALUES (2, 'GS', 2.99, 'A book', 'Book', 10, 'www.google.com', '2020-10-10', 2.99, 0, 0.0)")

print(connection.total_changes)