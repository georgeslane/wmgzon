import _sqlite3
import datetime

class Product:

    def __init__(self, product_id, name, base_price, description, category, quantity_in_stock, image_url):
        self.product_id = product_id
        self.name = name
        self.base_price = base_price
        self.description = description
        self.category = category
        self.quantity_in_stock = quantity_in_stock
        self.image_url = image_url
        self.date_added = datetime.datetime.now()
        self.price = self.base_price * (1 - self.discount)

    quantity_sold = 0
    discount = 0
    product_tags = []

    def purchase_increment_stock(self):
        self.quantity_sold += 1
        self.quantity_in_stock -= 1
    def calculate_discounted_price(self):
        self.price = self.base_price * (1 - self.discount)
    def apply_discount(self, discount):
        self.discount = discount
    def add_tags(self, tag):
        self.product_tags.append(tag)
    def get_similar_products(self):
        #Add a method to the Product class that returns a list of similar products.
    def get_reviews(self):
        #Add a method to the Product class that returns a list of reviews.
    def add_product_to_list(self):
        #Add a method to the Product class that adds a product to the list of products.
    def change_product_info(self, new_input):
        #Add a method to the Product class that changes the information of a product.


