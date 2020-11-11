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
name = char.name  # getter for name; Sting
meso = char.money  # getter for mesos; String
job = char.get_job_name()  # this getter gives us the actual job name; String
job_id = char.job  # This one gives us job id; Int
level = char.level  # getter for levels; Int
honor_exp = char.get_stat_by_column("honorexp")  # Int

print("Now checking char info from DB...")

print("Checking the ability to fetch the following information from DB: ")
print("    > Character Name; Mesos; Job name; Job ID; Character Level; Honour EXP. \n")
assert name == "Kookiiee", f"Critical Error: Name test failed! Name: {name}; Type: {type(name)}"
assert meso == "0", f"Meso test failed! Meso count: {meso}; Type: {type(meso)}"
assert job == "Beginner", f"Job name test failed! Job name: {job}; Type: {type(job)}"
assert job_id == 0, f"Job ID test failed! Job ID: {job_id}; Type: {type(job_id)}"
assert level == 1, f"Character level test failed! Level count: {level}; Type: {type(level)}"
assert honor_exp == 0, f"Honour EXP test failed! Honour count: {honor_exp}; Type: {type(honor_exp)}"
print("Checking the ability to fetch the following information from DB: ")
print("    > User ID. \n")
assert user_id == 5, f"Database method 'get_user_id_by_name' test failed! User ID: {user_id}; Type: {type(user_id)}"
print("Char info fetch tests complete!")
print("----------------------------------")

# Character info setting tests
fame = char.fame
print("Checking the ability to write the following information to DB: ")
print("    > Mesos; Fame. \n")
char.money = "0"  # reset to baseline
char.money = "314159" # Sets money to 314,159 mesos in the database
# character now has 314,159 mesos
char = spirit.get_char_by_name("Kookiiee")  # refresh
meso = char.money  # refresh
assert meso == "314159", f"Meso setting test failed! Meso count: {meso}; Type: {type(meso)}"
char.add_mesos(2827433)  # Adds 2,827,433 to the current meso count, and saves to DB
# character now has 3,141,592 mesos
char = spirit.get_char_by_name("Kookiiee")  # refresh
meso = char.money  # refresh
assert meso == "3141592", f"Meso adding test failed! Meso count: {meso}; Type: {type(meso)}"
char.money = "0"  # reset to baseline
char.fame = 0  # reset to baseline
char.fame = 3  # Sets fame to 3 in the database
char = spirit.get_char_by_name("Kookiiee")  # refresh
fame = char.fame  # refresh
assert fame == 3, f"Fame setting test failed! Fame count: {fame}; Type: {type(fame)}"
char.add_fame(28) # Adds 28 fame to the existing count and saves to database
# character fame is now 31
char = spirit.get_char_by_name("Kookiiee")  # refresh
fame = char.fame  # refresh
assert fame == 31, f"Fame adding test failed! Fame count: {fame}; Type: {type(fame)}"
char.fame = 0  # reset to baseline
print("Char info write tests complete!")
print("----------------------------------")
