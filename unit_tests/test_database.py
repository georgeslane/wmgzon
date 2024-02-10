import pytest
from database_backend import database_table_names as db_tables
import os

db_tables.Product.delete_record(1)
db_tables.Product.delete_record(2)

class TestProductDatabase:

    def test_add_product(self):
        db_tables.Product.add_product('LOTR', 10, 'Hobbits adventure', 'Fiction', 500, 'fdghfhgdgfh', '2020-01-01', 6, 0, 0.6)
        db_tables.Product.add_product('Python for dummies', 30, 'Coding guidebook', 'Knowledge', 2000, 'hdgfhdgfhdghf', '2023-02-04', 6, 0, 0.4)
        assert db_tables.Product.get_record(1) == [1, 'LOTR', 10, 'Hobbits adventure', 'Fiction', 500, 'fdghfhgdgfh', '2020-01-01', 6, 0, 0.6]

    def test_get_record(self):
        assert db_tables.Product.get_record(1) == [1, 'LOTR', 10, 'Hobbits adventure', 'Fiction', 500, 'fdghfhgdgfh', '2020-01-01', 6, 0, 0.6]

    def test_delete_record(self):
        db_tables.Product.add_product('Bible', 15, 'Holy book', 'Books', 1000, 'fdghfhgdgfh', '2020-01-01', 9, 100,
                                      0.4)
        db_tables.Product.delete_record(3)
        assert db_tables.Product.get_record(3) == None

    def test_get_id_from_any_column_1(self):
        id = db_tables.Product.get_id_from_any_column('product_name', 'LOTR')
        assert id == [1]

    def test_get_id_from_any_column_2(self):
        id = db_tables.Product.get_id_from_any_column('quantity_in_stock', 2000)
        assert id == [2]

    def test_get_id_from_any_column_3(self):
        id = db_tables.Product.get_id_from_any_column('price', 6)
        assert id == [1, 2]

    def test_update_record(self):
        db_tables.Product.update_record('TEST_PRODUCT', 1, 'product_name', 'Harry Potter')
        assert db_tables.Product.get_record(1) == [1, 'Harry Potter', 10, 'Hobbits adventure', 'Fiction', 500, 'fdghfhgdgfh', '2020-01-01', 6, 0, 0.6]

    def test_get_record_value(self):
        assert db_tables.Product.get_record_value('TEST_PRODUCT', 1, 'product_category') == ['Fiction']





