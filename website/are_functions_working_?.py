from website import database_table_names as db

# print(db.Product.search_products('T', db.ProductBook.level_2_table_name))
#
# a = (1, 2, 3,)
# print(a)
# print(list(a))

db.ProductDigitalBook.add_digital_book('LOTR', 12, 'A tale of middle earth', 'Book',
                                       100, 'https://m.media-amazon.com/images/I/81zqkBcTTCL._AC_UF1000,1000_QL80_.jpg'
                                       , '2023-07-10', 8, 1000, 0.33, 'JRR Tolkien', 'Ebook',
                                       'A brave tale of hobbits wandering through a desolate wilderness in a brave attempt to destroy a ring of power',
                                       'Fantasy', 'English', 'HarperCollins', '1st Edition', '9780261102385', False, 0, 0, '2020-05-04', 200, 'Stephen Fry', False, 'pdf', 600)
#
# db.Product.update_record(db.Product.level_1_table_name, 3, 'product_category', 'Book')
# db.Product.update_record(db.Product.level_1_table_name, 4, 'product_category', 'Book')

