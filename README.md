# Introduction
This repository contains a web application which allows users to register, login, view, add, update, delete and purchase products from an e-commerce site. The website is built using the Flask web framework and uses SQLite3 as a database server. The site can be run using the 'containerised_application' in the main directory.
# Dependancies:
- flask
- flask-login
- SQLite3
- Pytest
- bcrypt
- Bootstrap

The dependencies can be installed by running the requirements.txt file in the main directory.

# File Structure:
The main repository contains the following folders:
- database_backend is a folder containing the files: database.py (contains the classes used to initialise, update and read from the tables in the database) and website_functionality.py (which contains methods to act on the database taking website inputs as arguments).
- unit_tests contains the files test_database.py (which contains unit tests for the database.py file) and test_database_backend.py (containing unit tests for the database_backend.py file).
- utils contains the file utils.py, which contains methods used to hash passwords and convert inputs to and from tuples. The methods here are used in the backend of the website.
- website contains all files and folders used to run the web application, including html templates, css stylesheets and the main.py web app. It also contains the file which initialises database objects.

# How to run tests:
To run unit tests, navigate to the 'unit_tests' folder and run the test_database.py and test_website_functionality.py files. These files contain unit tests for some of the class methods in the database.
# How to run:
To run the website, simply navigate to the 'containerised_application' docker image and run the file. Then, navigate to 'http://127.0.0.1:5000' in your web browser.
To login, use the following credentials: 
Admin login:
- Username: donald_duck
- Password: password

User login:
- Username: micky_mouse
- Password: qwerty12345




