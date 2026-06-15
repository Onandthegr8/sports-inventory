"""Database and application configuration.

Copy this file to `config.py` and fill in your own values:

    copy config.example.py config.py      (Windows)
    cp   config.example.py config.py       (macOS / Linux)

`config.py` is listed in .gitignore, so your MySQL password is never
committed to git.
"""

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",                 # <-- your MySQL password
    "database": "sports_inventory",
}

# Passcode required to open the teacher menu.
TEACHER_PASSCODE = "0000"
