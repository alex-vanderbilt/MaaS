# Movies as a Service

### General Tech Stack:

Development Methodology: Agile

Technologies used: Flask, Python

Version Control: GitHub

Project Management System: GitHub Projects

Test: PyTest/PyUnit

Continuous Integration: GitHub Actions

Build Framework: .NET (?)



### Basic Install Instructions:

1. Clone the repo
2. Navigate to the root of the repo
3. Activate the virtual environment, and install the requirements:

```
source venv/Scripts/activate
pip install -r requirements.txt
```

4. Set Flask environment variables:

```
export FLASK_ENV=development
export FLASK_APP=app
```

5. Start flask (output should look as follows)

```
$ flask run
 * Serving Flask app 'app' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 649-503-402
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

6. Navigate to: http://127.0.0.1:5000/

### Inserting Data into SQLite3 Table
Statically:
```
sql_command = """CREATE TABLE (insert table name here) (
val1 TYPE PRIMARY KEY,
val2 TYPE,
.,
.,
valN TYPE);

sql_command = """INSERT INTO (above table name) VALUES (val1Type,val2Type,...,val3Type);"""
crsr.execute(sql_command)
```
Dynamically:
```
sql_command = """CREATE TABLE (insert table name here) (
val1 TYPE PRIMARY KEY,
val2 TYPE,
.,
.,
valN TYPE);
v1 = "something"
v2 = "in the"
vN = "water"

crsr.execute("""INSERT INTO credentials (val1, val2, valN) VALUES (?,?,?)""", (val1, val2, valN))
```