import mysql.connector as con

from swordie_db.character import Character


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
        return self._user

    @user.setter
    def user(self, x):
        self._user = x

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, x):
        self._password = x

    def get_char_by_name(self, char_name):
        """

        :param char_name: string
        :return: Character
        """
        try:
            database = con.connect(host=self.host, user=self.user, password=self.password, database=self.schema)
            cursor = database.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM characterstats WHERE name = '{char_name}'")
            character_stats = cursor.fetchall()[0]  # It is 0 because there should only be one character with that name
            database.disconnect()
            database_config = {
                "host": self.host,
                "user": self.user,
                "password": self.password,
                "schema": self.schema
            }
            character = Character(character_stats, database_config)
            return character
        except Exception as e:
            print("[ERROR] Error trying to retrieve character from database.", e)
            return None

    def set_char_stat(self, name, column, value):
        """
        Given a character name and column name, change it's value in the database
        :param column: string
        :param name: string
        :param value: string/int
        :return: boolean
        """
        try:
            database = con.connect(host=self.host, user=self.user, password=self.password, database=self.schema)
            cursor = database.cursor(dictionary=True)
            cursor.execute(f"UPDATE characterstats SET {column} = '{value}' WHERE name = '{name}'")
            database.commit()
            database.disconnect()
            print(f"Successfully set {name}'s stats in database.")
            return True
        except Exception as e:
            print("[ERROR] Error trying to update character stats in Database.", e)
            return False

    def get_user_id_by_name(self, char_name):
        """
        Given a character name, retrieve it's corresponding user id from database
        :param char_name: string
        :return: string / None
        """
        try:
            database = con.connect(host=self.host, user=self.user, password=self.password, database=self.schema)
            cursor = database.cursor(dictionary=True)

            cursor.execute(f"SELECT characterid FROM characterstats WHERE name = '{char_name}'")
            char_id = cursor.fetchall()[0]["characterid"]

            cursor.execute(f"SELECT accid FROM characters WHERE id = '{char_id}'")
            account_id = cursor.fetchall()[0]["accid"]

            cursor.execute(f"SELECT userid FROM accounts WHERE id = '{account_id}'")
            user_id = cursor.fetchall()[0]["userid"]

            database.disconnect()
            return user_id

        except Exception as e:
            print("[ERROR] Error trying to get user id from database.", e)
            return None  # Return None if there was an error
