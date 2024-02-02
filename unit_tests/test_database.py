import pytest
from database_backend import database as db

TestProduct = db.ProductDatabase('TEST_PRODUCT')
TestProductBook = db.ProductBookDatabase('TEST_PRODUCT', 'TEST_PRODUCT_BOOK')
TestProductDigitalBook = db.ProductDigitalBookDatabase('TEST_PRODUCT', 'TEST_PRODUCT_BOOK', 'TEST_PRODUCT_DIGITAL_BOOK')
TestProductPhysicalBook = db.ProductPhysicalBookDatabase('TEST_PRODUCT', 'TEST_PRODUCT_BOOK', 'TEST_PRODUCT_PHYSICAL_BOOK')
TestAccount = db.AccountDatabase('TEST_ACCOUNT_DATABASE', 'TEST_PASSWORD_DATABASE')

class TestProductDatabase:

    def test_add_product(self):
        TestProduct.add_product('Soup', 10, 'Totato and warm', 'Food', 1000, 'fdghfhgdgfh', '2020-01-01', 9, 0, 0.1)
        assert TestProduct.get_record(1) == [(1, 'Soup', 10, 'Totato and warm', 'Food', 1000, 'fdghfhgdgfh', '2020-01-01', 9, 0, 0.1)]






