import datetime
import database_table_names as db_tables


class Product:

    def add_new_product(self, product_name, base_price, product_description, product_category,
                    quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount):
        db_tables.Product.add_product(product_name, base_price, product_description, product_category,
                    quantity_in_stock, product_image_url, date_added, price, quantity_sold, product_discount)

    def purchase_increment_stock(self, id):
        quantity_in_stock = db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, id, 'quantity_in_stock')
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, quantity_in_stock)
        quantity_sold = db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, id, 'quantity_sold')
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, quantity_sold)

    def discount_price(self, id, discount):
        base_price = db_tables.Product.get_record_value(db_tables.Product.level_1_table_name, id, 'base_price')
        price = base_price * (1 - discount)
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, 'price', price)
        db_tables.Product.update_record(db_tables.Product.level_1_table_name, id, 'product_discount', discount)

    # def get_similar_products(self):

    def add_product_to_list(self):

    def change_product_info(self, new_input):


class ProductBook(Product):
    """Inherits from Product. Contains attributes: media_type, author, synopsis, genre, language, publisher, edition,
    ISBN, illustrations, series_id, position_in_series.
    And methods: view_similar_genre, view_similar_author"""

class ProductAudiobook(ProductBook):
    """Inherits from ProductBook. Contains attributes: length, narrator, dramatised, file_format, storage_size.
    And methods: sample_audiobook"""

class ProductEBook(ProductBook):
    """Inherits from ProductBook. Contains attributes: file_format, storage_size. And methods: sample_ebook"""

class ProductPhysicalBook(ProductBook):
    """Inherits from ProductBook. Contains attributes: product_condition, product_format, shipping_date.
    And methods: get_delivery_date"""

class Review:
    """Contains attributes: review_id, account_id, product_id, review_text, review_rating, review_date.
    And methods: edit_review, delete_review, report_review"""


    def add_review(self, product_id, account_id, review_text, review_rating):
        review_date = datetime.datetime.now()
        db_tables.Review.add_review(product_id, account_id, review_text, review_rating, review_date)

    def edit_review_rating(self, id, new_rating):
        db_tables.Review.update_record(db_tables.Review.review_table_name, id, 'review_rating', new_rating)

    def edit_review_text(self, id, new_text):
        db_tables.Review.update_record(db_tables.Review.review_table_name, id, 'review_text', new_text)

    def delete_review(self, id):
        db_tables.Review.delete_record(id)

    def get_reviews_for_product(self, product_id):
        review_ids = db_tables.Review.get_id_from_any_column('product_id', product_id)
        for id in review_ids:
            db_tables.Review.get_record(id)

    def get_reviews_for_account(self, account_id):
        review_ids = db_tables.Review.get_id_from_any_column('account_id', account_id)
        for id in review_ids:
            db_tables.Review.get_record(id)

class ProductList:
    """Contains attributes: product_list_id, product_list_type, product_list_name, product_list_description,
    product_ids, account_id.
    And methods: add_product, remove_product, delete_product_list"""

    def __init__(self, product_list_type, product_list_name, product_list_description, account_id ):
        #self.product_list_id =
        self.product_list_type = product_list_type
        self.product_list_name = product_list_name
        self.product_list_description = product_list_description
        self.product_ids = []
        self.account_id = account_id

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

