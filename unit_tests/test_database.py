from unit_tests import prep_test_data as prep_data
from website import database_object_initialisation as db_tables
import pytest

# Adding and removing dummy products to the database for testing
def setup_module(module):
    prep_data.add_products()

def teardown_module(module):
    prep_data.remove_products()

class TestProductDatabase:

    # Testing the get_record method
    def test_get_record(self):
        assert db_tables.Product.get_record(1) == [1, 'LOTR', 10.0, 'Hobbits adventure', 'Books', 500, 'fdghfhgdgfh', '2020-01-01', 6.0, 0, 0.6]

    #Testing delete_record returns 0 when record is deleted
    def test_delete_record(self):
        db_tables.Product.add_product('Bible', 15, 'Holy book', 'Books', 1000, 'fdghfhgdgfh', '2020-01-01', 9, 100,
                                      0.4)
        db_tables.Product.delete_record(5)
        assert db_tables.Product.get_record(5) == 0

    # Testing get_id_from_any_column method returns a list of matching ids
    def test_get_id_from_any_column_1(self):
        id = db_tables.Product.get_id_from_any_column(db_tables.Product.level_1_table_name, 'product_name', 'LOTR')
        assert id == [1, 3, 4]

    # Testing get_id_from_any_column method returns a list of matching ids
    def test_get_id_from_any_column_2(self):
        id = db_tables.Product.get_id_from_any_column(db_tables.Product.level_1_table_name, 'quantity_in_stock', 2000)
        assert id == [2]

    # Testing updating a record works
    def test_update_record(self):
        db_tables.Product.update_record('TEST_PRODUCT', 1, 'product_name', 'Charlie and the chocolate factory')
        assert db_tables.Product.get_record(1) == [1, 'Charlie and the chocolate factory', 10.0, 'Hobbits adventure', 'Books', 500, 'fdghfhgdgfh', '2020-01-01', 6.0, 0, 0.6]

    # Testing get record value returns the specified value as a list
    def test_get_record_value(self):
        assert db_tables.Product.get_record_value('TEST_PRODUCT', 1, 'product_category') == ['Books']

class TestProductBookDatabase:

    # Testing get_record returns a joined record when called using the ProductBook object
    def test_get_record(self):
        assert db_tables.ProductBook.get_record(3) == [3, 'LOTR', 12.0, 'A tale of middle earth', 'Book',
                                       100, 'https://m.media-amazon.com/images/I/81zqkBcTTCL._AC_UF1000,1000_QL80_.jpg'
                                       , '2023-07-10', 8.0, 1000, 0.33, 3, 'JRR Tolkien', 'Ebook',
                                       'A brave tale of hobbits wandering through a desolate wilderness in a brave attempt to destroy a ring of power',
                                       'Fantasy', 'English', 'HarperCollins', '1st Edition', '9780261102385',0 , 0,
                                                       0, '2020-05-04']

    # Testing delete_record returns 0 from both tables when a book record is deleted
    def test_delete_record(self):
        db_tables.ProductBook.delete_record(3)
        assert db_tables.Product.get_record(3) == 0 and db_tables.ProductBook.get_record(3) == 0


class TestAccountDatabase:

    # Testing function returns the correct id as a list when called with a valid username
    def test_get_id_from_username(self):
        assert db_tables.Account.get_id_from_username('donald_duck') == [1]

