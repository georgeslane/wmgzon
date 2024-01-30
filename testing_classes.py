import backend_classes as bc
import database as db

product = bc.Product('Curious Anise', 10, 'A happy bunny', 'Books', 1000, 'bdbbdhdh')

print(product.product_id)

print(db.ProductTable.get_record(3))


# class ProductDatabase:
#     #The init method below connects to the database and creates a product table if one does not already exist.
#     def __init__(self):
#         self.connection = sqlite3.connect("WMGZON.db")
#         self.cursor = self.connection.cursor()
#         self.cursor.execute("CREATE TABLE IF NOT EXISTS PRODUCTS (product_id INTEGER NOT NULL PRIMARY KEY, product_name VARCHAR(64),\
#                base_price FLOAT, product_description CLOB, product_category VARCHAR(64),\
#                quantity_in_stock INTEGER, product_image_url CLOB, date_added DATETIME,\
#                price FLOAT, quantity_sold INTEGER, product_discount FLOAT)")
#
#     #The add_product method below takes product related parameters and stores them in a new row in the product table.
#     def add_product(self, product_name, base_price, product_description, product_category,\
#                     quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount):
#         self.cursor.execute("INSERT INTO PRODUCTS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",\
#                             (ProductDatabase.get_new_id(self), product_name, base_price, product_description, product_category,\
#                              quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount))
#         self.connection.commit()
#     def get_product(self, product_id):
#         self.cursor.execute("SELECT * FROM PRODUCTS WHERE product_id = ?", (product_id,))
#         return self.cursor.fetchone()
#     def delete_product(self, product_id):
#         self.cursor.execute("DELETE FROM PRODUCTS WHERE product_id = ?", (product_id,))
#         self.connection.commit()
#
#     def update_product(self, product_id, column_name, new_value):
#         self.cursor.execute("UPDATE PRODUCTS SET ? = ? WHERE product_id = ?", (column_name, new_value, product_id))
#         self.connection.commit()
#
#     #The get_new_id method returns a new and unique id for a new product.
#     def get_new_id(self):
#         count_id = self.cursor.execute("SELECT COUNT(*) FROM PRODUCTS").fetchall()
#         cleaned_count_id = ''
#         for digit in cleaned_count_id:
#             cleaned_count_id = cleaned_count_id + str(digit)
#         if cleaned_count_id == '':
#             return 1
#         else:
#             max_id = self.cursor.execute("SELECT MAX(product_id) FROM PRODUCTS")
#             max_id = max_id.fetchall()
#             cleaned_max_id = ''
#             for digit in max_id:
#                 cleaned_max_id = cleaned_max_id + str(digit)
#             return int(cleaned_max_id) + 1
#
#
# ProductTable = ProductDatabase()