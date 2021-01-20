from swordie_db.database import SwordieDB
import time

swordie_data = SwordieDB(schema="spirit")  # If no parameters are given, it will attempt to connect to localhost

char = swordie_data.get_char_by_name("brandon")

assert char is not None, "Character does not exist"

print("Character Name:", char.name)
print("Character Level:", char.level)
print("Job:", char.get_job_name())
print("Mesos:", char.money)
print("Fame:", char.fame)
print("Character image", char.get_char_img())

primary_stats = char.get_primary_stats()

for stat in primary_stats:
    print(f"{stat}: {primary_stats[stat]}")
    # Str
    # Dex
    # Int
    # Luk

# User Class

user = char.user
user.is_admin()

# Inventory

print("Consume Inventory:", char.inventory.consume_inv)

equip_inv = char.inventory.consume_inv
print("Testing equip checks....")


def test_check_speed():
    for bag_index in equip_inv:
        if 2000000 in equip_inv[bag_index].values():
            return True
    return False


def test_check_speed_equals():
    for bag_index in equip_inv:
        if 2000000 == equip_inv[bag_index]['itemid']:
            return True
    return False


print("Starting list comprehension test")

start_time = time.time()

for i in range(100000):
    test_check_speed()

end_time = time.time()

print(f"Completed List Comprehension 100000 iterations in: {end_time - start_time} seconds")

print("Starting == test")

start_time1 = time.time()

for n in range(100000):
    test_check_speed_equals()

end_time1 = time.time()

print(f"Completed 100000 iterations of == operations in: {end_time1 - start_time1} seconds")
