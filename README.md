# Sports Inventory System

A simple **Python + MySQL** console application for managing a school's sports
equipment inventory. It records the stock of equipment (balls, rackets, etc.),
lets students borrow and return items, and keeps a log of every transaction.

Originally built as a Class 12 Computer Science project, then cleaned up into a
runnable, self-contained repository.

## Features

- **Two roles**, each with its own menu:
  - **Teacher** (passcode-protected): create tables, add / edit / delete stock,
    sort, search, issue and return equipment, and view all tables.
  - **Student**: view and search available stock, borrow and return equipment.
- **Live inventory** — stock quantity updates automatically on every borrow and
  return.
- `shunt_stock` tracks items that are **currently borrowed**; `all_entries`
  keeps a **permanent log** of every borrow transaction.

## Tech stack

- Python 3.7+
- MySQL 8.x
- [`mysql-connector-python`](https://pypi.org/project/mysql-connector-python/)

## Project structure

```
.
├── sports_inventory.py   # Main application
├── config.example.py     # Config template (copy to config.py)
├── schema.sql            # Database schema (optional helper)
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Create the database** — either run the schema file, or let the app create
   the tables via teacher-menu option 1:

   ```bash
   mysql -u root -p < schema.sql
   ```

3. **Configure your credentials** — copy the template and edit it with your
   MySQL password and a teacher passcode:

   ```bash
   copy config.example.py config.py     # Windows
   cp   config.example.py config.py     # macOS / Linux
   ```

   `config.py` is gitignored, so your password is never committed.

4. **Run the app**

   ```bash
   python sports_inventory.py
   ```

## Usage

On launch you choose **Teacher** or **Student**.

- The **teacher menu** asks for the passcode set in `config.py`
  (`TEACHER_PASSCODE`). The first time, use option **1** to create the three
  tables, then add stock with option **3**.
- The **student menu** lets you view, search, borrow, and return equipment.

## Database tables

| Table         | Purpose                                       |
|---------------|-----------------------------------------------|
| `Stock`       | Master inventory: item code, name, quantity   |
| `shunt_stock` | Items currently issued (removed on return)    |
| `all_entries` | Permanent log of every borrow transaction     |

## Notes

This is a learning project. The SQL statements are built with string
formatting and the interface is console-based, mirroring the original school
project — kept intentionally simple. Contributions and improvements are welcome.
