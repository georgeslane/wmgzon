import sqlite3
# The Database class below is an abstract class, acting as a superclass for all database subclasses.
class Database:
    def __init__(self, table_name):
        self.connection = sqlite3.connect("../WMGZON.db")
        self.cursor = self.connection.cursor()
        self.table_name = table_name

    # The get_record method below takes an id (unique primary key) as an argument and returns the associated record
    def get_record(self, id):
        self.cursor.execute("SELECT * FROM " + self.table_name + " WHERE id = ?", (str(id)))
        return self.cursor.fetchone()

    # The delete_record method below takes a unique id as an argument and deletes the associated record
    def delete_record(self, id):
        self.cursor.execute("DELETE FROM " + self.table_name + " WHERE id = ?", (str(id)))
        self.connection.commit()

    # The update_record method below updates a variable column in a variable record to be a new value
    def update_record(self, id, column_name, new_value):
        self.cursor.execute("UPDATE " + self.table_name + " SET ? = ? WHERE id = ?",\
                            (column_name, new_value, str(id)))
        self.connection.commit()

    """The get_new_id function below is called when creating a new record in a table. It first checks how many records 
    are in that table. If there are 0 records, the new record is assigned an id of 1. If there are already records in
    the table, it finds the largest record id, cleans it, converts it to an integer, before iterating it to get the 
    smallest possible unique id for the new record."""
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
    # The init method below calls the superclass init method and creates a product table if one does not already exist.
    def __init__(self):
        super().__init__("TEST_PRODUCTS")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.table_name + " (id INTEGER NOT NULL PRIMARY KEY,\
               product_name VARCHAR(64), base_price FLOAT, product_description CLOB, product_category VARCHAR(64),\
               quantity_in_stock INTEGER, product_image_url CLOB, date_added DATETIME,\
               price FLOAT, quantity_sold INTEGER, product_discount FLOAT)")

    # The add_product method below takes product related parameters and stores them in a new row in the product table.
    def add_product(self, product_name, base_price, product_description, product_category,\
                    quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount):
        self.cursor.execute("INSERT INTO " + self.table_name + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",\
                            (super().get_new_id(), product_name, base_price, product_description,\
                             product_category, quantity_in_stock, product_image_url, date_added, price, quantity_sold,\
                             product_discount))
        self.connection.commit()



ProductTable = ProductDatabase()









