# SwordieDB
https://pypi.org/project/swordiedb/

SwordieDB is a Maplestory Python-based pip package that allows access to information in SwordieMS database.

This API lets you have access to character stats as an object, allowing you to edit any stats easily.
## Installation
- In the python terminal type the follow command:
    `pip install swordiedb`
   - Too avoid any issues make sure to have these commands ran as well
    - `pip install -U setuptools`
    
      `pip install -U wheel`
- Now you should have access to swordie_db module
    - Import: `from swordie_db.database import SwordieDB`
## Examples
- How to create a character object and swordie database object.
    ```python
    from swordie_db.database import SwordieDB
    
    # Creating a swordie database object
    swordie = SwordieDB() # When provided with empty parameters, it will connect to localhost
    
    char = swordie.get_char_by_name("brandon") # Creating a character object from database
    ```
- Creating a database object with specific login information.
    ```python
    from swordie_db.database import SwordieDB
    
    # Parameters for creating a Swordie database object
    swordie = SwordieDB(host="53.153.23.124", password="password", user="root", schema="swordie")
    ```
- Getting information from a character (getters).
    ```python
    from swordie_db.database import SwordieDB
    
    # Boiler plate code
    swordie = SwordieDB()
    
    char = swordie.get_char_by_name("brandon") # Creating character object
    
    name = char.name # getter for name
    meso = char.money # getter for mesos
    job = char.get_job_name() # this getter gives us the actual job name
    job_id = char.job # This one gives us job id
    level = char.level # getter for levels
  
    # getting a value from a column that isn't a class property
    honor_exp = char.get_stat_by_column("honorexp") 
    
    print("Character name:", name)
    print("Character mesos:", meso)
    print("Character job:", job)
    print("Character level:", level)
    print("Character honor exp:", honor_exp)
    ```
- Writing new data to database from a character (setters).
    - Note: All setter methods in the character class automatically saves to database after setting.
    ```python
    from swordie_db.database import SwordieDB
    
    # Boiler plate code
    swordie = SwordieDB()
    
    char = swordie.get_char_by_name("brandon") # Creating character object
    
    char.money = 999999 # Sets money to 999,999 mesos in the database
    # character now has 999,999 mesos
    
    char.add_money(1) 
    # Adds to the current meso count, I.E 999999 + 1 and saves in the database
    # character now has 1,000,000
    
    char.fame = 2000 # Sets fame to 2000 and saves to database
    
    char.add_fame(1) # Adds 1 fame to the existing count and saves to database
    ```
- Setting stats that may not exist as a property in character class.
    ```python
    from swordie_db.database import SwordieDB
    
    # Boiler plate code
    swordie = SwordieDB()
    
    char = swordie.get_char_by_name("brandon")
    
    char.set_stat_by_column("honorexp", 521) 
    # sets the column "honorexp" in SQL to value of 521 and save
    ```

- Setting new stats without the use of a character object
    ```python
    from swordie_db.database import SwordieDB
    
    # Boiler plate code
    swordie = SwordieDB()
    
    swordie.set_char_stat("brandon", "level", 250) 
    # setting the character brandon to be level 250
    # set_char_stat(name, column, value)
    ```
