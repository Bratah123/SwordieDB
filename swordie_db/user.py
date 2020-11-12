"""This module holds the User class for the SwordieDB package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a MIT-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""

import mysql.connector as con


class User:
    """
    This Class is for keep track of all the "User" attributes from Swordie's Database
    """

    def __init__(self, user_stats, database_config):
        """

        :param user_stats: dictionary
        :param database_config: dictionary
        """

        self._user_stats = user_stats
        self._database_config = database_config

        self._id = 0
        self._ban_reason = ""
        self._vote_points = 0
        self._donation_points = 0
        self._maple_points = 0
        self._account_type = 0
        self.init_user_stats()

    def init_user_stats(self):
        self._id = self._user_stats["id"]
        self._ban_reason = self._user_stats["banReason"]
        self._vote_points = self._user_stats["votepoints"]
        self._donation_points = self._user_stats["donationpoints"]
        self._maple_points = self._user_stats["maplePoints"]
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
        new_vp = int(amount) + self.vote_points
        self.vote_points = new_vp

    @property
    def donation_points(self):
        return self._donation_points

    @donation_points.setter
    def donation_points(self, amount):
        self.set_stat_by_column("donationpoints", amount)
        self.donation_points = amount

    def add_donation_points(self, amount):
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
        self.account_type = 4

    def give_intern(self):
        self.account_type = 3

    def give_tester(self):
        self.account_type = 5

    def give_player(self):
        self.account_type = 0

    def is_admin(self):
        return self.account_type == 4 or self.account_type == "4"  # A string check just in case

    def change_password(self, new_pass):
        """
        Note: This is not a safe method to use when changing password as it does not hash the password after changing
        :param new_pass: string
        :return: void
        """
        self.set_stat_by_column("password", new_pass)

    def get_acc_type_string(self):
        if self.account_type == 4:
            return "Admin"
        elif self.account_type == 0:
            return "Player"
        elif self.account_type == 3:
            return "Intern"
        elif self.account_type == 5:
            return "Tester"

    def get_stat_by_column(self, column):
        try:
            return self.user_stats[str(column)]
        except Exception as e:
            print("[ERROR] Error trying to obtain the given column for table users.", e)

    def set_stat_by_column(self, column, value):
        """
        Given a column name from the user table in database, change it's value to the given value
        :param column: string
        :param value: string/int
        :return: boolean
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
