import pytest
from website import database_object_initialisation as db

class TestProduct:

    # Tests that adding a new product with an admin account adds the product to the product table.
    def test_add_new_product_0(self):
        db.ProductFunctions.add_new_product(1, 'LOTR', 10, 'Hobbits adventure', 'Book', 500, 'fdghfhgdgfh', '2020-01-01', 6, 0, 0.6)
        assert db.Product.get_record(5) == [5, 'LOTR', 10.0, 'Hobbits adventure', 'Book', 500, 'fdghfhgdgfh', '2020-01-01', 6.0, 0, 0.6]

    # Tests that adding a new product with a non admin account results in an error message.
    def test_add_new_product_1(self):
        assert db.ProductFunctions.add_new_product(2, 'Python for dummies', 30, 'Coding guidebook', 'Books', 2000, 'hdgfhdgfhdghf', '2023-02-04', 6, 0, 0.4) == "You do not have the correct permissions to add a product."


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

    # Tests that getting product by category returns a dictionry with the category as the key and a nested list of products as the value.
    def test_get_product_by_category(self):
        product_dictionary = {}
        db.ProductFunctions.get_products_by_category(1, product_dictionary)
        books = [db.Product.get_record(1), db.Product.get_record(2)]
        assert product_dictionary['Books'] == books








# cleans up from 'test_add_new_product_0'
db.Product.delete_record(5)


