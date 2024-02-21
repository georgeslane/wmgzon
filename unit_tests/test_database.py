from website import database_table_names as db_tables

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

class TestProductBookDatabase:

    def add_book(self):
        db_tables.ProductBook.add_book('The BFG', 12, 'The big friendly giant', 'Book', 23, 'dfhagfdgsjfgdjsfg', '2024-01-01', 5, 67, 0.1, 'electronic', 'A story about a giant who turns good', 'Fantasy', 'English', 'Random house', '1st', 1232343454567, False, 34, 5)

    def test_get_record(self):
        self.add_book()
        assert db_tables.ProductBook.get_record(3) == [3, 'The BFG', 12.0, 'The big friendly giant', 'Book', 23, 'dfhagfdgsjfgdjsfg', '2024-01-01', 5.0, 67, 0.1, 3, 'electronic', 'A story about a giant who turns good', 'Fantasy', 'English', 'Random house', '1st', '1232343454567', 0, 34, 5]

    def test_delete_record(self):
        db_tables.ProductBook.delete_record(3)
        assert db_tables.Product.get_record(3) == None and db_tables.ProductBook.get_record(3) == None


class TestAccountDatabase:

    def add_account(self):
        db_tables.Account.add_account('donald_duck', 'duckling4ever@gmail.com', 'CUST', 'qwerty')

    def test_get_id_from_username(self):
        self.add_account()
        assert db_tables.Account.get_id_from_username(1) == 'donald_duck'

