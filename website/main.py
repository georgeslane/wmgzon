from flask import Flask, render_template, url_for, redirect, request, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from website import database_object_initialisation as db
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(64)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = UserMixin()
    user.id = user_id
    return user

@app.route('/')
def home():
    return render_template('home_page.html')


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


@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      id = db.Account.get_id_from_username(username)
      if id != 0:
        if db.Account.compare_passwords(str(password), int(db.Account.get_id_from_username(username)[0])) == True:
            user = UserMixin()
            user.id = username
            login_user(user)
            return redirect(url_for('product', id=1))
      else:
        return 'Invalid username or password'
   return render_template('login_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
      if request.form['password'] != request.form['confirm_password']:
         return 'Passwords do not match'
      else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db.Account.add_account(username, email, "CUST", password)
        return redirect(url_for('login'))
   return render_template('register_page.html')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
        return render_template('account_page.html')


@app.route('/basket')
@login_required
def basket():
   return render_template('basket_page.html')


if __name__ == '__main__':
   app.run(debug=True)









