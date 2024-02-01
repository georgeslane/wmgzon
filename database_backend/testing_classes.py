from database_backend import backend_classes as bc, database as db
import sqlite3

# book = bc.Product('Curious Anise', 10, 'A happy bunny', 'Books', 1000, 'bdbbdhdh')
#
# print(product.product_id)
#
# print(db.ProductTable.get_record(3))


# food = db.TEST_PRODUCT.add_product('Soup', 10, 'Totato and warm', 'Food', 1000, 'fdghfhgdgfh', '2020-01-01', 9, 0, 0.1)
#
# book = db.TEST_PRODUCT_PHYSICAL_BOOK.add_physical_book('Cutesy wutesy Anise', 10, 'A happy bunny', 'Books', 1000,
#                                                      'bdbbdhdh', '2020-01-01', 9, 0, 0.1, 'physical',
#                                                      'Adorable gf', 'Romance', 'English', 'Penguin',
#                                                      '1st', '978-3-16-148410-0', 'No', 1, 5, 'New', 'Hardcover', 3)
#
print(db.TEST_PRODUCT_PHYSICAL_BOOK.get_record(12))

# connection = sqlite3.connect("WMGZON.db")
# cursor = connection.cursor()
# print(cursor.execute("SELECT MAX(id) FROM TEST_PRODUCT_PHYSICAL_BOOK").fetchall())


# print(tuple(str('10' + ',')))


