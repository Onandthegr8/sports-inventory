# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-file Python + MySQL console application (`sports_inventory.py`) that manages a school's sports-equipment inventory. It was adapted from a Class 12 project, so the code is deliberately kept simple — preserve that style when editing rather than introducing frameworks or abstractions.

## Commands

```bash
pip install -r requirements.txt              # install mysql-connector-python
copy config.example.py config.py             # Windows: create local config, then edit the password
mysql -u root -p < schema.sql                # create the database + tables (or use teacher menu option 1)
python sports_inventory.py                   # run the app
python -m py_compile sports_inventory.py     # syntax check (no build step exists)
```

There is no test suite, linter, or build tooling. The only automated check is `py_compile`.

## Configuration

- `config.py` holds `DB_CONFIG` (a dict passed straight to `mysql.connector.connect`) and `TEACHER_PASSCODE` (a string). It is **gitignored**; `config.example.py` is the committed template.
- The default database name is `sports_inventory`. Changing it means updating both `config.py`/`config.example.py` and `schema.sql`.

## Architecture

- **Module-level connection at import time.** `sports_inventory.py` runs `con = mysql.connector.connect(**DB_CONFIG)` at the top level, so *importing the module opens a real DB connection and requires the target database to already exist*. The app does not create the database itself — only the tables (via teacher menu option 1). `schema.sql` creates both.
- **Two roles, one loop.** `main()` is an infinite menu loop dispatching to `teacher_menu()` (passcode-gated) or `student_menu()`. Each menu function returns `False` to signal exit, which breaks the loop. All DB work lives in standalone `*_stock` functions that share the module-level `con`.
- **Three tables and their invariants:**
  - `Stock` — master inventory (one row per item code; quantity is the live count).
  - `shunt_stock` — items *currently* borrowed; rows are inserted on borrow and **deleted** on return.
  - `all_entries` — append-only log of every borrow (never deleted, even on return).
  - **Borrow** decrements `Stock.Quantity` and inserts into *both* `shunt_stock` and `all_entries`. **Return** increments `Stock.Quantity` and deletes from `shunt_stock` only. Keep this dual-write/single-delete pattern intact when modifying borrow/return.
- **SQL is built with `str.format`, not parameterized queries.** This is intentional (mirrors the original project). Match the existing style; do not silently rewrite to parameterized queries without being asked.
- **Table-name case sensitivity caveat.** Tables are created as `Stock` but queried as `stock`. This works only where MySQL treats table names case-insensitively (the default on Windows/macOS). It would break on a case-sensitive Linux server — keep this in mind if portability comes up.

## Testing an interactive app

The app is driven entirely by `input()`, so to exercise it programmatically: set `config.DB_CONFIG` (point it at a test database) **before** importing `sports_inventory`, create that database first, then monkeypatch `builtins.input` to feed a scripted list of responses and call `sports_inventory.main()`.
