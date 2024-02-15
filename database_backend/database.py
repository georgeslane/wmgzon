import sqlite3
from utils import database_utils


"""The Database class below is an abstract class, acting as a superclass for all database subclasses. 
It contains methods for getting records, updating records, deleting records and getting ids for new records."""


class Database:

    """The init method below connects to the database and stores the table name as an attribute.
    It also creates an SqlReader object, which inherits from database_utils.SqliteReader.
    This object stores methods for converting data types and other database utilities."""
    def __init__(self, table_name):
        self.connection = sqlite3.connect("WMGZON.db")
        self.cursor = self.connection.cursor()
        self.table_name = table_name
        self.SqlReader = database_utils.SqliteReader()

    """The get_record method below takes an id (unique primary key) as an argument and returns the associated record 
    from the table denoted by 'self.table_name'."""
    def get_record(self, id):
        try:
            self.cursor.execute("SELECT * FROM " + self.table_name + " WHERE id = ?", (self.SqlReader.convert_to_tuple(id)))
            result = self.cursor.fetchall()
            return self.SqlReader.convert_from_tuple(result)
        except IndexError:
            'The inputted ID does not exist in the table'

    """The method below gets all ids from a table, where a particular column matches a particular value. """
    def get_id_from_any_column(self, column_name, value):
        self.cursor.execute("SELECT id FROM " + self.table_name + " WHERE " + column_name + " = ?", (self.SqlReader.convert_to_tuple(value)))
        results = self.cursor.fetchall()
        results = self.SqlReader.convert_from_plural_tuples(results)
        return results

    """The delete_record method below takes a unique id as an argument and 
    deletes the record with that id from 'self.table_name'."""
    def delete_record(self, id):
        self.cursor.execute("DELETE FROM " + self.table_name + " WHERE id = ?", self.SqlReader.convert_to_tuple(id))
        self.connection.commit()

    """The update_record method below updates a specific value in the selected table. 
    The value is determined by the 'column_name' and 'id' parameters."""
    def update_record(self, table_name, id, column_name, new_value):
        if column_name == 'id':
            raise Exception('Cannot change the id of a record')
        else:
            self.cursor.execute("UPDATE " + table_name + " SET " + column_name + " = ? WHERE id = ?",
                                (new_value, id))
            self.connection.commit()

    """The method below gets a specific value from a record in a table."""
    def get_record_value(self, table_name, id, column_name):
        self.cursor.execute("SELECT " + column_name + " FROM " + table_name + " WHERE id = ?", (self.SqlReader.convert_to_tuple(id)))
        result = self.cursor.fetchall()
        return self.SqlReader.convert_from_tuple(result)


    """The get_new_id function below is called when creating a new record in a table. It first checks how many records 
    are in that table. If there are 0 records, the new record is assigned an id of 1. If there are already records in
    the table, it finds the largest record id, cleans it, converts it to an integer, before iterating it to get the 
    smallest possible unique id for the new record."""
    def get_new_id(self, table_name):
        count_id = self.cursor.execute("SELECT COUNT(*) FROM " + table_name).fetchall()
        cleaned_count_id = ''
        for digit in count_id:
            if digit not in ['(', ')', ',', ' ', '[', ']']:
                cleaned_count_id = cleaned_count_id + str(digit)
        if cleaned_count_id == '(0,)':
            return 1
        else:
            max_id = self.cursor.execute("SELECT MAX(id) FROM " + table_name).fetchall()
            cleaned_max_id = ''
            for digit in str(max_id):
                if digit not in ['(', ')', ',', ' ', '[', ']']:
                    cleaned_max_id = cleaned_max_id + str(digit)
            return int(cleaned_max_id) + 1


class ProductDatabase(Database):

    """The init method below calls the superclass init method and creates a product table containing the
    following attributes: id, product_name, base_price, product_description, product_category, quantity_in_stock,
    product_image_url, data_added, price, quantity_sold, product_discount."""
    def __init__(self, level_1_table_name):
        self.level_1_table_name = level_1_table_name
        super().__init__(level_1_table_name)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.level_1_table_name + " (id INTEGER NOT NULL \
                PRIMARY KEY, product_name VARCHAR(64), base_price FLOAT, product_description CLOB, product_category \
                VARCHAR(64), quantity_in_stock INTEGER, product_image_url CLOB, date_added DATETIME,\
                price FLOAT, quantity_sold INTEGER, product_discount FLOAT)")
        self.connection.commit()

    """The add_product method below takes product related parameters and 
    stores them in a new row in the product table."""
    def add_product(self, product_name, base_price, product_description, product_category,
                    quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount):
        self.cursor.execute("INSERT INTO " + self.level_1_table_name + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (super().get_new_id(self.level_1_table_name), product_name, base_price,
                             product_description, product_category, quantity_in_stock, product_image_url, date_added,
                             price, quantity_sold, product_discount,))
        self.connection.commit()


class ProductBookDatabase(ProductDatabase):

    """The init method below calls the ProductDatabase class initialisation method for the product table, before
    storing the Product and ProductBook table names as 'level_1_table_name' and 'level_2_table_name' respectively.
    It then creates a new ProductBook table, with attributes: id, media_type, synopsis, genre, language, publisher,
    edition, isbn, illustrations, series_id and position_in_series."""
    def __init__(self, level_1_table_name, level_2_table_name):
        super().__init__(level_1_table_name)
        self.level_1_table_name = level_1_table_name
        self.level_2_table_name = level_2_table_name
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.level_2_table_name + " (id INTEGER NOT NULL \
                            PRIMARY KEY, media_type VARCHAR(64), synopsis CLOB, genre VARCHAR(64), language \
                            VARCHAR(64), publisher VARCHAR(64), edition VARCHAR(64), isbn CHAR(13), illustrations \
                            BOOLEAN, series_id INTEGER, position_in_series INTEGER)")
        self.connection.commit()

    """The add_book method below calls the add_product method from the ProductDatabase class to add a new record to the 
    product table, before also adding a new record to the book table with the same id."""
    def add_book(self, product_name, base_price, product_description, product_category, quantity_in_stock,
                 product_image_url, date_added, price, quantity_sold, product_discount, media_type, synopsis, genre,
                 language, publisher, edition, isbn, illustrations, series_id, position_in_series):
        super().add_product(product_name, base_price, product_description, product_category,
                            quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount)
        self.cursor.execute("INSERT INTO " + self.level_2_table_name + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            ((super().get_new_id(self.level_1_table_name) - 1), media_type, synopsis, genre,
                             language, publisher, edition, isbn, illustrations, series_id, position_in_series))
        self.connection.commit()

    """The get_record method below overwrites the get_record method from the Database class. 
    It returns the joined record from the Product and ProductBook tables."""
    def get_record(self, id):
        try:
            self.cursor.execute("SELECT * FROM " + self.level_1_table_name + " INNER JOIN\
             " + self.level_2_table_name + " ON " + self.level_1_table_name + ".id=\
             " + self.level_2_table_name + ".id  WHERE " + self.level_1_table_name + ".id = ?",
                            (self.SqlReader.convert_to_tuple(id)))
            result = self.cursor.fetchall()
            return self.SqlReader.convert_from_tuple(result)

        except IndexError:
            'The inputted ID does not exist in the table'

    """The delete_record method below overwrites the delete_record method from the Database class. 
    It deletes records of the same id from both the Product and ProductBook tables."""
    def delete_record(self, id):
        self.cursor.execute("DELETE FROM " + self.level_1_table_name + " WHERE id = ?",
                            self.SqlReader.convert_to_tuple(id))
        self.cursor.execute("DELETE FROM " + self.level_2_table_name + " WHERE id = ?",
                            self.SqlReader.convert_to_tuple(id))
        self.connection.commit()


class ProductDigitalBookDatabase(ProductBookDatabase):

    """The init method below calls the ProductBookDatabase class initialisation method for the Product and ProductBooks
    tables, before storing the Product, ProductBook and ProductDigitalBook table names as 'level_1_table_name',
    'level_2_table_name' and 'level_3_table_name' respectively. It then creates a new ProductDigitalBook table, with
    attributes: id, length, narrator, dramatised, file_format and storage_size."""
    def __init__(self, level_1_table_name, level_2_table_name, level_3_table_name):
        super().__init__(level_1_table_name, level_2_table_name)
        self.level_3_table_name = level_3_table_name
        self.level_2_table_name = level_2_table_name
        self.level_1_table_name = level_1_table_name
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.level_3_table_name + " (id INTEGER NOT NULL\
                            PRIMARY KEY, length INTEGER, narrator VARCHAR(64), dramatised BOOLEAN,\
                            file_format VARCHAR(64), storage_size FLOAT)")
        self.connection.commit()

    """The add_digital_book method below calls the add_book method from the ProductBookDatabase class to add a new 
    record to the Product and ProductBook tables, before also adding a new record to the ProductDigitalBook table with 
    the same id."""
    def add_digital_book(self, product_name, base_price, product_description, product_category, quantity_in_stock,
                         product_image_url, date_added, price, quantity_sold, product_discount, media_type, synopsis,
                         genre, language, publisher, edition, isbn, illustrations, series_id, position_in_series,
                         length, narrator, dramatised, file_format, storage_size):
        super().add_book(product_name, base_price, product_description, product_category, quantity_in_stock,
                         product_image_url, date_added, price, quantity_sold, product_discount, media_type, synopsis,
                         genre, language, publisher, edition, isbn, illustrations, series_id, position_in_series)
        self.cursor.execute("INSERT INTO " + self.level_3_table_name + " VALUES (?, ?, ?, ?, ?, ?)",
                            ((super().get_new_id(self.level_1_table_name) - 1), length, narrator,
                             dramatised, file_format, storage_size))
        self.connection.commit()

    """The get_record method below overwrites the get_record method from the Database class. 
    It returns the joined record from the Product, ProductBook and ProductDigitalBook tables."""
    def get_record(self, id):
        self.cursor.execute("SELECT * FROM " + self.level_1_table_name + " INNER JOIN " + self.level_2_table_name + " \
        ON " + self.level_1_table_name + ".id=" + self.level_2_table_name + ".id INNER JOIN \
        " + self.level_3_table_name + " ON " + self.level_1_table_name + ".id=" + self.level_3_table_name + ".id \
        WHERE " + self.level_1_table_name + ".id = ?", (self.SqlReader.convert_to_tuple(id)))
        return self.cursor.fetchall()

    """The delete_record method below overwrites the delete_record method from the Database class. 
    It deletes records of the same id from both the Product, ProductBook and ProductDigitalBook tables."""
    def delete_record(self, id):
        self.cursor.execute("DELETE FROM " + self.level_1_table_name + " WHERE id = ?",
                            self.SqlReader.convert_to_tuple(id))
        self.cursor.execute("DELETE FROM " + self.level_2_table_name + " WHERE id = ?",
                            self.SqlReader.convert_to_tuple(id))
        self.cursor.execute("DELETE FROM " + self.level_3_table_name + " WHERE id = ?",
                            self.SqlReader.convert_to_tuple(id))
        self.connection.commit()


class ProductPhysicalBookDatabase(ProductBookDatabase):

    """The init method below calls the ProductBookDatabase class initialisation method for the Product and ProductBooks
    tables, before storing the Product, ProductBook and ProductPhysicalBook table names as 'level_1_table_name',
    'level_2_table_name' and 'level_3_table_name' respectively. It then creates a new ProductPhysicalBook table, with
    attributes: id, product_condition, product_format and shipping_time."""
    def __init__(self, level_1_table_name, level_2_table_name, level_3_table_name):
        super().__init__(level_1_table_name, level_2_table_name)
        self.level_3_table_name = level_3_table_name
        self.level_2_table_name = level_2_table_name
        self.level_1_table_name = level_1_table_name
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.level_3_table_name + " (id INTEGER NOT NULL\
                            PRIMARY KEY, product_condition VARCHAR(16), product_format VARCHAR(32),\
                            shipping_time INTEGER)")
        self.connection.commit()

    """The add_physical_book method below calls the add_book method from the ProductBookDatabase class to add a new 
    record to the Product and ProductBook tables, before also adding a new record to the ProductPhysicalBook table with 
    the same id."""
    def add_physical_book(self, product_name, base_price, product_description, product_category, quantity_in_stock,
                          product_image_url, date_added, price, quantity_sold, product_discount, media_type, synopsis,
                          genre, language, publisher, edition, isbn, illustrations, series_id, position_in_series,
                          product_condition, product_format, shipping_time):
        super().add_book(product_name, base_price, product_description, product_category, quantity_in_stock,
                         product_image_url, date_added, price, quantity_sold, product_discount, media_type, synopsis,
                         genre, language, publisher, edition, isbn, illustrations, series_id, position_in_series)
        self.cursor.execute("INSERT INTO " + self.level_3_table_name + " VALUES (?, ?, ?, ?)",
                            ((super().get_new_id(self.level_1_table_name) - 1), product_condition,
                             product_format, shipping_time))
        self.connection.commit()

    """The get_record method below overwrites the get_record method from the Database class. 
    It returns the joined record from the Product, ProductBook and ProductPhysicalBook tables."""
    def get_record(self, id):
        self.cursor.execute("SELECT * FROM " + self.level_1_table_name + " INNER JOIN " + self.level_2_table_name + " \
        ON " + self.level_1_table_name + ".id=" + self.level_2_table_name + ".id INNER JOIN \
        " + self.level_3_table_name + " ON " + self.level_1_table_name + ".id=" + self.level_3_table_name + ".id \
        WHERE " + self.level_1_table_name + ".id = ?", (self.SqlReader.convert_to_tuple(id)))
        return self.cursor.fetchall()

    """The delete_record method below overwrites the delete_record method from the Database class. 
    It deletes records of the same id from both the Product, ProductBook and ProductPhysicalBook tables."""
    def delete_record(self, id):
        self.cursor.execute("DELETE FROM " + self.level_1_table_name + " WHERE id = ?",
                            self.SqlReader.convert_to_tuple(id))
        self.cursor.execute("DELETE FROM " + self.level_2_table_name + " WHERE id = ?",
                            self.SqlReader.convert_to_tuple(id))
        self.cursor.execute("DELETE FROM " + self.level_3_table_name + " WHERE id = ?",
                            self.SqlReader.convert_to_tuple(id))
        self.connection.commit()


class AccountDatabase(Database):

    """The init method below stores the account table and password table names as attributes, before calling the
    superclass initialisation method on the account table. It then creates the account table (containing attributes:
    id, username, email and permission_id) and password table (containing attributes: id and hashed_password).
    Finally, it creates an AccountSecurity object, which inherits from database_utils.AccountSecurity, and stores
    methods for hashing passwords and comparing them to stored passwords."""
    def __init__(self, account_table_name, password_table_name):
        self.account_table_name = account_table_name
        self.password_table_name = password_table_name
        super().__init__(account_table_name)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.account_table_name + " (id INTEGER NOT NULL \
        PRIMARY KEY, username VARCHAR(64) NOT NULL, email VARCHAR(64), permission_id VARCHAR(16) NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.password_table_name + " \
        (id INTEGER NOT NULL PRIMARY KEY, hashed_passwords VARCHAR(64) NOT NULL)")
        self.connection.commit()
        self.AccountSecurity = database_utils.AccountSecurity()

    """The add_account method below inserts a new record into the account table and password table when called."""
    def add_account(self, username, email, permission_id, password):
        self.cursor.execute("INSERT INTO " + self.table_name + " VALUES (?, ?, ?, ?)",
                            (super().get_new_id(self.account_table_name), username, email, permission_id))
        self.cursor.execute("INSERT INTO " + self.password_table_name + " VALUES (?, ?)",
                            (super().get_new_id(self.account_table_name) - 1,
                             self.AccountSecurity.hash_password(password,
                                                                super().get_new_id(self.account_table_name) - 1)))
        self.connection.commit()

    """The get_id_from_username method below takes a username as argument and returns the database id associated 
    with that username."""
    def get_id_from_username(self, username):
        self.cursor.execute("SELECT id FROM " + self.account_table_name + " WHERE username = ?",
                            (self.SqlReader.convert_to_tuple(username)))
        result = self.cursor.fetchall()
        return self.SqlReader.convert_from_tuple(result)

    """The delete_record method below overwrites the delete_record method from the Database class, altering it to 
    delete the record from both the account and password tables."""
    def delete_record(self, id):
        self.cursor.execute("DELETE FROM " + self.account_table_name + " WHERE id = ?",
                            self.SqlReader.convert_to_tuple(id))
        self.cursor.execute("DELETE FROM " + self.password_table_name + " WHERE id = ?",
                            self.SqlReader.convert_to_tuple(id))
        self.connection.commit()

    """The compare_passwords method below takes a password and id as arguments and returns True only if the hashed and 
    salted password argument matches the stored hashed_password in the password table."""
    def compare_passwords(self, password, id):
        stored_password = self.cursor.execute("SELECT hashed_passwords FROM " + self.password_table_name + "WHERE id = \
        ?", self.SqlReader.convert_to_tuple(id))
        if stored_password == self.AccountSecurity.hash_password(password, id):
            return True
        else:
            return False


class PaymentMethodDatabase(Database):

    """The init method below stores the payment table name as an attribute, before calling the superclass
    initialisation method on the payment table name, and then creates a new payment table if one does not exist,
    with attributes: id, account_id, card_number, security_code, card_holder_name, expiry_date, billing_address
    and bank_name."""
    def __init__(self, payment_table_name):
        self.payment_table_name = payment_table_name
        super().__init__(payment_table_name)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.payment_table_name + " (id INTEGER NOT NULL \
        PRIMARY KEY, account_id INTEGER NOT NULL, card_number CHAR(16) NOT NULL, security_code CHAR(3) NOT NULL, \
        card_holder_name VARCHAR(64) NOT NULL, expiry_date DATE NOT NULL, billing_address CLOB NOT NULL, bank_name \
        VARCHAR(64) NOT NULL)")
        self.connection.commit()

    """The add_payment method below inserts a new record into the payment table when called."""
    def add_payment_method(self, account_id, card_number, security_code, card_holder_name, expiry_date, billing_address,
                           bank_name):
        self.cursor.execute("INSERT INTO " + self.payment_table_name + " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (super().get_new_id(self.payment_table_name), account_id, card_number,
                             security_code, card_holder_name, expiry_date, billing_address, bank_name))
        self.connection.commit()


class DeliveryMethodDatabase(Database):

    """The init method below stores the delivery table name as an attribute, before calling the init method of the
    superclass on the delivery table name. It then creates a new delivery table, with attributes: id, account_id,
    address_line_1, address_line_2, address_line_3, address_city, address_country and address_postcode."""
    def __init__(self, delivery_table_name):
        self.delivery_table_name = delivery_table_name
        super().__init__(delivery_table_name)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.delivery_table_name + " (id INTEGER NOT NULL \
        PRIMARY KEY, account_id INTEGER NOT NULL, address_line_1 VARCHAR(64) NOT NULL, address_line_2 VARCHAR(64), \
        address_line_3 VARCHAR(64), address_city VARCHAR(64) NOT NULL, address_country VARCHAR(64) NOT NULL, \
        address_postcode CHAR(8) NOT NULL)")
        self.connection.commit()

    """The add_delivery_method method below inserts a new record into the delivery table when called."""
    def add_delivery_method(self, account_id, address_line_1, address_line_2, address_line_3, address_city,
                            address_country, address_postcode):
        self.cursor.execute("INSERT INTO " + self.delivery_table_name + " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (super().get_new_id(self.delivery_table_name), account_id, address_line_1,
                             address_line_2, address_line_3, address_city, address_country, address_postcode))
        self.connection.commit()


class ReviewDatabase(Database):

    """The init method below stores the review table as an attribute, calls the superclass init method on it, and
    creates a table with its name with attributes: id, product_id, account_id, review_text, review_rating and
    review_date."""
    def __init__(self, review_table_name):
        self.review_table_name = review_table_name
        super().__init__(review_table_name)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.review_table_name + " (id INTEGER NOT NULL \
        PRIMARY KEY, product_id INTEGER NOT NULL, account_id INTEGER NOT NULL, review_text CLOB, review_rating INTEGER \
        NOT NULL, review_date DATE)")
        self.connection.commit()

    """The add_review method inserts a new record into the review_table when called."""
    def add_review(self, product_id, account_id, review_text, review_rating, datetime):
        self.cursor.execute("INSERT INTO " + self.review_table_name + " VALUES (?, ?, ?, ?, ?, ?)",
                            (self.get_new_id(self.review_table_name), product_id, account_id, review_text,
                             review_rating, datetime))
        self.connection.commit()


class ProductListDatabase(Database):

    """The init method below stores the product list table name as an attribute, calls the superclass init method on it,
    and creates a table containing the following attributes: id, account_id, list_type, list_name and
    list_description."""
    def __init__(self, product_list_table_name):
        self.product_list_table_name = product_list_table_name
        super().__init__(product_list_table_name)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.product_list_table_name + " (id INTEGER NOT NULL \
        PRIMARY KEY, account_id INTEGER, list_type VARCHAR(32), list_name VARCHAR(64), list_description CLOB)")
        self.connection.commit()

    """The add_product_list method inserts a new record into the product list table when called."""
    def add_product_list(self, account_id, list_type, list_name, list_description):
        self.cursor.execute("INSERT INTO " + self.product_list_table_name + " VALUES(?,?,?,?,?)",
                            (self.get_new_id(self.product_list_table_name), account_id, list_type,
                             list_name, list_description))
        self.connection.commit()


class ProductListItemsDatabase(Database):

    """The init method below creates a table containing the following attributes: id, product_list_id and product_id.
    Every record is a unique combination of product_id and product_list_id."""
    def __init__(self, product_list_items_table_name):
        self.product_list_items_table_name = product_list_items_table_name
        super().__init__(product_list_items_table_name)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.product_list_items_table_name + " (id INTEGER \
        NOT NULL PRIMARY KEY, product_list_id INTEGER NOT NULL, product_id INTEGER NOT NULL)")
        self.connection.commit()

    def add_product_to_list(self, product_list_id, product_id):
        self.cursor.execute("INSERT INTO " + self.product_list_items_table_name + " VALUES(?,?,?)",
                            (self.get_new_id(self.product_list_items_table_name), product_list_id,
                             product_id))
        self.connection.commit()
































