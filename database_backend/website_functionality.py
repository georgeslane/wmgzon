from datetime import datetime
from website import database_object_initialisation as db_tables


class Product:
    """The purchase_increment_stock method decreases the quantity of stock in the database by one and increments the 
    quantity sold by one. It should be called each time a product is purchased."""
    def purchase_increment_stock(self, id):
        quantity_in_stock = int(db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, id,
                                                                   'quantity_in_stock')[0])
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, 'quantity_in_stock',
                                        quantity_in_stock - 1)
        quantity_sold = int(db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, id,
                                                               'quantity_sold')[0])
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, 'quantity_sold',
                                        quantity_sold + 1)

    """The discount_price_method takes a discount value as an argument and uses it to calculate a new product price 
    before updating the net product price in the database. It is called whenever an admin applies a product discount."""
    def discount_price(self, id, discount):
        base_price = int(db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, id, 'base_price')[0])
        price = base_price * (1 - discount)
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, 'price', price)
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, 'product_discount', discount)

    """The get_reviews_for_product method returns all reviews for a given product in the form of a for loop that 
    returns each review as a list. It outputs a dictionary containing a nested kist of reviews."""
    def get_reviews_for_product(self, product_id, dictionary):
        review_ids = db_tables.Review.get_id_from_any_column(db_tables.Review.table_name, 'product_id', product_id)
        reviews = []
        for review_id in review_ids:
            reviews.append(db_tables.Review.get_record(review_id))
        dictionary['reviews'] = reviews
        return dictionary

    """The get_products_by_category method returns other products that are in the same category as the 
    product it is called on. It outputs a dictionary containing a nested list of products."""
    def get_products_by_category(self, product_id, dictionary):
        # gets the category of the product corresponding to the product_id
        category = db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, product_id,
                                                      'product_category')[0]
        # gets a list of product ids that are in the same category as the product
        product_ids = db_tables.Product.get_id_from_any_column(db_tables.Product.level_1_table_name,
                                                               'product_category', category)
        category = str(category[0])
        products = []
        # runs a for loop to get product records for each product id in the list of product ids.
        for id in product_ids:
            products.append(db_tables.Product.get_record(id))
        dictionary[category] = products
        return dictionary

    """get_full_product returns a dictionary containing the product type as well as product data from the relevent 
    product tables."""
    def get_full_product(self, id, dictionary):
        # checks if product is a book
        if db_tables.Product.get_record(id)[4].lower() == "book":
            # if product is book, checks if book is physical, if it is, gets the physical book data
            if (db_tables.ProductBook.get_record(id)[13].lower() == "physical" or
                    db_tables.ProductBook.get_record(id)[13].lower() == "paperback" or
                    db_tables.ProductBook.get_record(id)[13].lower() == "hardcover"):
                product = db_tables.ProductPhysicalBook.get_record(id)
                category = 'physical_book'
            # if book is digital, gets the digital book data
            elif (db_tables.ProductBook.get_record(id)[13].lower() == "digital" or
                  db_tables.ProductBook.get_record(id)[13].lower() == "ebook"):
                product = db_tables.ProductDigitalBook.get_record(id)
                category = 'digital_book'
            else:
                product = db_tables.ProductBook.get_record(id)
                category = 'other_book'
        # if product is not a book, only returns data from the product table.
        else:
            product = db_tables.Product.get_record(id)
            category = 'other'
        dictionary['category'] = category
        dictionary['product_data'] = product
        return dictionary

    """'restock_product' allows admin users to update the stock of a product in the database."""
    def restock_product(self, id, quantity):
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, 'quantity_in_stock', quantity)


class ProductBook(Product):
    """'add_new_book' adds a new book to the database, passing arguments to the add_book method in the 
    database module."""
    def add_new_book(self, product_name, base_price, product_description, product_category,
                     quantity_in_stock, product_image_url, author,
                     media_type, synopsis, genre, language, publisher, edition, isbn, illustrations, series_id,
                     position_in_series, date_published):

        db_tables.ProductBook.add_book(product_name, base_price, product_description, product_category,
                                           quantity_in_stock, product_image_url, datetime.now(), base_price, 0,
                                           0, author, media_type, synopsis, genre, language, publisher, edition,
                                           isbn, illustrations, series_id, position_in_series, date_published)

    """Returns a dictionary containing a nested list of products that are in the same genre as the product the 
    function is called on."""
    def view_similar_genre(self, id, dictionary):
        genre = db_tables.ProductBook.get_record_value(db_tables.ProductBook.level_2_table_name, id, 'genre')[0]
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

    """Returns a dictionary containing a nested list of products that are by the same author as the product the 
    function is called on"""
    def view_similar_author(self, id, dictionary):
        author = db_tables.ProductBook.get_record_value(db_tables.ProductBook.level_2_table_name, id, 'author')[0]
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

class Review:
    """'add_review' adds a new review to the database, passing the current date to the add_review method in the
    database"""
    def add_review(self, product_id, account_id, review_header, review_text, review_rating):
        review_date = datetime.now()
        db_tables.Review.add_review(product_id, account_id, review_header, review_text, review_rating, review_date)

    """Allows users to edit their review rating. Not currently implemented in the website."""
    def edit_review_rating(self, id, new_rating):
        db_tables.Review.update_record(db_tables.Review.review_table_name, id, 'review_rating', new_rating)

    """Allows users to edit their review text. Not currently implemented in the website."""
    def edit_review_text(self, id, new_text):
        db_tables.Review.update_record(db_tables.Review.review_table_name, id, 'review_text', new_text)

    """Allows users to delete their review. Not currently implemented in the website."""
    def delete_review(self, id):
        db_tables.Review.delete_record(id)

    """Gets all reviews written by a specific account."""
    def get_reviews_for_account(self, account_id):
        review_ids = db_tables.Review.get_id_from_any_column(db_tables.Review.review_table_name, 'account_id', account_id)
        for id in review_ids:
            db_tables.Review.get_record(id)

class ProductList:
    pass
class Basket(ProductList):
    """Inherits from ProductList. Contains method: purchase_basket"""

class PaymentMethod:
    """Gets all payment methods for a specific account. Outputs as a dictionary containing a nested list."""
    def get_payment_methods_for_account(self, account_id, dictionary):
        payment_ids = db_tables.PaymentMethod.get_id_from_any_column(db_tables.PaymentMethod.payment_table_name, 'account_id', account_id)
        payment_methods = []
        for id in payment_ids:
            payment_methods.append(db_tables.PaymentMethod.get_record(id))
        dictionary['payment_methods'] = payment_methods
        return dictionary

class DeliveryMethod:
    """Gets all delivery methods for a specific account. Outputs as a dictionary containing a nested list."""
    def get_delivery_methods_for_account(self, account_id, dictionary):
        delivery_ids = db_tables.DeliveryMethod.get_id_from_any_column(db_tables.DeliveryMethod.delivery_table_name, 'account_id', account_id)
        delivery_methods = []
        for id in delivery_ids:
            delivery_methods.append(db_tables.DeliveryMethod.get_record(id))
        dictionary['delivery_methods'] = delivery_methods
        return dictionary

class Search:
    """Gets the average rating for a product.
    It is used to calculate the average rating for each product in the search page.
    It outputs a dictionary containing a nested list of product ids and their average ratings."""
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

    """search_products returns a dictionary containing a nested list of products that match the search string."""
    def search_products(self, search_string, dictionary):
        search_results = db_tables.ProductBook.search_products(search_string, db_tables.ProductBook.level_2_table_name)
        dictionary['search_results'] = search_results
        return dictionary

    """Gets unique values for several product attributes. It is used to populate the search filters pane."""
    def get_unique_values_from_search(self, dictionary, products):
        product_categories = []
        product_genres = []
        product_media_types = []
        product_languages = []
        product_author = []
        for product in products:
            product_categories.append(product[4])
            product_genres.append(product[10])
            product_media_types.append(product[9])
            product_languages.append(product[11])
            product_author.append(product[8])
        product_categories = list(set(product_categories))
        product_genres = list(set(product_genres))
        product_media_types = list(set(product_media_types))
        product_languages = list(set(product_languages))
        product_author = list(set(product_author))
        dictionary['unique_categories'] = product_categories
        dictionary['unique_genres'] = product_genres
        dictionary['unique_media_types'] = product_media_types
        dictionary['unique_languages'] = product_languages
        dictionary['unique_authors'] = product_author