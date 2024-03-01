import bcrypt
import random
import string
class SqliteReader():

    """The method below converts any single value input into a tuple of size 1"""
    def convert_to_tuple(self, input):
        return (input,)

    """The method below converts any tuple of size n stored inside a list of size 1 into a list of size n, with each 
    element of the list coresponding to an element of the tuple."""
    def convert_from_tuple(self, input):
        try:
            input = list(input[0])
            return input
        except IndexError:
            return 0

    """The following method takes a list of size n, containing tuples, each of size 1, and returns a list of size n, 
    containing non tuple elements."""
    def convert_from_plural_tuples(self, input):
        output_list = []
        for item in input:
            item = list(item)
            output_list.append(item[0])
        return output_list

    """The 'convert_from_large_tuples_in_large_lists' method takes a list of multiple tuples, 
    each containing multiple values, and retuns a nested list."""
    def convert_from_large_tuples_in_large_lists(self, input):
        output_nested_list = []
        for tuple in input:
            output_nested_list.append(list(tuple))
        return output_nested_list




class AccountSecurity():

    """The following method takes a password input and a salt input, combines inputs and hashes the combined string
    using the bcrypt.hashpw function."""
    def hash_password(self, password, salt):
        password = password.encode('utf-8')
        for number in range(10):
            password = bcrypt.hashpw(password=password, salt=salt)
        return password

    def generate_salt(self):
          return bcrypt.gensalt()



