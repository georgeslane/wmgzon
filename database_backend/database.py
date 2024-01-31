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
        self.cursor.execute("UPDATE " + self.table_name + " SET ? = ? WHERE id = ?",
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
    def __init__(self, table_name):
        super().__init__(table_name)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.table_name + " (id INTEGER NOT NULL PRIMARY KEY,\
               product_name VARCHAR(64), base_price FLOAT, product_description CLOB, product_category VARCHAR(64),\
               quantity_in_stock INTEGER, product_image_url CLOB, date_added DATETIME,\
               price FLOAT, quantity_sold INTEGER, product_discount FLOAT)")
        self.connection.commit()

    # The add_product method below takes product related parameters and stores them in a new row in the product table.
    def add_product(self, product_name, base_price, product_description, product_category,
                    quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount):
        self.cursor.execute("INSERT INTO " + self.table_name + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (super().get_new_id(), product_name, base_price, product_description,
                             product_category, quantity_in_stock, product_image_url, date_added, price, quantity_sold,
                             product_discount))
        self.connection.commit()


class ProductBookDatabase(ProductDatabase):
    # The init method below calls the Product class init, as well as creating a book table called 'sub_table_name'
    def __init__(self, table_name, sub_table_name):
        super().__init__(table_name)
        self.sub_table_name = sub_table_name
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.sub_table_name + " (id INTEGER NOT NULL PRIMARY KEY, \
                            media_type VARCHAR(64), synopsis CLOB, genre VARCHAR(64), language VARCHAR(64), \
                            publisher VARCHAR(64), edition VARCHAR(64), isbn CHAR(13), illustrations BOOLEAN, \
                            series_id INTEGER, position_in_series INTEGER)")
        self.connection.commit()

    """The add_book method below calls the add_product method to add a new record to the product table, before 
    adding a new record to the book table with the same id."""
    def add_book(self, product_name, base_price, product_description, product_category, quantity_in_stock,
                 product_image_url, date_added, price, quantity_sold, product_discount, media_type, synopsis, genre,
                 language, publisher, edition, isbn, illustrations, series_id, position_in_series):
        super().add_product(product_name, base_price, product_description, product_category,
                            quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount)
        self.cursor.execute("INSERT INTO " + self.sub_table_name + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            ((super().get_new_id() - 1), media_type, synopsis, genre, language, publisher,
                             edition, isbn, illustrations, series_id, position_in_series))
        self.connection.commit()


class ProductDigitalBookDatabase(ProductBookDatabase):

    def __init__(self, table_name, sub_table_name, sub_sub_table_name):
        super().__init__(table_name, sub_table_name)
        self.sub_sub_table_name = sub_sub_table_name
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.sub_sub_table_name + " (id INTEGER NOT NULL\
                            PRIMARY KEY, length INTEGER, narrator VARCHAR(64), dramatised BOOLEAN,\
                            file_format VARCHAR(64), storage_size FLOAT)")
        self.connection.commit()

    def add_digital_book(self, product_name, base_price, product_description, product_category, quantity_in_stock,
                         product_image_url, date_added, price, quantity_sold, product_discount, media_type, synopsis,
                         genre, language, publisher, edition, isbn, illustrations, series_id, position_in_series,
                         length, narrator, dramatised, file_format, storage_size):
        super().add_book(product_name, base_price, product_description, product_category, quantity_in_stock,
                         product_image_url, date_added, price, quantity_sold, product_discount, media_type, synopsis,
                         genre, language, publisher, edition, isbn, illustrations, series_id, position_in_series)
        self.cursor.execute("INSERT INTO " + self.sub_sub_table_name + " VALUES (?, ?, ?, ?, ?, ?)",
                            ((super().get_new_id() - 1), length, narrator, dramatised, file_format,
                             storage_size))
        self.connection.commit()


class ProductPhysicalBookDatabase(ProductBookDatabase):

    def __init__(self, table_name, sub_table_name, sub_sub_table_name):
        super().__init__(table_name, sub_table_name)
        self.sub_sub_table_name = sub_sub_table_name
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.sub_sub_table_name + " (id INTEGER NOT NULL\
                            PRIMARY KEY, product_condition VARCHAR(16), product_format VARCHAR(32),\
                            shipping_time INTEGER)")
        self.connection.commit()

    def add_digital_book(self, product_name, base_price, product_description, product_category, quantity_in_stock,
                         product_image_url, date_added, price, quantity_sold, product_discount, media_type, synopsis,
                         genre, language, publisher, edition, isbn, illustrations, series_id, position_in_series,
                         product_condition, product_format, shipping_time):
        super().add_book(product_name, base_price, product_description, product_category, quantity_in_stock,
                         product_image_url, date_added, price, quantity_sold, product_discount, media_type, synopsis,
                         genre, language, publisher, edition, isbn, illustrations, series_id, position_in_series)
        self.cursor.execute("INSERT INTO " + self.sub_sub_table_name + " VALUES (?, ?, ?, ?)",
                            ((super().get_new_id() - 1), product_condition, product_format, shipping_time))
        self.connection.commit()


class AccountDatabase(Database):
    def __init__(self, table_name):
        super().__init__(table_name)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.table_name + " (id INTEGER NOT NULL PRIMARY KEY, username VARCHAR(64) MOT NULL, email VARCHAR(64), permission_id VARCHAR(16)) NOT NULL")
        self.connection.commit()

    def add_account(self, username, email, permission_id):
        self.cursor.execute("INSERT INTO TABLE " + self.table_name + " VALUES (?, ?, ?, ?)", (super().get_new_id(), username, email, permission_id))
        self.connection.commit()





























# ProductTable = ProductBookDatabase('TEST_PRODUCT', 'TEST_BOOK') 
