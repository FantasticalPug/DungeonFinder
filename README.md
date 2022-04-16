# DungeonFinder

Make sure you're in your Python Virtual Environment whenever entering commands into the Terminal / Command Prompt

## Setup

### Python Virtual Environment
#### Install Python
If you don't have it already, install Python (Python 3.6 or later):
##### macOS
```
brew install python3
```
##### WSL or Linux
```
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv python3-wheel python3-setuptools
```

#### Create Virtual Environment
Now create the virtual environment
```
python3 -m venv env
```

To activate your virtual environment, enter into your Terminal / Command Prompt
```
source env/bin/activate
```

To deactivate, enter into your Terminal / Command Prompt
```
deactivate
```

### Install Utilities

Make sure you're in your Python Virtual Environment

#### Install SQLite3
We will be using SQLite3 for our database

##### macOS
```
brew install sqlite3 curl
```

##### Linux and WSL
```
sudo apt-get install sqlite3 curl
```

#### Install Requirements
These commands will install many of the other requirements you will need locally to contribute to DungeonFinder
```
pip install --upgrade pip setuptools wheel
pip install html5validator
pip install -r requirements.txt
pip install -e .
```

## Database Management
The dfdb script found in the bin subdirectory will automate many functions to help with testing. Here are the usages for it (make sure you have executing permissions on the file):
```
./bin/dfdb create
./bin/dfdb destroy
./bin/dfdb reset
./bin/dfdb dump
```
Create will create the database abiding by the tables in sql/schema.sql and the data in sql/data.sql
Destroy will remove the database
Reset will essentially run destroy followed by create
Dump will output all the data currently stored in the database

## Testing & Hosting Locally
Run dfrun found in the bin subdirectory to host the site locally to test (make sure you have executing permissions on the file):
```
./bin/dfrun
```

## DungeonFinder's Structure
Most of our development will be done in the DungeonFinder subdirectory (that is the app afterall). 
static will be where static (non-changing) files are stored like logo images and CSS files for styling.
templates will be where all HTML files are stored, we are using Jinja to help with dynamicness
views will be where our Python files are stored for page rendering / generation (be sure to add an import statement in DungeonFinder/views/__init__.py to make sure the Flask can find the proper functions for rendering / generation).
