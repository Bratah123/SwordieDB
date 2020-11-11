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
# Set values for Meso and Fame
char.money = "314159" # Sets money to 314,159 mesos in the database
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


print("\nChecking the ability to write the following information to DB: ")
print("    > Level; Job ID; Name; Map. \n")
# Set values for Level, Job ID, Name, and Map
char.level = 10
char.job = 100  # set job ID to warrior
char.name = "Kookiie"
char.map = "100000000"

level = char.level  # re-fetch data
assert level == 10, f"Character level setting test failed! Level count: {level}; Type: {type(level)}"
char.add_level(21)  # Adds 21 to the existing count and saves to database
# character is now level 31
level = char.level  # re-fetch data
assert level == 31, f"Character level adding test failed! Level count: {level}; Type: {type(level)}"
char.level = 1  # reset to baseline

job_id = char.job  # re-fetch data
assert job_id == 100, f"Job ID setting test failed! Job ID: {job_id}; Type: {type(job_id)}"
char.job = 0  # reset job ID to beginner

name = char.name  # re-fetch data
assert name == "Kookiie", f"Name setting test failed! Name: {name}; Type: {type(name)}"
char.name = "Kookiiee"  # reset to baseline

map = char.map  # re-fetch data
assert map == "100000000", f"Map ID setting test failed! Map ID: {map}; Type: {type(map)}"
char.map = 4000011  # reset to baseline


print("\nChecking the ability to write the following information to DB: ")
print("    > Face; Hair; Skin; EXP. \n")
# Set values for Face, Hair, Skin, EXP
char.face = 20010
char.hair = 30027
char.skin = 2
char.exp = "314159"

face = char.face  # re-fetch data
assert face == 20010, f"Face ID setting test failed! Face ID: {face}; Type: {type(face)}"
char.face = 23300  # reset to baseline

hair = char.hair  # re-fetch data
assert hair == 30027, f"Hair ID setting test failed! Hair ID: {hair}; Type: {type(hair)}"
char.hair = 36786  # reset to baseline

skin = char.skin  # re-fetch data
assert skin == 2, f"Skin ID setting test failed! Skin ID: {skin}; Type: {type(skin)}"
char.skin = 0  # reset to baseline

exp = char.exp  # re-fetch data
assert exp == "314159", f"EXP test setting failed! EXP amount: {exp}; Type: {type(exp)}"
char.add_exp(2827433)
exp = char.exp  # re-fetch data
assert exp == "3141592", f"EXP test adding failed! EXP amount: {exp}; Type: {type(exp)}"
char.exp = "0"  # reset to baseline


print("\nChecking the ability to write the following information to DB: ")
print("    > STR; DEX; INT; LUK. \n")
# Set values for STR, DEX, INT, LUK
char.strength = 31
char.dex = 31
char.inte = 31
char.luk = 31

strength = char.strength  # re-fetch data
assert strength == 31, f"STR setting test failed! STR amount: {strength}; Type: {type(strength)}"
char.add_str(1)
strength = char.strength  # re-fetch data
assert strength == 32, f"STR adding test failed! STR amount: {strength}; Type: {type(strength)}"
char.strength = 12  # reset to baseline

dex = char.dex  # re-fetch data
assert dex == 31, f"DEX setting test failed! DEX amount: {dex}; Type: {type(dex)}"
char.add_dex(1)
dex = char.dex  # re-fetch data
assert dex == 32, f"DEX adding test failed! DEX amount: {dex}; Type: {type(dex)}"
char.dex = 5  # reset to baseline

inte = char.inte  # re-fetch data
assert inte == 31, f"INT setting test failed! INT amount: {inte}; Type: {type(inte)}"
char.add_inte(1)
inte = char.inte  # re-fetch data
assert inte == 32, f"INT adding test failed! INT amount: {inte}; Type: {type(inte)}"
char.inte = 4  # reset to baseline

luk = char.luk  # re-fetch data
assert luk == 31, f"LUK setting test failed! LUK amount: {luk}; Type: {type(luk)}"
char.add_luk(1)
luk = char.luk  # re-fetch data
assert luk == 32, f"LUK adding test failed! LUK amount: {luk}; Type: {type(luk)}"
char.luk = 4  # reset to baseline


print("\nChecking the ability to write the following information to DB: ")
print("    > HP; MP; AP; SP. \n")
# Set values for HP, MP, AP, SP
char.max_hp = 31
char.max_mp = 31
char.ap = 31
char.sp = 31

hp = char.max_hp  # re-fetch data
assert hp == 31, f"HP setting test failed! HP amount: {hp}; Type: {type(hp)}"
char.add_max_hp(1)
hp = char.max_hp  # re-fetch data
assert hp == 32, f"HP adding test failed! HP amount: {hp}; Type: {type(hp)}"
char.max_hp = 50  # reset to baseline

mp = char.max_mp  # re-fetch data
assert mp == 31, f"MP setting test failed! MP amount: {mp}; Type: {type(mp)}"
char.add_max_mp(1)
mp = char.max_mp  # re-fetch data
assert mp == 32, f"MP adding test failed! MP amount: {mp}; Type: {type(mp)}"
char.max_mp = 0  # reset to baseline

ap = char.ap  # re-fetch data
assert ap == 31, f"AP setting test failed! AP amount: {ap}; Type: {type(ap)}"
char.add_ap(1)
ap = char.ap  # re-fetch data
assert ap == 32, f"AP adding test failed! AP amount: {ap}; Type: {type(ap)}"
char.ap = 0  # reset to baseline

sp = char.sp  # re-fetch data
assert sp == 31, f"SP setting test failed! SP amount: {sp}; Type: {type(sp)}"
char.add_sp(1)
sp = char.sp  # re-fetch data
assert sp == 32, f"SP adding test failed! SP amount: {sp}; Type: {type(sp)}"
char.sp = 0  # reset to baseline

print("\nChar info write tests complete!")
print("----------------------------------")
