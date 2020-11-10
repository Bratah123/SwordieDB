import json
import mysql.connector as con
from os import path


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
        self.money = new_amount

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

    def get_job_name(self):
        """
        Returns the actual name of the job from job id
        :return: String
        """
        json_path = path.dirname(path.abspath(__file__)) + "/jobs.json"
        with open(json_path, 'r') as f:
            json_data = json.load(f)
            return json_data[str(self.job)]

    def set_stat_by_column(self, column, value):
        """
        Update a character's stats from column name in database
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
            database.disconnect()
            return True
        except Exception as e:
            print("[ERROR] Error trying to set stats in database.", e)
            return False
