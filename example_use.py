from swordie_db.database import SwordieDB

swordie_data = SwordieDB()  # If no parameters are given, it will attempt to connect to localhost

char = swordie_data.get_char_by_name("brandon")

assert char is not None, "Character does not exist"

print("Character Name:", char.name)
print("Character Level:", char.level)
print("Job:", char.get_job_name())
print("Mesos:", char.money)
print("Fame:", char.fame)


primary_stats = char.get_primary_stats()

for stat in primary_stats:
    print(f"{stat}: {primary_stats[stat]}")
    # Str
    # Dex
    # Int
    # Luk


