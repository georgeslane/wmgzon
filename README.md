# Introduction

# Dependancies:
- Python
- flask
- flask-login
- SQLite3
- Pytest
- bcrypt

# File Structure:
The main repository contains the following folders:
- database_backend is a folder containing the files database.py (contains the classes used to initialise, update and read from the tables in the database), database_table_names.py (which initialises the tables in the database), and website_functionality.py (which contains methods to act on the database taking website inputs as arguments).
- unit_tests contains the files test_database.py (which contains unit tests for the database.py file) and test_database_backend.py (containing unit tests for the database_backend.py file).
- utils contains the file utils.py, which contains methods used to hash passwords and convert inputs to and from tuples. The methods here are used in the backend of the website.


