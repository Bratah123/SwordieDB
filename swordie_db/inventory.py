class Inventory:

    def __init__(self):
        """

        Possible solution 1:
            All "inv" attributes will be dictionaries
            Key: bag index
            Value: a dictionary with item_info

        Possible Solution 2:
            Make an Item Class that stores all of that info and store these Item objects into the dictionary

        EX:
        equip_inv = {
            # Bag index 1
            "1" :{
                    "itemid": 2000005
                    "invtype": 1 # It's "1" in this case because Equip inventory ID is 1
                    "quantity": 300
                    "iscash": False
                 }
        }
        """
        self._inventory_id = 0
        self._equip_inv = {}
        self._use_inv = {}
        self._etc_inv = {}
        self._cash_inc = {}

        self._equipped_inv = {}
