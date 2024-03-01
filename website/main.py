from flask import Flask, render_template, url_for, redirect, request, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from website import database_object_initialisation as db
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(64)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.unauthorized_handler
def unauthorized_callback():
    if 'login' not in request.path:
        session['next_url'] = request.path
    return redirect(url_for('login'))

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
   session['product_id'] = id

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
        if db.Account.compare_passwords(str(password), int(id[0])) == True:
            user = UserMixin()
            user.id = username
            login_user(user)
            session['permission_id'] = db.Account.get_record_value(db.Account.account_table_name, id[0], 'permission_id')[0]
            session['account_id'] = id[0]
            return redirect(session.get('next_url'))
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
    if session['permission_id'] == 'ADMIN':
        return render_template('account_page.html')
    else:
        customer_info = {}
        db.PaymentMethodFunctions.get_payment_methods_for_account(session['account_id'], customer_info)
        return render_template('customer_account_page.html', customer_info=customer_info)


@app.route('/basket')
@login_required
def basket():
   return render_template('basket_page.html')


@app.route('/review', methods=['POST', 'GET'])
@login_required
def review():
    if request.method == 'POST':
        review_heading = request.form['review_heading']
        review_text = request.form['review_text']
        rating = request.form['rating']
        product_id = session['product_id']
        account_id = session['account_id']
        db.ReviewFunctions.add_review(product_id, account_id, review_heading, review_text, rating)
        return redirect(url_for('product', id=product_id))
    return render_template('review_page.html')




if __name__ == '__main__':
   app.run(debug=True)









