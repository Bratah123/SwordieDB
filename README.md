# SwordieDB
### [SwordieDB PyPi Page](https://pypi.org/project/swordiedb/)

SwordieDB is a pip-compatible Python package designed for use in development of SwordieMS-based MapleStory private server tools (e.g. Discord bots).  

The SwordieDB API allows access to character stats in the form of objects, for easy manipulation.  

**Current Status:** In Active Development  
**Developmental Progress:** ![70%](https://progress-bar.dev/70) (arbitrary number - to be tracked by Brandon)  
## Installation
Note: You are recommended to install to the project virtual environment.
- In the python terminal type the follow command:
    `pip install swordiedb`
   - Too avoid any issues make sure to have these commands ran prior too installing swordiedb
    - `pip install -U setuptools`
    - `pip install -U wheel`
- Now you should have access to swordie_db module
    - Import: `from swordie_db.database import SwordieDB`
## Examples
See the [examples page](EXAMPLES.md) for sample code fragments.
## Technical Details
|  | Target Minimum | Target Maximum |
|---|---|---|
| Python | 3.6 | 3.8.5 |

To be tested:
 - [ ] Python 3.8.6
    - TODO: KOOKIIE
 - [ ] Python 3.9
    - TODO: KOOKIIE
 - [ ] Python 3.10
    - Awaiting stable release
    
### How to build
#### Generate the virtual environment
  - In the root of the repository, create a virtual environment using `Python -m venv venv`
    - Substitute "Python" with whichever command you have assigned to Python 3.6 - 3.8
  - Activate the virtual environment using `call venv\scripts\activate.bat` in Command Prompt 
    - The command is `venv/scripts/activate` in Power Shell
    - Note: PowerShell can take both backslash and forward slashes, but CMD only accepts backslashes
    - Note: You can deactivate the venv by using the command deactivate
  - Use the command `venv/scripts/pip install -r requirements.txt` to install the required modules
    - Use `venv\scripts\pip install wheel`, if the above commands throw errors
