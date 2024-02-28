from website import database_table_names as db

# This file adds dummy data to the database for testing purposes.

db.Product.add_product('LOTR', 10, 'Hobbits adventure', 'Books', 500, 'fdghfhgdgfh', '2020-01-01', 6, 0, 0.6)

db.Product.add_product('Python for dummies', 30, 'Coding guidebook', 'Books', 2000, 'hdgfhdgfhdghf', '2023-02-04', 6, 0, 0.4)


db.ProductBook.add_book('LOTR', 12, 'A tale of middle earth', 'Book',
                                       100, 'https://m.media-amazon.com/images/I/81zqkBcTTCL._AC_UF1000,1000_QL80_.jpg'
                                       , '2023-07-10', 8, 1000, 0.33, 'JRR Tolkien', 'Ebook',
                                       'A brave tale of hobbits wandering through a desolate wilderness in a brave attempt to destroy a ring of power',
                                       'Fantasy', 'English', 'HarperCollins', '1st Edition', '9780261102385', False, 0, 0, '2020-05-04')

db.ProductDigitalBook.add_digital_book('LOTR', 12, 'A tale of middle earth', 'Book',
                                       100, 'https://m.media-amazon.com/images/I/81zqkBcTTCL._AC_UF1000,1000_QL80_.jpg'
                                       , '2023-07-10', 8, 1000, 0.33, 'JRR Tolkien', 'Ebook',
                                       'A brave tale of hobbits wandering through a desolate wilderness in a brave attempt to destroy a ring of power',
                                       'Fantasy', 'English', 'HarperCollins', '1st Edition', '9780261102385', False, 0, 0, '2020-05-04', 200, 'Stephen Fry', False, 'pdf', 600)

db.Account.add_account('donald_duck', '15grs@swgs.wilts.sch.uk', 'ADMIN', 'qwerty')

db.Account.add_account('micky_mouse', '15abc@swgs.wilts.sch.uk', 'CUST', 'qwerty12345')

db.Review.add_review(1, 1, 'Thrilling, sensational', 'This is the best book to ever grace the earth', 5, '2020-05-04')