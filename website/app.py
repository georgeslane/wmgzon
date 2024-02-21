from flask import Flask, render_template
from website import database_table_names as db
import json

# db.ProductPhysicalBook.add_physical_book("The Alchemist", 12.99, "A philosophical novel about a shepherd named Santiago who travels from Spain to Egypt in search of a treasure.", "Book", 150, "https://m.media-amazon.com/images/I/81fiotccNCL._AC_UF894,1000_QL80_.jpg", "2023-07-10", 9.99, 700, 0.23, "Paulo Coelho", "Paperback", "The Alchemist follows Santiago, a young shepherd who dreams of finding treasure. Along the journey, he learns about life, love, and the importance of following one's dreams.", "Fiction, Philosophy", "English", "HarperOne", "25th Anniversary Edition", "9780062315007", False, 0, 0, "2020-05-04", "New", "Mass Market Paperback", 4, 600)
db.Review.add_review(1, 1, "This book is great", "This is a life changing experience", 3, "2020-04-04")


app = Flask(__name__)

@app.route('/')
def home():
   id = 1
   category = ""
   if db.Product.get_record(id)[4].lower() == "book":
      if db.ProductBook.get_record(id)[13].lower() == "physical" or db.ProductBook.get_record(id)[13].lower() == "paperback" or db.ProductBook.get_record(id)[13].lower() == "hardcover":
         product = db.ProductPhysicalBook.get_record(id)
         category = 'physical_book'
      elif db.ProductBook.get_record(id)[13].lower() == "digital" or db.ProductBook.get_record(id)[13].lower() == "ebook":
         product = db.ProductDigitalBook.get_record(id)
         category = 'digital_book'
      else:
         product = db.ProductBook.get_record(id)
         category = 'other_book'
   else:
      product = db.Product.get_record(id)
      category = 'other'
   product_dict = {'product': product}

   reviews = db.ProductFunctions.get_reviews_for_product(id)
   reviews_dict = {'reviews': reviews}

   same_authors_count = 'not_empty'
   same_genre_count = 'not_empty'

   same_author_products = db.ProductBookFunctions.view_similar_author(id)
   same_author_products_dict = {'same_author_products': same_author_products}
   if same_author_products == ['null']:
      same_authors_count = 'empty'
   same_genre_products = db.ProductBookFunctions.view_similar_genre(id)
   same_genre_products_dict = {'same_genre_products': same_genre_products}
   if same_genre_products == ['null']:
      same_genre_count = 'empty'


   return render_template('product_page.html', product=product, product_dict=product_dict, category=category,
                          reviews=reviews_dict, same_author=same_author_products_dict,
                          same_genre=same_genre_products_dict, same_genre_count=same_genre_count,
                          same_authors_count=same_authors_count)
if __name__ == '__main__':
   app.run(debug=True)


