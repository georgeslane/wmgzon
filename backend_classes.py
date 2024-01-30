import datetime
import database
class Product:
    """Contains attributes: product_id, product_name, product_base_price, product_description, product_category,
    product_quantity_in_stock, product_image_url,product_date_added, product_price.
    And methods: purchase_increment_stock, calculate_discounted_price, apply_discount, add_tags,get_similar_products,
    get_reviews, add_product_to_list, change_product_info."""

    def __init__(self, name, base_price, description, category, quantity_in_stock, image_url):
        self.product_id = database.ProductTable.get_new_id()
        self.product_name = name
        self.product_base_price = base_price
        self.product_description = description
        self.product_category = category
        self.product_quantity_in_stock = quantity_in_stock
        self.product_image_url = image_url
        self.product_date_added = datetime.datetime.now()
        self.product_price = self.product_base_price * (1 - self.product_discount)
        database.ProductTable.add_product(self.product_name, self.product_base_price, self.product_description,\
                                          self.product_category, self.product_quantity_in_stock,\
                                          self.product_image_url, self.product_date_added, self.product_price, self.product_quantity_sold,\
                                          self.product_discount)

    product_quantity_sold = 0
    product_discount = 0
    product_tags = []

    def purchase_increment_stock(self):
        self.product_quantity_sold += 1
        self.product_quantity_in_stock -= 1
    def calculate_discounted_price(self):
        self.product_price = self.product_base_price * (1 - self.product_discount)
    def apply_discount(self, discount):
        self.product_discount = discount
    def add_tags(self, tag):
        self.product_tags.append(tag)
    # def get_similar_products(self):
    #     #Add a method to the Product class that returns a list of similar products.
    # def get_reviews(self):
    #     #Add a method to the Product class that returns a list of reviews.
    # def add_product_to_list(self):
    #     #Add a method to the Product class that adds a product to the list of products.
    # def change_product_info(self, new_input):
    #     #Add a method to the Product class that changes the information of a product.

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

    def __init__(self, account_id, product_id, review_text, review_rating):
        self.account_id = account_id
        self.product_id = product_id
        self.review_text = review_text
        self.review_rating = review_rating
        self.review_date = datetime.datetime.now()
        self.review_id = self.account_id + self.product_id
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

