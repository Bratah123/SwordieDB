import mysql.connector as con
from swordie_db import JOBS


class Character:

    def __init__(self, char_stats, database_config):
        """
        Emulates how character object is handled server-sided
        :param char_stats: dict
        :param database_config: dict
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

    def init_stats(self):
        """
        Given a dictionary of stats from Swordie's DB we add them to character's attributes
        :return: void
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

    @property
    def stats(self):
        return self._stats

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, x):
        self.set_stat_by_column("level", x)
        self._level = x

    def add_level(self, amount):
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
        """
        Returns the actual name of the job from job id
        :return: String
        """
        return JOBS[str(self.job)]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        """
        Set a new name for the character
        :param new_name: string
        :return: void
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
        """
        Adds to the current meso count
        :param amount: int
        :return: void
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
        """
        Adds to the current fame amount
        :param amount: int
        :return:
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
        """
        Add to the current existing exp pool
        :param amount: int
        :return: void
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
        new_luk = int(self.luk) + amount
        self.luk = new_luk

    def get_primary_stats(self):
        """
        Returns str, int, dex, luk in a dictionary
        :return: dict
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
        new_sp = int(self.sp) + amount
        self.sp = new_sp

    def set_stat_by_column(self, column, value):
        """
        Update a character's stats from column name in database
        :param value: int or string
        :param column: string
        :return: boolean
        """

        host = self._database_config["host"]
        user = self._database_config["user"]
        password = self._database_config["password"]
        schema = self._database_config["schema"]
        try:
            database = con.connect(host=host, user=user, password=password, database=schema)

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
        """
        Given a column name, return it's value in the database
        :param column: string
        :return: string
        """
        try:
            return self.stats[column]
        except Exception as e:
            print("[ERROR] Error trying to get stats from given column.", e)
            return False
