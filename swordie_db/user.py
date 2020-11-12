"""This module holds the User class for the SwordieDB package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a MIT-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""
import mysql.connector as con


class User:
    """User object; models SwordieMS users.

    Using instance method SwordieDB::get_user_by_username(username) or the SwordieDB::get_char_by_name(name).user getter
    will create a User object instance with attributes identical to the user with username "username"
    (or IGN "name" for the latter) in the connected Swordie-based database.
    This class contains the appropriate getter and setter methods for said attributes.

    Attributes:
        account_type: Integer, representing the level of authority
        ban_reason: String (256 Char), representing the reason the user is banned
        donation_points: Integer, representing the amount of DP the user has
        maple_points: Integer, representing the amount of Maple Points the user has
        nx_prepaid: Integer, representing the amoung of NX Prepaid the user has
        user_id: Integer, representing the User ID
        vote_points: Integer, representing the amount of VP the user has
    """

    def __init__(self, user_stats, database_config):
        """Emulates how user object is handled server-sided

        Args:
            user_stats: dictionary of user attributes, formatted in SwordieMS style
            database_config: dictionary of protected attributes from a SwordieDB object
        """

        self._user_stats = user_stats
        self._database_config = database_config

        self._id = 0
        self._ban_reason = ""
        self._vote_points = 0
        self._donation_points = 0
        self._maple_points = 0
        self._nx_prepaid = 0
        self._account_type = 0
        self.init_user_stats()

    def init_user_stats(self):
        """Given a dictionary of stats from Swordie's DB we add them to User object's attributes

        Runs near the end of User::__init__(user_stats, database_config).
        It assigns the user attributes in user_stats to their respective protected attributes belonging to
        the User object instance.
        """
        self._id = self._user_stats["id"]
        self._ban_reason = self._user_stats["banReason"]
        self._vote_points = self._user_stats["votepoints"]
        self._donation_points = self._user_stats["donationpoints"]
        self._maple_points = self._user_stats["maplePoints"]
        self._nx_prepaid = self._user_stats["nxPrepaid"]
        self._account_type = self._user_stats["accounttype"]

    @property
    def user_stats(self):
        return self._user_stats

    @property
    def database_config(self):
        return self._database_config

    @property
    def user_id(self):
        return self._id

    @property
    def ban_reason(self):
        return self._ban_reason

    @ban_reason.setter
    def ban_reason(self, reason):
        if len(reason) < 255:
            self.set_stat_by_column("banReason", reason)
            self._ban_reason = reason
        else:
            print("Ban Reason was too long.")

    @property
    def vote_points(self):
        return self._vote_points

    @vote_points.setter
    def vote_points(self, amount):
        self.set_stat_by_column("votepoints", amount)
        self._vote_points = amount

    def add_vote_points(self, amount):
        """Adds the specified amount to the current VP count

        Args:
            amount: Int, representing the number of vote points to be added to the current count
        """
        new_vp = int(amount) + self.vote_points
        self.vote_points = new_vp

    @property
    def donation_points(self):
        return self._donation_points

    @donation_points.setter
    def donation_points(self, amount):
        self.set_stat_by_column("donationpoints", amount)
        self._donation_points = amount

    def add_donation_points(self, amount):
        """Adds the specified amount to the current DP count

        Args:
            amount: Int, representing the number of DPs to be added to the current count
        """
        new_dp = int(amount) + self.donation_points
        self.donation_points = new_dp

    @property
    def maple_points(self):
        return self._maple_points

    @maple_points.setter
    def maple_points(self, amount):
        self.set_stat_by_column("maplePoints", amount)
        self._maple_points = amount

    def add_maple_points(self, amount):
        """Adds the specified amount to the current Maple Points pool

        Args:
            amount: Int, representing the number of Maple Points to be added to the current pool
        """
        new_maple_points = int(amount) + self.maple_points
        self.maple_points = new_maple_points

    @property
    def account_type(self):
        return self._account_type

    @account_type.setter
    def account_type(self, acc_type):
        self.set_stat_by_column("accounttype", acc_type)
        self._account_type = acc_type

    def give_admin(self):
        """Sets the user account type to: Admin"""
        self.account_type = 4

    def give_intern(self):
        """Sets the user account type to: Intern"""
        self.account_type = 3

    def give_tester(self):
        """Sets the user account type to: Tester"""
        self.account_type = 5

    def give_player(self):
        """Sets the user account type to: Player"""
        self.account_type = 0

    def is_admin(self):
        """Checks if the user's account type is: Admin (Strictly)

        Checks if the account type ID associated with the user is 4. Both Int and String types are checked.

        Returns:
            Boolean, representing whether user is Admin (True) or not (False)
        """
        return self.account_type == 4 or self.account_type == "4"  # A string check just in case

    def change_password(self, new_pass):
        """WARNING: UNSAFE!

        Primitive password change function. It will break in real Swordie-based sources, as Swordie hashes passwords.
        Note: This is not a safe method to use when changing password as it does not hash the password after changing.

        Args:
            new_pass: string, representing the new plaintext password to be set to the database
        """
        self.set_stat_by_column("password", new_pass)

    def get_acc_type_string(self):
        """Fetches the account type of the user in words

        Fetches the account type (Int) from user attributes. Maps the account type to its meaning in words

        Returns:
            String, representing account type
        """
        if self.account_type == 4:
            return "Admin"
        elif self.account_type == 0:
            return "Player"
        elif self.account_type == 3:
            return "Intern"
        elif self.account_type == 5:
            return "Tester"

    @property
    def nx_prepaid(self):
        return self._nx_prepaid

    @nx_prepaid.setter
    def nx_prepaid(self, amount):
        self.set_stat_by_column("nxPrepaid", amount)
        self._nx_prepaid = amount

    def add_nx_prepaid(self, amount):
        new_nx = int(amount) + self.nx_prepaid
        self.nx_prepaid = new_nx

    def get_stat_by_column(self, column):
        """Fetches user attribute by column name

        Returns:
            Int or String, representing user attribute queried
        Raises:
            Generic error on failure
        """
        try:
            return self.user_stats[str(column)]
        except Exception as e:
            print("[ERROR] Error trying to obtain the given column for table users.", e)

    def set_stat_by_column(self, column, value):
        """Sets a user's attributes by column name in database

        Grabs the database attributes provided through the class constructor.
        Uses these attributes to attempt a database connection.
        Attempts to update the field represented by the provided column in the users table, with the provided value.
        Not recommended to use this alone, as it won't update the user object which this was used from

        Args:
            value: int or string, representing the value to be set in the database
            column: string, representing the column in the database that is to be updated

        Returns:
            A boolean representing whether the operation was successful.

        Raises:
            SQL Error 2003: Can't cannect to DB
            WinError 10060: No response from DB
            List index out of range: Wrong column name
        """
        host = self._database_config["host"]
        user = self._database_config["user"]
        password = self._database_config["password"]
        schema = self._database_config["schema"]
        port = self._database_config["port"]

        try:
            database = con.connect(host=host, user=user, password=password, database=schema, port=port)

            cursor = database.cursor(dictionary=True)
            cursor.execute(f"UPDATE users SET {column} = '{value}' WHERE id = '{self.user_id}'")
            database.commit()
            print(f"Successfully updated {column} value for user id: {self.user_id}.")
            self._user_stats[column] = value  # Update the stats in the dictionary
            database.disconnect()
            return True
        except Exception as e:
            print("[ERROR] Error trying to set stats in database.", e)
            return False
