# This is a unit test for checking basic functionality
from swordie_db.database import SwordieDB

print("This is a unit test for checking basic functionality.")
print("If no error messages are shown, it means that the program is working correctly.")
print("----------------------------------\n")

# Import DB
try:
	spirit = SwordieDB(host="127.0.0.1", password="", user="root", schema="spirit", port=3306)
except Exception as e:
	print(f"Error has occurred whist attempting to load DB: \n{e}")
	sys.exit(0)

# Character info fetching tests
char = spirit.get_char_by_name("Kookiiee")
if char == None:
	print("CRITICAL ERROR: UNABLE TO FETCH CHARACTER BY NAME! TERMINATING...")
	sys.exit(0)
user_id = spirit.get_user_id_by_name("Kookiiee")
if user_id == None:
	print("CRITICAL ERROR: UNABLE TO FETCH USER ID BY NAME! TERMINATING...")
	sys.exit(0)

# Fetch character object properties
name = char.name  # getter for name; Sting
meso = char.money  # getter for mesos; String
fame = char.fame  # getter for fame; Int
job = char.get_job_name()  # return job name from ID via Hashmap; String
job_id = char.job  # getter for job id; Int
level = char.level  # getter for levels; Int
honor_exp = char.get_stat_by_column("honorexp")  # Int

map = char.map  # getter for map ID; String
face = char.face  # getter for face ID; Int
hair = char.hair  # getter for hair ID; Int
skin = char.skin  # getter for skin ID; Int
exp = char.exp  # getter for EXP amount; String

strength = char.strength  # getter for STR; Int
dex = char.dex  # getter for DEX; Int
inte = char.inte  # getter for INT; Int
luk = char.luk  # getter for LUK; Int
primary_stats = char.get_primary_stats()  # returns a dictionary of the 4 main stats; dictionary
hp = char.max_hp  # getter for max HP; Int
mp = char.max_mp  # getter for max MP; Int
ap = char.ap  # getter for free AP; Int
sp = char.sp  # getter for free SP; Int


print("Now checking char info from DB...")

print("Checking the ability to fetch the following information from DB: ")
print("    > Character Name; Mesos; Fame; Job name; Job ID; Character Level; Honour EXP. \n")
assert name == "Kookiiee", f"Critical Error: Name test failed! Name: {name}; Type: {type(name)}"
assert meso == "0", f"Meso test failed! Meso count: {meso}; Type: {type(meso)}"
assert fame == 0, f"Fame test failed! Fame count: {fame}; Type: {type(fame)}"
assert job == "Beginner", f"Job name test failed! Job name: {job}; Type: {type(job)}"
assert job_id == 0, f"Job ID test failed! Job ID: {job_id}; Type: {type(job_id)}"
assert level == 1, f"Character level test failed! Level count: {level}; Type: {type(level)}"
assert honor_exp == 0, f"Honour EXP test failed! Honour count: {honor_exp}; Type: {type(honor_exp)}"

print("Checking the ability to fetch the following information from DB: ")
print("    > Map; Face; Hair; Skin; EXP. \n")
assert map == "4000011", f"Map ID test failed! Map ID: {map}; Type: {type(map)}"
assert face == 23300, f"Face ID test failed! Face ID: {face}; Type: {type(face)}"
assert hair == 36786, f"Hair ID test failed! Hair ID: {hair}; Type: {type(hair)}"
assert skin == 0, f"Skin ID test failed! Skin ID: {skin}; Type: {type(skin)}"
assert exp == "0", f"EXP test failed! EXP amount: {exp}; Type: {type(exp)}"

print("Checking the ability to fetch the following information from DB: ")
print("    > STR; DEX; INT; LUK; Primary Stats; HP; MP; AP; SP. \n")
assert strength == 12, f"STR test failed! STR amount: {strength}; Type: {type(strength)}"
assert dex == 5, f"DEX test failed! DEX amount: {dex}; Type: {type(dex)}"
assert inte == 4, f"INT test failed! INT amount: {inte}; Type: {type(inte)}"
assert luk == 4, f"LUK test failed! LUK amount: {luk}; Type: {type(luk)}"
assert primary_stats == {'str': 12, 'dex': 5, 'int': 4, 'luk': 4}, f"Primary Stats test failed! \nExpected: {{'str': 12, 'dex': 5, 'int': 4, 'luk': 4}} \nEncountered: {primary_stats}"
assert hp == 50, f"HP test failed! HP amount: {hp}; Type: {type(hp)}"
assert mp == 0, f"MP test failed! MP amount: {mp}; Type: {type(mp)}"
assert ap == 0, f"AP test failed! AP amount: {ap}; Type: {type(ap)}"
assert sp == 0, f"SP test failed! SP amount: {sp}; Type: {type(sp)}"

print("Checking the ability to fetch the following information from DB: ")
print("    > User ID. \n")
assert user_id == 5, f"Database method 'get_user_id_by_name' test failed! User ID: {user_id}; Type: {type(user_id)}"
print("Char info fetch tests complete!")
print("----------------------------------")

# Character info setting tests
print("Checking the ability to write the following information to DB: ")
print("    > Mesos; Fame. \n")
print("Resetting meso and fame to 0, and subsequently setting new values for them.")
char.money = "0"  # reset to baseline
char.money = "314159" # Sets money to 314,159 mesos in the database
char.fame = 0  # reset to baseline
char.fame = 3  # Sets fame to 3 in the database

meso = char.money  # re-fetch data
assert meso == "314159", f"Meso setting test failed! Meso count: {meso}; Type: {type(meso)}"
char.add_mesos(2827433)  # Adds 2,827,433 to the current meso count, and saves to DB
# character now has 3,141,592 mesos
meso = char.money  # re-fetch data
assert meso == "3141592", f"Meso adding test failed! Meso count: {meso}; Type: {type(meso)}"
char.money = "0"  # reset to baseline

fame = char.fame  # re-fetch data
assert fame == 3, f"Fame setting test failed! Fame count: {fame}; Type: {type(fame)}"
char.add_fame(28) # Adds 28 fame to the existing count and saves to database
# character fame is now 31
fame = char.fame  # re-fetch data
assert fame == 31, f"Fame adding test failed! Fame count: {fame}; Type: {type(fame)}"
char.fame = 0  # reset to baseline
print("Char info write tests complete!")
print("----------------------------------")
