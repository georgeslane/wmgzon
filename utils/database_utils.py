import bcrypt

class SqliteReader():

    """The method below converts any single value input into a tuple of size 1"""
    def convert_to_tuple(self, input):
        return (input,)

    """The method below converts any tuple of size n stored inside a list of size 1 into a list of size n, with each 
    element of the list coresponding to an element of the tuple."""
    def convert_from_tuple(self, input):
        input = list(input[0])
        return input

    """The following method takes a list of size n, containing tuples, each of size 1, and returns a list of size n, 
    containing non tuple elements."""
    def convert_from_plural_tuples(self, input):
        output_list = []
        for item in input:
            item = list(item)
            output_list.append(item[0])
        return output_list



class AccountSecurity():

    """The following method takes a password input and a salt input, combines inputs and hashes the combined string
    using the bcrypt.hashpw function."""
    def hash_password(self, password, salt):
        return bcrypt.hashpw(password, salt)

