# SwordieDB
### [SwordieDB PyPi Page](https://pypi.org/project/swordiedb/)

SwordieDB is a pip-compatible Python package designed for use in development of SwordieMS-based MapleStory private server tools (e.g. Discord bots).  

The SwordieDB API allows access to character stats in the form of objects, for easy manipulation.  

**Current Status:** In Active Development  
**Developmental Progress:** ![70%](https://progress-bar.dev/70) (arbitrary number - to be tracked by Brandon)  
## Installation
Note: You are recommended to install to the project virtual environment.
- In the terminal type the follow command: `pip install swordiedb`  
    - Note: use system shell and not the Python REPL for pip!
    - To avoid any issues make sure to have these commands run prior to installing SwordieDB:
        - `pip install -U setuptools`
        - `pip install -U wheel`
- Now to verify that you have access to the swordie_db module:
    - Try this import statement in the Python terminal: `from swordie_db.database import SwordieDB`
## Examples
See the [Code Examples page](https://github.com/Bratah123/SwordieDB/wiki/Examples) for sample code fragments.
## Technical Details
Please refer to the [Technical Details page](https://github.com/Bratah123/SwordieDB/wiki/Technical-Details) for details, as well as detailed instructions for how to build this package for testing.  