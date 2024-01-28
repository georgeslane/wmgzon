import sqlite3

class ProductDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("WMGZON.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS PRODUCTS (product_id INTEGER NOT NULL PRIMARY KEY, product_name VARCHAR(64),\
               base_price FLOAT, product_description CLOB, product_category VARCHAR(64),\
               quantity_in_stock INTEGER, product_image_url CLOB, date_added DATETIME,\
               price FLOAT, quantity_sold INTEGER, product_discount FLOAT)")

    def add_product(self, product_id, product_name, base_price, product_description, product_category,\
                    quantity_in_stock, product_image_url, price, quantity_sold, product_discount):
        self.cursor.execute("INSERT INTO PRODUCTS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",\
                            (product_id, product_name, base_price, product_description, product_category,\
                             quantity_in_stock, product_image_url, price, quantity_sold, product_discount))
        self.connection.commit()




product_table = ProductDatabase()









