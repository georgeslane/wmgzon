import bcrypt

class SqliteReader():

    def convert_to_tuple(self, input):
        return (input,)


class AccountSecurity():

    def hash_password(self, password, salt):
        return bcrypt.hashpw(password, salt)
