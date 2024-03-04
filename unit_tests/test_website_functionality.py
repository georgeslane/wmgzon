import pytest
from unit_tests import prep_test_data as prep_data
from website import database_object_initialisation as db


# Adding and removing dummy products to the database for testing
def setup_module(module):
    prep_data.add_products()

def teardown_module(module):
    prep_data.remove_products()
    # cleans up from 'test_add_new_product_0'
    try:
        db.Product.delete_record(5)
    except:
        pass

class TestProduct:

    # Tests that adding a new product with an admin account adds the product to the product table.



    # Tests that incrementing stock updates the quantity sold and decreases the quantity in stock by 1.
    def test_purchase_increment_stock(self):
        quantity_in_stock = db.Product.get_record_value(db.Product.level_1_table_name, 1, 'quantity_in_stock')[0]
        quantity_sold = db.Product.get_record_value(db.Product.level_1_table_name, 1, 'quantity_sold')[0]
        db.ProductFunctions.purchase_increment_stock(1)
        assert db.Product.get_record_value(db.Product.level_1_table_name, 1, 'quantity_in_stock') == [quantity_in_stock - 1] and db.Product.get_record_value(db.Product.level_1_table_name, 1, 'quantity_sold') == [quantity_sold + 1]

    # Tests that adding a discount updates the price attribute in the database.
    def test_discount_price(self):
        discount = 0.1
        base_price = db.Product.get_record_value(db.Product.level_1_table_name, 1, 'base_price')[0]
        db.ProductFunctions.discount_price(1, discount)
        assert db.Product.get_record_value(db.Product.level_1_table_name, 1, 'price') == [base_price * (1 - discount)] and db.Product.get_record_value(db.Product.level_1_table_name, 1, 'product_discount') == [discount]

    # Tests that the 'get_reviews_for_product' function returns all reviews for a product as a nested list.
    def test_get_reviews_for_product(self):
        product_dictionary = {}
        db.ProductFunctions.get_reviews_for_product(1, product_dictionary)
        assert product_dictionary['reviews'] == [[1, 1, 1, 'Thrilling, sensational', 'This is the best book to ever grace the earth', 5, '2020-05-04']]













