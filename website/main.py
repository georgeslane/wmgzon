from flask import Flask, render_template, url_for, redirect, request, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from website import database_object_initialisation as db
import secrets

# Sets up the flask login manager and secret key.
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(64)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Redirects unauthenticated users to login when they try to access a page that requires authentication.
@login_manager.unauthorized_handler
def unauthorized_callback():
    if 'login' not in request.path:
        session['next_url'] = request.path
    return redirect(url_for('login'))

# Loads the user from the session.
@login_manager.user_loader
def load_user(user_id):
    user = UserMixin()
    user.id = user_id
    return user

# Home page route.
@app.route('/')
def home():
    return render_template('home_page.html')

# Routes to the product page with the product id as a parameter.
@app.route('/product/<int:id>', methods=['GET', 'POST'])
def product(id):
   """Creares a dictionary of product page info with the following keys: 'reviews', 'matching_author_products',
   'matching_genre_products' , 'product_data' (storing the home product data) and 'category'"""
   product_dictionary = {}
   # Gets product data
   db.ProductFunctions.get_full_product(id, product_dictionary)
   # Gets product reviews
   db.ProductFunctions.get_reviews_for_product(id, product_dictionary)
   #Gets products by the same author
   db.ProductBookFunctions.view_similar_author(id, product_dictionary)
   # Gets products in the same genre
   db.ProductBookFunctions.view_similar_genre(id, product_dictionary)
   session['product_id'] = id
   # Adds product to basket if user is logged in
   if request.method == 'POST' and 'account_id' in session:
       product_id = session['product_id']
       db.BasketFunctions.add_to_basket(session['account_id'], product_id)
   elif request.method == 'POST' and 'account_id' not in session:
       return redirect(url_for('login'))
   return render_template('product_page.html', product=product_dictionary)

# Routes to the search page
@app.route('/search', methods=['POST'])
def search():
   """Creates a dictionary with two keys: 'search_results' and 'average_ratings'."""
   search_dict = {}
   search_string = request.form['search_string']
   db.SearchFunctions.search_products(search_string, search_dict)
   db.SearchFunctions.get_average_rating(search_dict['search_results'], search_dict)
   db.SearchFunctions.get_unique_values_from_search(search_dict, search_dict['search_results'])
   return render_template('search_page.html', search_results=search_dict)

# Routes to login. After login, users are redirected to the page they were trying to access before logging in.
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
            session['username'] = username
            return redirect(session.get('next_url'))
      else:
        return 'Invalid username or password'
   return render_template('login_page.html')

# Logs the user out and redirects them to the home page.
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Routes to the register page.
@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
      if request.form['password'] != request.form['confirm_password']:
         return 'Passwords do not match'
      elif len(request.form['password']) < 8:
            return 'Password must be at least 8 characters'
      else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db.AccountFunctions.add_account(username, email, "CUST", password)
        return redirect(url_for('login'))
   return render_template('register_page.html')

# Routes to the account page. Loads different pages depending on the user's permission level.
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if session['permission_id'] == 'ADMIN':
        admin_info = {}
        admin_info['username'] = session['username']
        admin_info['search_results'] = db.Product.get_all_products(db.ProductBook.level_2_table_name)
        if request.method == 'POST':
            # Allows admins to search for products
            if 'search_string' in request.form:
                search_string = request.form['search_string']
                db.SearchFunctions.search_products(search_string, admin_info)
            # Allows admins to update product discounts
            elif 'discount' in request.form:
                discount = request.form['discount']
                product_id = request.form['product_id']
                db.ProductFunctions.discount_price(product_id, float(discount))
            # Allows admins to update product stock levels
            elif 'stock' in request.form:
                stock = request.form['stock']
                product_id = request.form['product_id']
                db.ProductFunctions.restock_product(product_id, stock)
            # Allows admins to add new products
            elif 'add_product' in request.form:
                name = request.form['product_name']
                price = request.form['product_price']
                description = request.form['product_description']
                category = request.form['product_category']
                stock = request.form['product_stock']
                image = request.form['product_image']
                genre = request.form['product_genre']
                author = request.form['product_author']
                publisher = request.form['product_publisher']
                edition = request.form['product_edition']
                isbn = request.form['product_isbn']
                media_type = request.form['product_media_type']
                illustrations = request.form['product_illustrations']
                synopsis = request.form['product_synopsis']
                language = request.form['product_language']
                series_id = request.form['product_series_id']
                position_in_series = request.form['product_position_in_series']
                date_published = request.form['product_date_published']
                db.ProductBookFunctions.add_new_book(name, price, description, category, stock, image, author,
                                                     media_type, synopsis, genre, language, publisher, edition, isbn,
                                                     illustrations, series_id, position_in_series, date_published)
            return redirect(url_for('account'))
        return render_template('admin_account_page.html', admin_info=admin_info)
    else:
        # Loads customer payment and delivery method data.
        customer_info = {}
        db.PaymentMethodFunctions.get_payment_methods_for_account(session['account_id'], customer_info)
        db.DeliveryMethodFunctions.get_delivery_methods_for_account(session['account_id'], customer_info)
        customer_info['username'] = session['username']
        if request.method == 'POST':
            # Allows customers to add new payment method.
            if 'card_number' in request.form:
                card_number = request.form['card_number']
                expiry_date = request.form['expiry_date']
                cvv = request.form['security_code']
                card_name = request.form['cardholder_name']
                bank = request.form['card_provider']
                billing_address = request.form['billing_address']
                db.PaymentMethod.add_payment_method(session['account_id'], card_number, cvv, card_name, expiry_date,
                                                    billing_address, bank)
            # Allows customers to add new delivery method.
            elif 'postcode' in request.form:
                line_1 = request.form['address_line_1']
                line_2 = request.form['address_line_2']
                line_3 = request.form['address_line_3']
                postcode = request.form['postcode']
                city = request.form['city']
                country = request.form['address_country']
                db.DeliveryMethod.add_delivery_method(session['account_id'], line_1, line_2, line_3, city, country,
                                                      postcode)
        return render_template('customer_account_page.html', customer_info=customer_info)

#The delete_product page deletes a product before redirecting to the account page.
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if UserMixin.is_authenticated:
        db.Product.delete_record(product_id)
        try:
            db.ProductBook.delete_record(product_id)
        except:
            pass
        try:
            db.ProductDigitalBook.delete_record(product_id)
        except:
            pass
        try:
            db.ProductPhysicalBook.delete_record(product_id)
        except:
            pass
        return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))

# delete_card deletes a card before redirecting to the account page.
@app.route('/delete_card/<int:card_id>', methods=['POST'])
def delete_card(card_id):
    if UserMixin.is_authenticated:
        db.PaymentMethod.delete_record(card_id)
        return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))

# delete_address deletes an address before redirecting to the account page.
@app.route('/delete_address/<int:address_id>', methods=['POST'])
def delete_address(address_id):
    if UserMixin.is_authenticated:
        db.DeliveryMethod.delete_record(address_id)
        return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))

# Routes to the basket page.
@app.route('/basket', methods=['POST', 'GET'])
@login_required
def basket():
    basket = {}
    account_id = session['account_id']
    db.BasketFunctions.get_basket(account_id, basket)
    if request.method == 'POST':
        if 'remove' in request.form:
            product_id = request.form['remove']
            db.BasketFunctions.delete_from_basket(account_id, product_id)
        elif 'purchase' in request.form:
            product_id = request.form['purchase']
            db.BasketFunctions.purchase_from_basket(account_id, product_id)
    return render_template('basket_page.html', basket=basket)

# Routes to the review page, allowing users to add a review to a product.
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









