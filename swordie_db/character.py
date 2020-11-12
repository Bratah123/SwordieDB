"""This module holds the Character class for the SwordieDB package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a MIT-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""
import mysql.connector as con

from swordie_db import JOBS
from swordie_db.user import User


class Character:
    """Character object; models SwordieMS characters.

    Using instance method SwordieDB::get_char_by_name(name) will create a Character object instance with
    attributes identical to the character with IGN "name" in the connected Swordie-based database.
    This class contains the appropriate getter and setter methods for said attributes.

    Attributes:
        user: User, A User object
        stats: Dictionary of all character stats obtained from the characterstats table
        level: Integer, representing character level
        job: Integer, representing character job ID
        name: String, representing character name (aka IGN)
        money: String, representing character wealth (aka Meso count)
        fame: Integer, representing character popularity
        map: String, representing the Map ID of the map that the character is currently in
        face: Integer, representing the Face ID of the character
        hair: Integer, representing the Hair ID of the character
        skin: Integer, representing the Skin ID of the character
        exp: String, representing character EXP pool (amount)
        strength: Integer, representing character STR stat pool
        dex: Integer, representing character DEX stat pool
        inte: Integer, representing character INT stat pool
        luk: Integer, representing character LUK stat pool
        max_hp: Integer, representing character Max HP stat pool
        max_mp: Integer, representing character Max MP stat pool
        ap: Integer, representing character free Ability Points (AP) pool
        sp: Integer, representing character free SP points pool
        equip_inv_id: Integer, representing the "equip" inventory id
        equipped_inv_id: Integer, representing the "equipped" (i.e. Hotkey "E" in-game) inventory id
        consume_inv_id: Integer, representing "consume" (aka USE) inventory id
        etc_inv_id: Integer, representing "etc" (aka ETC) inventory id
        install_inv_id: Integer, representing "install" (aka SETUP) inventory id
        cash_inv_id: Integer, representing "cash" (aka CASH) inventory id
    """

    def __init__(self, char_stats, database_config):
        """Emulates how character object is handled server-sided

        Args:
            char_stats: dictionary of character stats, formatted in SwordieMS style
            database_config: dictionary of protected attributes from a SwordieDB object
        """
        self._stats = char_stats
        self._database_config = database_config

        self._vague_id = 0
        self._character_id = 0
        self._character_id_for_log = 0
        self._world_id = 0
        self._name = ""
        self._gender = 0
        self._skin = 0
        self._face = 0
        self._hair = 0
        self._mix_base_hair_color = 0
        self._mix_add_hair_color = 0
        self._mix_hair_base_prob = 0
        self._level = 0
        self._job = 0
        self._strength = 0
        self._dex = 0
        self._inte = 0
        self._luk = 0
        self._hp = 0
        self._max_hp = 0
        self._mp = 0
        self._max_mp = 0
        self._ap = 0
        self._sp = 0
        self._exp = 0
        self._pop = 0  # fame
        self._money = 0
        self._wp = 0
        self._position_map = 0
        self._portal = 0
        self._sub_job = 0
        self.init_stats()

        # These attributes are separate from characterstats table in database
        self._equip_inv_id = 0
        self._equipped_inv_id = 0
        self._consume_inv_id = 0
        self._etc_inv_id = 0
        self._install_inv_id = 0
        self._cash_inv_id = 0
        # Create Inventory object instance via class constructor, using details from Character object instance
        # (Stipulated algorithm for unfinished sequence)
        self.init_inv_id()

        # Create User object instance via class constructor, using details from Character object instance
        self._user = self.init_user()

    def init_stats(self):
        """Given a dictionary of stats from Swordie's DB we add them to Character object's attributes

        Runs near the end of Character::__init__(char_stats, database_config).
        It assigns the character attributes in char_stats to their respective protected attributes belonging to
        the Character object instance.
        """
        self._vague_id = self._stats["id"]
        self._character_id = self._stats["characterid"]
        self._character_id_for_log = self._stats["characteridforlog"]
        self._world_id = self._stats["worldidforlog"]
        self._name = self._stats["name"]
        self._gender = self._stats["gender"]
        self._skin = self._stats["skin"]
        self._face = self._stats["face"]
        self._hair = self._stats["hair"]
        self._mix_base_hair_color = self._stats["mixbasehaircolor"]
        self._mix_add_hair_color = self._stats["mixaddhaircolor"]
        self._mix_hair_base_prob = self._stats["mixhairbaseprob"]
        self._level = self._stats["level"]
        self._job = self._stats["job"]
        self._strength = self._stats["str"]
        self._dex = self._stats["dex"]
        self._inte = self._stats["inte"]
        self._luk = self._stats["luk"]
        self._hp = self._stats["hp"]
        self._max_hp = self._stats["maxhp"]
        self._mp = self._stats["mp"]
        self._max_mp = self._stats["maxmp"]
        self._ap = self._stats["ap"]
        self._sp = self._stats["sp"]
        self._exp = self._stats["exp"]
        self._pop = self._stats["pop"]  # fame
        self._money = self._stats["money"]
        self._wp = self._stats["wp"]
        self._position_map = self._stats["posmap"]
        self._portal = self._stats["portal"]
        self._sub_job = self._stats["subjob"]

    def init_user(self):
        """Fetch a dictionary of user attributes from Swordie's DB and use it to instantiate a new User object

        Runs at the end of Character::__init__(char_stats, database_config).
        Checks the User ID associated with the character instance, and uses the User class constructor to create
        a new User object instance, with the relevant user attributes from the database.

        Returns:
            User
        Raises:
            Generic error on failure - handled by the Character::get_db() method
        """
        user_id = self.get_user_id()
        
        user_stats = self.get_db(
            self._database_config,
            f"SELECT * FROM users WHERE id = '{user_id}'"
        )  # The row will always be 0 because there should be no characters with the same name

        user = User(user_stats, self.database_config)
        return user

    def init_inv_id(self):
        """Fetch a dictionary of user attributes from Swordie's DB and use it to instantiate a new (custom) Inventory object

        (Stipulated algorithm for unfinished sequence)
        Runs near the end of Character::__init__(char_stats, database_config).
        Uses the Character ID associated with the character instance, and the Inventory class constructor to create
        a new Inventory object instance, with the relevant character attributes from the database.

        Raises:
            Generic error on failure - handled by the Character::get_db() method
        """
        inventory_ids = self.get_db(
            self._database_config,
            f"SELECT equippedinventory, consumeinventory, etcinventory, installinventory, cashinventory "
            f"FROM characters WHERE id = '{self.character_id}'"
        )  # The row will always be 0 because there should be no characters with the same ID

        self._equip_inv_id = inventory_ids["equipinventory"]
        self._equipped_inv_id = inventory_ids["equippedinventory"]
        self._consume_inv_id = inventory_ids["consumeinventory"]
        self._etc_inv_id = inventory_ids["etcinventory"]
        self._install_inv_id = inventory_ids["installinventory"]
        self._cash_inv_id = inventory_ids["cashinventory"]

    # Static method for fetching DB
    @staticmethod
    def get_db(config, query):
        """Generic static method for fetching data from DB using the provided DB config and query
        
        This method assumes that only one character is found - it always defaults to the first result.
        An effort has been made to convert this to a decorator so that it may also be applied to
        Character::set_stat_by_column() & Character::get_user_id(), which ultimately ended in failure.
        
        Args:
            config, dictionary, representing database config attributes
            query, String, representing SQL query
        Returns:
            String representing the result of the provided SQL query, using the provided DB connection attributes
        """
        try:
            database = con.connect(
                host=config["host"], 
                user=config["user"], 
                password=config["password"], 
                database=config["schema"], 
                port=config["port"]
            )
            cursor = database.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()[0]
            database.disconnect()

            return data
            
        except Exception as e:
            print("CRITICAL: Error encountered whilst attempting to connect to the database! \n", e)

    @property
    def database_config(self):
        return self._database_config

    @property
    def stats(self):
        return self._stats

    @property
    def character_id(self):
        return self._character_id

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, x):
        self.set_stat_by_column("level", x)
        self._level = x

    def add_level(self, amount):
        """Adds the specified amount to the current level count

        Args:
            amount: Int, representing the number of levels to be added to the current count
        """
        new_level = int(self.level) + amount
        self.level = new_level

    @property
    def job(self):
        return self._job

    @job.setter
    def job(self, job_id):
        self.set_stat_by_column("job", job_id)
        self._job = job_id

    def get_job_name(self):
        """Returns the actual name of the job from job id

        Returns:
            String, representing the job name corresponding to a job ID
        """
        return JOBS[str(self.job)]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        """Set a new name for the character

        Args:
            new_name: string, representing the new character name that will be set in the database
        """
        self.set_stat_by_column("name", new_name)
        self._name = new_name

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, amount):
        self.set_stat_by_column("money", amount)
        self._money = amount

    def add_mesos(self, amount):
        """Adds the specified amount to the current meso count

        Args:
            amount: Int, representing the amount of mesos to be added to the current count
        """
        new_amount = int(self.money) + amount
        self.money = str(new_amount)  # money is a String; converting back to String for consistency

    @property
    def fame(self):
        return self._pop

    @fame.setter
    def fame(self, amount):
        self.set_stat_by_column("pop", amount)
        self._pop = amount

    def add_fame(self, amount):
        """Adds the specified amount to the current fame count

        Args:
            amount: Int, representing the number of fames to be added to the current count
        """
        new_fame = int(self.fame) + amount
        self.fame = new_fame

    @property
    def map(self):
        return self._position_map

    @map.setter
    def map(self, map_id):
        self.set_stat_by_column("posmap", map_id)
        self._position_map = map_id

    @property
    def face(self):
        return self._face

    @face.setter
    def face(self, face_id):
        self.set_stat_by_column("face", face_id)
        self._face = face_id

    @property
    def hair(self):
        return self._hair

    @hair.setter
    def hair(self, hair_id):
        self.set_stat_by_column("hair", hair_id)
        self._hair = hair_id

    @property
    def skin(self):
        return self._skin

    @skin.setter
    def skin(self, skin_id):
        self.set_stat_by_column("skin", skin_id)
        self._skin = skin_id

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, exp_amount):
        self.set_stat_by_column("exp", exp_amount)
        self._exp = exp_amount

    def add_exp(self, amount):
        """Add the specified amount to the current existing EXP pool

        Args:
            amount: Int, representing the amount of EXP to be added to the current pool
        """
        new_exp = int(self.exp) + amount
        self.exp = str(new_exp)  # EXP is a String; converting back to String for consistency

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, amount):
        self.set_stat_by_column("str", amount)
        self._strength = amount

    def add_str(self, amount):
        """Add the specified amount to the current existing STR pool

        Args:
            amount: Int, representing the amount of STR to be added to the current pool
        """
        new_str = int(self.strength) + amount
        self.strength = new_str

    @property
    def dex(self):
        return self._dex

    @dex.setter
    def dex(self, amount):
        self.set_stat_by_column("dex", amount)
        self._dex = amount

    def add_dex(self, amount):
        """Add the specified amount to the current existing DEX pool

        Args:
            amount: Int, representing the amount of DEX to be added to the current pool
        """
        new_dex = int(self.dex) + amount
        self.dex = new_dex

    @property
    def inte(self):
        return self._inte

    @inte.setter
    def inte(self, amount):
        self.set_stat_by_column("inte", amount)
        self._inte = amount

    def add_inte(self, amount):
        """Add the specified amount to the current existing INT pool

        Args:
            amount: Int, representing the amount of INT to be added to the current pool
        """
        new_inte = int(self.inte) + amount
        self.inte = new_inte

    @property
    def luk(self):
        return self._luk

    @luk.setter
    def luk(self, amount):
        self.set_stat_by_column("luk", amount)
        self._luk = amount

    def add_luk(self, amount):
        """Add the specified amount to the current existing LUK pool

        Args:
            amount: Int, representing the amount of LUK to be added to the current pool
        """
        new_luk = int(self.luk) + amount
        self.luk = new_luk

    def get_primary_stats(self):
        """Returns str, int, dex, luk values in a dictionary

        Returns:
            dictionary of primary stats
        """
        primary_stats = {
            "str": self.strength,
            "dex": self.dex,
            "int": self.inte,
            "luk": self.luk
        }
        return primary_stats

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, amount):
        self.set_stat_by_column("maxhp", amount)
        self._max_hp = amount

    def add_max_hp(self, amount):
        """Add the specified amount to the current existing Max HP pool

        Args:
            amount: Int, representing the amount of Max HP to be added to the current pool
        """
        new_hp = int(self.max_hp) + amount
        self.max_hp = new_hp

    @property
    def max_mp(self):
        return self._max_mp

    @max_mp.setter
    def max_mp(self, amount):
        self.set_stat_by_column("maxmp", amount)
        self._max_mp = amount

    def add_max_mp(self, amount):
        """Add the specified amount to the current existing Max MP pool

        Args:
            amount: Int, representing the amount of max MP to be added to the current pool
        """
        new_mp = int(self.max_mp) + amount
        self.max_mp = new_mp

    @property
    def ap(self):
        return self._ap

    @ap.setter
    def ap(self, amount):
        self.set_stat_by_column("ap", amount)
        self._ap = amount

    def add_ap(self, amount):
        """Add the specified amount to the current existing free AP pool

        Args:
            amount: Int, representing the amount of free AP to be added to the current pool
        """
        new_ap = int(self.ap) + amount
        self.ap = new_ap

    @property
    def sp(self):
        return self._sp

    @sp.setter
    def sp(self, amount):
        self.set_stat_by_column("sp", amount)
        self._sp = amount

    def add_sp(self, amount):
        """Add the specified amount to the current existing free SP pool

        Args:
            amount: Int, representing the amount of free SP to be added to the current pool
        """
        new_sp = int(self.sp) + amount
        self.sp = new_sp

    @property
    def user(self):
        return self._user

    @property
    def equipped_inv_id(self):
        return self._equipped_inv_id

    @property
    def consume_inv_id(self):
        return self._consume_inv_id

    @property
    def etc_inv_id(self):
        return self._etc_inv_id

    @property
    def install_inv_id(self):
        return self._install_inv_id

    @property
    def cash_inv_id(self):
        return self._cash_inv_id

    @property
    def equip_inv_id(self):
        return self._equip_inv_id

    def get_user_id(self):
        """Queries the database to obtain the User ID associated with this character instance

        Created this method to avoid circular imports by using SwordieDB's get_user_id

        Returns:
            Int, representing the User ID
            Returns None if User ID is not found
        Raises:
            Generic error on failure
        """
        host = self._database_config["host"]
        user = self._database_config["user"]
        password = self._database_config["password"]
        schema = self._database_config["schema"]
        port = self._database_config["port"]
        try:
            database = con.connect(host=host, user=user, password=password, database=schema, port=port)
            cursor = database.cursor(dictionary=True)

            cursor.execute(f"SELECT characterid FROM characterstats WHERE name = '{self.name}'")
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

    def set_stat_by_column(self, column, value):
        """Update a character's stats from column name in database

        Grabs the database attributes provided through the class constructor.
        Uses these attributes to attempt a database connection.
        Attempts to update the field represented by the provided column in characterstats, with the provided value.
        Not recommended to use this alone, as it won't update the character object which this was used from.

        Args:
            value: int or string, representing the value to be set in the database
            column: string, representing the column in the database that is to be updated

        Returns:
            A boolean representing whether the operation was successful

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
            cursor.execute(f"UPDATE characterstats SET {column} = '{value}' WHERE name = '{self.name}'")
            database.commit()
            print(f"Successfully updated {column} value for character: {self.name}.")
            self._stats[column] = value  # Update the stats in the dictionary
            database.disconnect()
            return True
        except Exception as e:
            print("[ERROR] Error trying to set stats in database.", e)
            return False

    def get_stat_by_column(self, column):
        """Given a column name, return its value in the database

        Args:
            column: string, representing the column in the database from which the value is to be fetched from

        Returns:
            string, representing the value in the database associated with the provided column

        Raises:
            Generic error on failure
        """
        try:
            return self.stats[column]
        except Exception as e:
            print("[ERROR] Error trying to get stats from given column.", e)
            return False
