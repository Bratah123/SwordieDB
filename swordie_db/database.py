"""SwordieDB is designed for use in development of SwordieMS-based MapleStory private server tools (e.g. Discord bots).

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a MIT-style license that can be found in the LICENSE file.
This module contains the main class that users would instantiate: SwordieDB.
Users can use this class to fetch and manipulate information from the database.
Refer to the project wiki on GitHub for more in-depth examples.

    Typical usage example:

    swordie = SwordieDB()  # Instantiate DB object
    char = swordie.get_char_by_name("brandon")  # Instantiate Character object
    meso = char.money  # Use of Character methods to fetch data from DB
    char.money = 123456789  # Use of Character methods to write data to DB
"""
import mysql.connector as con
from swordie_db.character import Character
from swordie_db.user import User


class SwordieDB:
    """Database object; models the SwordieMS DB.

    Use this class to create instances of SwordieMS characters, users, or inventories, complete with their respective
    data from the connected Swordie-based database.
    Using instance method SwordieDB::get_char_by_name("name") will create a Character object (see character.py) instance
    that has attributes identical to the character with IGN "name" in the connected Swordie-based database.

    Attributes:
        host: Optional; IP address of the database. Defaults to "localhost"
        schema: Optional; Name of the schema of the database (aka connection name). Defaults to "swordie"
        user: Optional; Username for access to the database. Defaults to "root"
        password: Optional; Password for access to the database. Defaults to ""
        port: Optional; Port with which to access the database. Defaults to 3306
    """
    def __init__(self, host="localhost", schema="swordie", user="root", password="", port=3306):
        self._host = host
        self._schema = schema
        self._user = user
        self._password = password
        self._port = port

        self._database_config = {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "schema": self.schema,
            "port": self.port
        }

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

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_port):
        self._port = new_port

    def get_char_by_name(self, char_name):
        """Create an instance of a Character object from the given character name

        Uses the class constructor of the Character class to create a new instance, with the corresponding
        character data and database attributes from the connected database.

        Args:
            char_name: string, representing character name (aka IGN)

        Returns:
            Character object instantiated with corresponding data from the connected database.
            Defaults to None if the operation fails.

        Raises:
            Generic error on failure - handled by the Character::get_db() method
        """
        character_stats = Character.get_db(
            self._database_config,
            f"SELECT * FROM characterstats WHERE name = '{char_name}'"
        )  # Fetch first result because there should only be one character with that name

        character = Character(character_stats, self._database_config)
        return character

    def get_user_by_username(self, username):
        """Given a username (NOT IGN), create a new user object instance

        Fetches the user attributes from the database by querying for username.
        uses the User class constructor to create a new User object instance, with the said attributes.
        Useful for getting account information from accounts with no characters.

        Args:
            username: String, representing the username used for logging the user into game

        Returns:
            User object with attributes identical to its corresponding entry in the database

        Raises:
            Generic error on failure - handled by the Character::get_db() method
        """
        user_stats = Character.get_db(
            self._database_config,
            f"SELECT * FROM users WHERE name = '{username}'"
        )  # Fetch first result because there should only be one character with that name

        user = User(user_stats, self._database_config)
        return user

    def set_char_stat(self, name, column, value):
        """Given a character name and column name, change its value in the database

        Args:
            column: string, representing the column in the database
            name: string, representing the character name in the database
            value: string/int, representing the value that is to be updated in the corresponding field

        Returns:
            boolean, representing whether the operation completed successfully

        Raises:
            SQL Error 2003: Can't cannect to DB
            WinError 10060: No response from DB
            List index out of range: Wrong column or character name
        """
        try:
            database = con.connect(host=self.host, user=self.user, password=self.password, database=self.schema, port=self.port)
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
        """Given a character name, retrieve its corresponding user id from database

        Uses static method Character::get_user_id_by_name() for core logic

        Args:
            char_name: string, representing the character name in the database

        Returns:
            String, representing the user ID in the database
            Defaults to None if the operation fails.

        Raises:
            Errors are handled and thrown by Character::get_user_id_by_name()
            SQL Error 2003: Can't cannect to DB
            WinError 10060: No response from DB
            List index out of range: Wrong character name
        """
        return Character.get_user_id_by_name(self._database_config, char_name)
