import mysql.connector as con


class Inventory:

    def __init__(self, inv_ids, db_config):
        """

        :param inv_ids: dictionary
        :param db_config: dictionary

        Every inventory attribute is a dictionary where the key is the bag index of the item
        The Value is a dictionary pertaining attributes from items table in Swordie DB
        No write operations will be made by this class due to the complexity of Maplestory's Item and Equip's system
        To keep this a safer library, Inventory will not have ANY write operations but only reads instead.
        """
        self._inventory_ids = inv_ids
        self._database_config = db_config

        self._equip_inv = self.init_equip_items()
        self._use_inv = self.init_use_inv()
        self._etc_inv = self.init_etc_inv()
        self._cash_inv = self.init_cash_inv()
        self._install_inv = self.init_install_inv()

        self._equipped_inv = self.init_equipped_inv()

    @property
    def database_config(self):
        return self._database_config

    @property
    def inventory_ids(self):
        return self._inventory_ids

    @property
    def equip_inv(self):
        return self._equip_inv

    @property
    def consume_inv(self):
        return self._use_inv

    @property
    def etc_inv(self):
        return self._etc_inv

    @property
    def cash_inv(self):
        return self._cash_inv

    @property
    def install_inv(self):
        return self._install_inv

    @property
    def equipped_inv(self):
        return self._equipped_inv

    def has_item_in_equip(self, item_id):
        for bag_index in self.equip_inv:
            if int(self.equip_inv[bag_index]['itemid']) == item_id:
                return True
        return False

    def has_item_in_consume(self, item_id):
        for bag_index in self.consume_inv:
            if int(self.consume_inv[bag_index]['itemid']) == item_id:
                return True
        return False

    def has_item_in_etc(self, item_id):
        for bag_index in self.etc_inv:
            if int(self.etc_inv[bag_index]['itemid']) == item_id:
                return True
        return False

    def has_item_in_install(self, item_id):
        for bag_index in self.install_inv:
            if int(self.install_inv[bag_index]['itemid']) == item_id:
                return True
        return False

    def has_item_in_cash(self, item_id):
        for bag_index in self.cash_inv:
            if int(self.cash_inv[bag_index]['itemid']) == item_id:
                return True
        return False

    def is_equipping(self, item_id):
        for bag_index in self.equipped_inv:
            if int(self.equipped_inv[bag_index]['itemid']) == item_id:
                return True
        return False

    def init_equip_items(self):
        return self.load_inv("equip_inv_id")

    def init_use_inv(self):
        return self.load_inv("consume_inv_id")

    def init_etc_inv(self):
        return self.load_inv("etc_inv_id")

    def init_cash_inv(self):
        return self.load_inv("cash_inv_id")

    def init_equipped_inv(self):
        return self.load_inv("equipped_inv_id")

    def init_install_inv(self):
        return self.load_inv("install_inv_id")

    def load_inv(self, inventory_type):
        """
        Given an inventory_type, load every item in it.
        Refer to Character::init_inventory_ids() for a list of inventory_types.
        :param inventory_type: string
        :return: dictionary
        """
        try:
            database = con.connect(
                host=self.database_config["host"],
                user=self.database_config["user"],
                password=self.database_config["password"],
                database=self.database_config["schema"],
                port=self.database_config["port"]
            )
            cursor = database.cursor(dictionary=True)

            cursor.execute(f"SELECT * FROM items WHERE inventoryid = '{self.inventory_ids[str(inventory_type)]}'")
            rows = cursor.fetchall()

            inv = {}

            for items in rows:
                bag_index = items["bagindex"]
                item_id = items["itemid"]
                quantity = items["quantity"]
                inv_type = items["invtype"]
                is_cash = items["iscash"]
                item_stats = {
                    "itemid": item_id,
                    "quantity": quantity,
                    "invtype": inv_type,
                    "iscash": is_cash
                }
                inv[bag_index] = item_stats
            return inv
        except Exception as e:
            print("Critical: Error occured when initializing equip items", e)
