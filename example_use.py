from swordie_db.database import SwordieDB

swordie_data = SwordieDB()  # If no parameters are given, it will attempt to connect to localhost

char = swordie_data.get_char_by_name("brandon")

if char is None:
    print("Character does not exist")
else:
    print("Character Name:", char.name)
    print("Character Level:", char.level)
    print("Job:", char.get_job_name())
    print("Mesos:", char.money)
    print("Fame:", char.fame)

