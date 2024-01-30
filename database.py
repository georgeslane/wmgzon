import sqlite3

class Database:
    def __init__(self, table_name):
        self.connection = sqlite3.connect("WMGZON.db")
        self.cursor = self.connection.cursor()
        self.table_name = table_name

    def get_record(self, id):
        self.cursor.execute("SELECT * FROM " + self.table_name + " WHERE id = ?", (str(id)))
        return self.cursor.fetchone()
    def delete_record(self, id):
        self.cursor.execute("DELETE FROM " + self.table_name + " WHERE id = ?", (str(id)))
        self.connection.commit()

    def update_record(self, id, column_name, new_value):
        self.cursor.execute("UPDATE " + self.table_name + " SET ? = ? WHERE id = ?",\
                            (column_name, new_value, str(id)))
        self.connection.commit()

    #The get_new_id method returns a new and unique id for a new product.
    def get_new_id(self):
        count_id = self.cursor.execute("SELECT COUNT(*) FROM " + self.table_name).fetchall()
        cleaned_count_id = ''
        for digit in count_id:
            cleaned_count_id = cleaned_count_id + str(digit)
        if cleaned_count_id == '':
            return 1
        else:
            max_id = self.cursor.execute("SELECT MAX(id) FROM " + self.table_name).fetchall()
            cleaned_max_id = ''
            for digit in str(max_id):
                if digit not in ['(', ')', ',', ' ', '[', ']']:
                    cleaned_max_id = cleaned_max_id + str(digit)
            return int(cleaned_max_id) + 1









class ProductDatabase(Database):
    #The init method below connects to the database and creates a product table if one does not already exist.
    def __init__(self):
        super().__init__("TEST_PRODUCTS")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.table_name + " (id INTEGER NOT NULL PRIMARY KEY, product_name VARCHAR(64),\
               base_price FLOAT, product_description CLOB, product_category VARCHAR(64),\
               quantity_in_stock INTEGER, product_image_url CLOB, date_added DATETIME,\
               price FLOAT, quantity_sold INTEGER, product_discount FLOAT)")

    #The add_product method below takes product related parameters and stores them in a new row in the product table.
    def add_product(self, product_name, base_price, product_description, product_category,\
                    quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount):
        self.cursor.execute("INSERT INTO " + self.table_name + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",\
                            (super().get_new_id(), product_name, base_price, product_description, product_category,\
                             quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount))
        self.connection.commit()



ProductTable = ProductDatabase()









