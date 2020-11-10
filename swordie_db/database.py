import mysql.connector


class SwordieDB:

    def __init__(self, host="localhost", schema="swordie", user="root", password=""):
        self._host = host
        self._schema = schema
        self._user = user
        self._password = password

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, x):
        self._host = x

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, x):
        self._schema = x

    @property
    def user(self):
        return self._schema

    @user.setter
    def user(self, x):
        self._user = x

    @property
    def password(self):
        return self._schema

    @password.setter
    def password(self, x):
        self._password = x