"""This module holds the Inventory class for the SwordieDB package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a MIT-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""
import mysql.connector as con


class Inventory:
    """Inventory object; quasi-models SwordieMS inventories.

    The instance method SwordieDB::get_char_by_name(name) creates a Character object; as part of
    swordie_db Charatcer object instantiation, an Inventory object instance containing inventory attributes of
    the character with IGN "name" in the connected Swordie-based database is created.
    This class contains the appropriate getter methods for said attributes.
    As a consequence of the inherent complexity of MapleStory's item system, for safety reasons,
    this module offers NO inventory-write operations (aka setters).

    Attributes:
        inventory_ids: dictionary, representing inventory IDs
        equip_inv: dictionary of dictionaries, representing in-game items contained by the EQUIP tab
        consume_inv: dictionary of dictionaries, representing in-game items contained by the USE tab
        etc_inv: dictionary of dictionaries, representing in-game items contained by the ETC tab
        install_inv: dictionary of dictionaries, representing in-game items contained by the SETUP tab
        cash_inv: dictionary of dictionaries, representing in-game items contained by the CASH tab
        equipped_inv: dictionary of dictionaries, representing in-game items currently equipped by the character
    """

    def __init__(self, inv_ids, db_config):
        """Inventory object; quasi-models SwordieMS inventories.

        Due to the inherent complexity of SwordieMS's iventory system, this Inventory object will
        attempt to contain attributes of all 6 of SwordieMS's inventory types, using a custom object.
        (Refer to Character::init_inventory_ids() for a list of inventory_types)
        Every inventory attribute is a dictionary of dictionaries, where the Key is the bag index
        (i.e. inventory type), and the Value is a dictionary modeling contents of the `items` table
        in a Swordie-based database.
        As a consequence of the inherent complexity of MapleStory's item system, for safety reasons,
        this module offers NO inventory-write operations (only inventory-read operations).

        Args:
            inv_ids: dictionary, representing inventory IDs
            db_config: dictionary, containing database connection attributes
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

    @staticmethod
    def has_item_in_inv_type(inv_type, item_id):
        """Checks whether the particular tab of the inventory has an item

        Generic static method used by the other Inventory::has_item_in_XXX() methods, and the
        Character::is_equipping() method.
        Iterates through the dictionary of items associated with the specified tab, and check if
        the provided item ID can be found as a value.

        Returns:
            Boolean, representing whether the specified item was found
        """
        for bag_index in inv_type:
            if inv_type[bag_index]['itemid'] == item_id:
                return True
        return False

    def has_item_in_equip(self, item_id):
        """Checks whether the EQUIP tab of the inventory has an item

        Uses Inventory::has_item_in_inv_type()

        Returns:
            Boolean, representing whether the specified item was found
        """
        return self.has_item_in_inv_type(self.equip_inv, item_id)

    def has_item_in_consume(self, item_id):
        """Checks whether the USE tab of the inventory has an item

        Uses Inventory::has_item_in_inv_type()

        Returns:
            Boolean, representing whether the specified item was found
        """
        return self.has_item_in_inv_type(self.consume_inv, item_id)

    def has_item_in_etc(self, item_id):
        """Checks whether the ETC tab of the inventory has an item

        Uses Inventory::has_item_in_inv_type()

        Returns:
            Boolean, representing whether the specified item was found
        """
        return self.has_item_in_inv_type(self.etc_inv, item_id)

    def has_item_in_install(self, item_id):
        """Checks whether the SETUP tab of the inventory has an item

        Uses Inventory::has_item_in_inv_type()

        Returns:
            Boolean, representing whether the specified item was found
        """
        return self.has_item_in_inv_type(self.install_inv, item_id)

    def has_item_in_cash(self, item_id):
        """Checks whether the CASH tab of the inventory has an item

        Uses Inventory::has_item_in_inv_type()

        Returns:
            Boolean, representing whether the specified item was found
        """
        return self.has_item_in_inv_type(self.cash_inv, item_id)

    def is_equipping(self, item_id):
        """Checks whether the EQUIP window (i.e. Hotkey "E") has an item (i.e. item is equipped)

        Uses Inventory::has_item_in_inv_type()

        Returns:
            Boolean, representing whether the specified item was found
        """
        return self.has_item_in_inv_type(self.equipped_inv, item_id)

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
        """Given an inventory_type, fetch every item associated with it.

        Generic instance method used by Character::init_XXX_inv() methods.
        Refer to Character::init_inventory_ids() for a list of inventory_types.

        Args:
            inventory_type: string, representing the inventory type

        Returns:
            dictionary, representing all the in-game items that in the specified inventory type

        Raises:
            Generic error
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
            print("CRITICAL: Error occurred when initializing inventory items: \n", e)
