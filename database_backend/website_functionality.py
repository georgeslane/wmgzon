import datetime
from website import database_table_names as db_tables


class Product:

    """The 'add_new_product' method adds a new product to the database if the adding account has the
    correct permissions."""
    def add_new_product(self, account_id, product_name, base_price, product_description, product_category,
                        quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount):
        permissions = db_tables.Account.get_record_value(db_tables.Account.account_table_name, account_id,
                                                         'permission_id')
        if permissions == ['ADMIN']:
            db_tables.Product.add_product(product_name, base_price, product_description, product_category,
                                          quantity_in_stock, product_image_url, date_added, price, quantity_sold,
                                          product_discount)
        else:
            return 'You do not have the correct permissions to add a product.'

    """The purchase_increment_stock method decreases the quantity of stock in the database by one and increments the 
    quantity sold by one. It should be called each time a product is purchased."""
    def purchase_increment_stock(self, id):
        quantity_in_stock = db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, id, 'quantity_in_stock')
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, quantity_in_stock)
        quantity_sold = db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, id, 'quantity_sold')
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, quantity_sold)

    """The discount_price_method takes a discount value as an argument and uses it to calculate a new product price 
    before updating the product price in the database."""
    def discount_price(self, id, discount):
        base_price = db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, id, 'base_price')
        price = base_price * (1 - discount)
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, 'price', price)
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, 'product_discount', discount)

    """The get_reviews_for_product method returns all reviews for a given product in the form of a for loop that 
    returns each review as a list."""
    def get_reviews_for_product(self, product_id, dictionary):
        review_ids = db_tables.Review.get_id_from_any_column(db_tables.Review.table_name, 'product_id', (product_id,))
        reviews = []
        for review_id in review_ids:
            reviews.append(db_tables.Review.get_record(review_id))
        dictionary['reviews'] = reviews
        return dictionary


    """The get_products_by_category method returns other products that are in the same category as the 
    product it is called on."""
    def get_products_by_category(self, product_id):
        category = db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, product_id,
                                                      'product_category')
        product_ids = db_tables.Product.get_id_from_any_column(db_tables.Product.level_1_table_name,
                                                               'product_category', category)
        products = []
        for id in product_ids:
            products.append(db_tables.Product.get_record(id))
            return products

    """The add_product_to_list method adds the product it is called on to a specified product list."""
    def add_product_to_list(self, product_id, list_id):
        db_tables.ProductListItems.add_product_to_list(list_id, product_id)


    """get_full_product returns a dictionary containing the product type as well as product data from the relevent product tables."""
    def get_full_product(self, id, dictionary):
        if db_tables.Product.get_record(id)[4].lower() == "book":
            if db_tables.ProductBook.get_record(id)[13].lower() == "physical" or db_tables.ProductBook.get_record(id)[13].lower() == "paperback" or db_tables.ProductBook.get_record(id)[13].lower() == "hardcover":
                product = db_tables.ProductPhysicalBook.get_record(id)
                category = 'physical_book'
            elif db_tables.ProductBook.get_record(id)[13].lower() == "digital" or db_tables.ProductBook.get_record(id)[
                13].lower() == "ebook":
                product = db_tables.ProductDigitalBook.get_record(id)
                category = 'digital_book'
            else:
                product = db_tables.ProductBook.get_record(id)
                category = 'other_book'
        else:
            product = db_tables.Product.get_record(id)
            category = 'other'
        dictionary['category'] = category
        dictionary['product_data'] = product
        return dictionary


class ProductBook(Product):
    """Inherits from Product. Contains attributes: media_type, author, synopsis, genre, language, publisher, edition,
    ISBN, illustrations, series_id, position_in_series.
    And methods: view_similar_genre, view_similar_author"""
    def add_new_book(self, account_id, product_name, base_price, product_description, product_category,
                     quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount, author,
                     media_type, synopsis, genre, language, publisher, edition, isbn, illustrations, series_id,
                     position_in_series, date_published):
        permissions = db_tables.Account.get_record_value(db_tables.Account.account_table_name, account_id,
                                                         'permission_id')
        if permissions == ['ADMIN']:
            db_tables.ProductBook.add_book(product_name, base_price, product_description, product_category,
                                           quantity_in_stock, product_image_url, date_added, price, quantity_sold,
                                           product_discount, author, media_type, synopsis, genre, language, publisher, edition,
                                           isbn, illustrations, series_id, position_in_series, date_published)
        else:
            return 'You do not have the correct permissions to add a product.'

    def view_similar_genre(self, id, dictionary):
        genre = db_tables.ProductBook.get_record_value(db_tables.ProductBook.level_2_table_name, id, 'genre')
        if genre != 0:
            product_ids = db_tables.ProductBook.get_id_from_any_column(db_tables.ProductBook.level_2_table_name, 'genre',
                                                                   genre)
            products = []
            for product_id in product_ids:
                product = db_tables.ProductBook.get_record(product_id)
                products.append(product)
            dictionary['matching_genre_products'] = products
        else:
            dictionary['matching_genre_products'] = ['null']
        return dictionary



    def view_similar_author(self, id, dictionary):
        author = db_tables.ProductBook.get_record_value(db_tables.ProductBook.level_2_table_name, id, 'author')
        if author != 0:
            product_ids = db_tables.ProductBook.get_id_from_any_column(db_tables.ProductBook.level_2_table_name, 'author',
                                                                   author)
            products = []
            for product_id in product_ids:
                product = db_tables.ProductBook.get_record(product_id)
                products.append(product)
            dictionary['matching_author_products'] = products
        else:
            dictionary['matching_author_products'] = ['null']
        return dictionary

    def view_others_in_series(self, id):
        list_of_products = []
        sorted_list_of_products = []
        series_id = db_tables.ProductBook.get_record_value(db_tables.ProductBook.level_2_table_name, id, 'series_id')
        product_ids = db_tables.ProductBook.get_id_from_any_column(db_tables.ProductBook.level_2_table_name,
                                                                   'series_id', series_id)
        for product_id in product_ids:
            book = db_tables.ProductBook.get_record(product_id)
            list_of_products.append(book)
            sorted_list_of_products.append([''])

        for product in list_of_products:
            sorted_list_of_products[int(product[22])] = product

        return sorted_list_of_products






class Review:
    """Contains attributes: review_id, account_id, product_id, review_text, review_rating, review_date.
    And methods: edit_review, delete_review, report_review"""


    def add_review(self, product_id, account_id, review_header, review_text, review_rating):
        review_date = datetime.datetime.now()
        db_tables.Review.add_review(product_id, account_id, review_header, review_text, review_rating, review_date)

    def edit_review_rating(self, id, new_rating):
        db_tables.Review.update_record(db_tables.Review.review_table_name, id, 'review_rating', new_rating)

    def edit_review_text(self, id, new_text):
        db_tables.Review.update_record(db_tables.Review.review_table_name, id, 'review_text', new_text)

    def delete_review(self, id):
        db_tables.Review.delete_record(id)

    def get_reviews_for_account(self, account_id):
        review_ids = db_tables.Review.get_id_from_any_column(db_tables.Review.review_table_name, 'account_id', account_id)
        for id in review_ids:
            db_tables.Review.get_record(id)

class ProductList:
    """Contains attributes: product_list_id, product_list_type, product_list_name, product_list_description,
    product_ids, account_id.
    And methods: add_product, remove_product, delete_product_list"""

    # def __init__(self, product_list_type, product_list_name, product_list_description, account_id ):
    #     #self.product_list_id =
    #     self.product_list_type = product_list_type
    #     self.product_list_name = product_list_name
    #     self.product_list_description = product_list_description
    #     self.product_ids = []
    #     self.account_id = account_id

class Basket(ProductList):
    """Inherits from ProductList. Contains method: purchase_basket"""

class Account:
    """Contains attributes: account_id, account_username, account_password, account_email, account_permission_id.
    And methods: secure_password"""

class AccountCustomer(Account):
    """Inherits from Account. Contains methods: get_payment_methods, create_payment_methods, get_delivery_methods,
    create_delivery_method, create_review, contact_us, get_product_lists """

class AccountAdmin(Account):
    """Inherits from Account. Contains methods: add_product, view_analytics, view_messages"""

class PaymentMethod:
    """Contains attributes: payment_method_id, payment_method_card_number, payment_method_card_security_code,
    payment_method_card_holder_name, payment_method_card_holder_expiry_date, payment_method_card_provider, account_id.
    And methods: edit_payment_method, delete_payment_method"""

class DeliveryMethod:
    """Contains attributes: delivery_method_id, delivery_method_address_line_1, delivery_method_address_line_2,
    delivery_method_address_line_3, delivery_method_address_city, delivery_method_address_country,
    delivery_method_address_postcode, account_id.
    And methods: edit_delivery_method, delete_delivery_method"""

class Search:

    def get_average_rating(self, products, dictionary):
        average_ratings = []
        for product in products:
            temporary_review_dict = {}
            db_tables.ProductFunctions.get_reviews_for_product(product[0], temporary_review_dict)
            reviews = temporary_review_dict['reviews']
            review_count = 0
            review_sum = 0
            if len(reviews) > 0:
                for review in reviews:
                    review_sum += review[5]
                    review_count += 1
                average_ratings.append([[product[0]], [int(round(review_sum/review_count))]])
            else:
                average_ratings.append([[product[0]], [0]])
        dictionary['average_ratings'] = average_ratings
        return dictionary

    def search_products(self, search_string, dictionary):
        search_results = db_tables.ProductBook.search_products(search_string, db_tables.ProductBook.level_2_table_name)
        dictionary['search_results'] = search_results
        return dictionary



