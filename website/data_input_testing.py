from website import database_object_initialisation as db

# print(db.Product.search_products('T', db.ProductBook.level_2_table_name))
#
# a = (1, 2, 3,)
# print(a)
# print(list(a))
#
# db.ProductDigitalBook.add_digital_book('Harry Potter', 12, 'A tale of middle earth', 'Book',
#                                        100, 'https://m.media-amazon.com/images/I/81zqkBcTTCL._AC_UF1000,1000_QL80_.jpg'
#                                        , '2023-07-10', 8, 1000, 0.33, 'JRR Tolkien', 'Ebook',
#                                        'A brave tale of hobbits wandering through a desolate wilderness in a brave attempt to destroy a ring of power',
#                                        'Fantasy', 'English', 'HarperCollins', '1st Edition', '9780261102385', False, 0, 0, '2020-05-04', 200, 'Stephen Fry', False, 'pdf', 600)
#
# db.Product.update_record(db.Product.level_1_table_name, 3, 'product_category', 'Book')
# db.Product.update_record(db.Product.level_1_table_name, 4, 'product_category', 'Book')

# db.Account.add_account('donald_duck', '15grs@swgs.wilts.sch.uk', 'ADMIN', 'qwerty')
db.Account.add_account('kneecy', 'neece@coolmail.com', 'CUST', 'cute')
# if db.Account.compare_passwords('qwerty', db.Account.get_id_from_username('donald_duck')[0]) == True:
#     print('True')
# else:
#     print('False')

# db.PaymentMethod.add_payment_method('2', 1233321234566789, 234, 'George', '2023-07-10', '78 moon rd', 'Chase')


# db.ProductBook.update_record(db.ProductBook.level_2_table_name, 6, 'media_type', 'praperback')
# dictionary = {}
# db.BasketFunctions.get_basket(5, dictionary)
# print(dictionary['basket'])

print(db.ProductListItems.get_id_from_any_column(db.ProductListItems.product_list_items_table_name, 'product_list_id', 1))