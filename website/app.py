import secrets
from flask import Flask, render_template, url_for, redirect, request
from website import database_table_names as db
import json
from forms import ProductForm
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(64)
@app.route('/product/<int:id>')
def product(id):

   """Creares a dictionary of product page info with the following keys: 'reviews', 'matching_author_products', 'matching_genre_products' , 'product_data' (storing the home product data) and 'category'"""
   product_dictionary = {}
   db.ProductFunctions.get_full_product(id, product_dictionary)
   db.ProductFunctions.get_reviews_for_product(id, product_dictionary)
   db.ProductBookFunctions.view_similar_author(id, product_dictionary)
   db.ProductBookFunctions.view_similar_genre(id, product_dictionary)

   return render_template('product_page.html', product=product_dictionary)


@app.route('/search', methods=['POST'])
def search():

   """Creates a dictionary with two keys: 'search_results' and 'average_ratings'."""
   search_dict = {}
   search_string = request.form['search_string']
   db.SearchFunctions.search_products(search_string, search_dict)
   db.SearchFunctions.get_average_rating(search_dict['search_results'], search_dict)
   db.SearchFunctions.get_unique_values_from_search(search_dict, search_dict['search_results'])

   return render_template('search_page.html', search_results=search_dict)


if __name__ == '__main__':
   app.run(debug=True)


