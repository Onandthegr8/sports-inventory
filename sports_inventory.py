"""
Sports Inventory System
========================
A simple Python + MySQL console application to manage a school's sports
equipment inventory.

- Teachers (passcode-protected) can create tables, add/edit/delete stock,
  sort, search, and issue/return equipment.
- Students can view, search, borrow, and return equipment.

Database credentials and the teacher passcode are read from `config.py`
(copy `config.example.py` to `config.py` and fill in your own values).
"""

import mysql.connector

from config import DB_CONFIG, TEACHER_PASSCODE

con = mysql.connector.connect(**DB_CONFIG)


def create_stock():
    cur = con.cursor()
    query = ("create table Stock(Sno int, Item_Code int primary key, "
             "Item_Name varchar(200), Quantity int)")
    cur.execute(query)
    print("Table created successfully")
    n = int(input("Enter no. of entries to be entered in the Stock table: "))
    for i in range(1, n + 1):
        a = int(input("Please enter Item_Code: "))
        b = input("Please enter Item_Name: ")
        c = int(input("Please enter Quantity: "))
        query1 = "insert into stock values({},{},'{}',{})".format(i, a, b, c)
        cur.execute(query1)
        con.commit()


def create_shunt_stock():
    cur = con.cursor()
    query = ("create table shunt_stock(Name char(99), Class varchar(4), "
             "Section varchar(4), Item_Code int, Item_Name varchar(99), "
             "Quantity int, Date_Time varchar(200))")
    cur.execute(query)
    con.commit()


def create_all_entries():
    cur = con.cursor()
    query = ("create table all_entries(Name char(99), Class varchar(4), "
             "Section varchar(4), Item_Code int, Item_Name varchar(99), "
             "Quantity int, Date_Time varchar(200))")
    cur.execute(query)
    con.commit()


def view_table_stock():
    cur = con.cursor()
    cur.execute("select * from stock order by Sno")
    for row in cur.fetchall():
        print("-" * 99)
        print(row)
    print("-" * 99)


def view_table_shunt_stock():
    cur = con.cursor()
    cur.execute("select * from shunt_stock")
    for row in cur.fetchall():
        print("-" * 99)
        print(row)
    print("-" * 99)


def view_table_all_stock():
    cur = con.cursor()
    cur.execute("select * from all_entries")
    for row in cur.fetchall():
        print("-" * 99)
        print(row)
    print("-" * 99)


def add_stock():
    cur = con.cursor()
    cur.execute("select * from stock order by Sno")
    n = 0
    for row in cur.fetchall():
        n = row[0]
    n += 1
    e = int(input("Please enter Item_Code (4 digits): "))
    f = input("Please enter Item_Name: ")
    g = int(input("Please enter Quantity: "))
    query = "insert into stock values({},{},'{}',{})".format(n, e, f, g)
    cur.execute(query)
    con.commit()


def edit_stock():
    cur = con.cursor()
    x = int(input("Enter Item_Code: "))
    jk = input("Enter whether to 'increase' or 'decrease' quantity: ")
    y = int(input("Enter number of items: "))
    z = 0
    cur.execute("select * from stock order by Sno")
    for row in cur.fetchall():
        if x in row:
            print("Item found")
            z = 1
    if jk == 'increase':
        query = "update stock set quantity=quantity+{} where Item_Code={}".format(y, x)
    else:
        query = "update stock set quantity=quantity-{} where Item_Code={}".format(y, x)
    cur.execute(query)
    con.commit()

    cur.execute("select * from stock order by Sno")
    for row in cur.fetchall():
        if x == row[1]:
            print("-" * 99)
            print(row)
            print("-" * 99)
    if z == 0:
        print("Item not found. Please enter a valid Item_Code")


def sort_stock():
    cur = con.cursor()
    gh = input("Enter whether to sort by 'asc' or 'desc': ")
    if gh == 'asc':
        cur.execute("select Item_Code, Item_Name, Quantity from stock "
                    "order by Item_Name asc")
    else:
        cur.execute("select Item_Code, Item_Name, Quantity from stock "
                    "order by Item_Name desc")
    for row in cur.fetchall():
        print(row)
        print("-" * 99)


def search_stock():
    cur = con.cursor()
    h = int(input("Enter Item_Code to search: "))
    z = 0
    cur.execute("select * from stock order by Sno")
    for row in cur.fetchall():
        if h in row:
            print("Item_Code found")
            z = 1
    cur.execute("select * from stock where Item_Code={}".format(h))
    for row in cur.fetchall():
        print(row)
    if z == 0:
        print("Item not found. Please enter a valid Item_Code")


def delete_stock():
    cur = con.cursor()
    w = int(input("Enter Item_Code to delete: "))
    z = 0
    cur.execute("select * from stock order by Sno")
    for row in cur.fetchall():
        if w in row:
            print("Item_Code found")
            z = 1
    cur.execute("delete from stock where Item_Code={}".format(w))
    con.commit()
    if z == 1:
        print("Successfully deleted")
    else:
        print("Item not found. Please enter a valid Item_Code")


def borrow_stock_student():
    cur = con.cursor()
    name = input("Please enter your name: ")
    cls = int(input("Please enter your class: "))
    section = input("Please enter your section: ")
    item_code = int(input("Please enter the Item_Code: "))
    qty = int(input("Please enter the quantity: "))
    z = 0
    item_name = None
    cur.execute("select * from stock order by Sno")
    for row in cur.fetchall():
        if item_code in row:
            item_name = row[2]
            z = 1
    if z == 0:
        print("Item not found. Please enter a valid Item_Code")
        return

    cur.execute("select now()")
    date_time = str(cur.fetchall()[0][0])

    cur.execute("insert into shunt_stock values('{}',{},'{}',{},'{}',{},'{}')".format(
        name, cls, section, item_code, item_name, qty, date_time))
    con.commit()

    cur.execute("insert into all_entries values('{}',{},'{}',{},'{}',{},'{}')".format(
        name, cls, section, item_code, item_name, qty, date_time))
    con.commit()

    cur.execute("update stock set quantity=quantity-{} where Item_Code={}".format(
        qty, item_code))
    con.commit()

    print("Your entry has been recorded")
    cur.execute("select * from shunt_stock")
    for row in cur.fetchall():
        if item_code in row:
            print("-" * 99)
            print(row)
            print("-" * 99)


def borrow_stock_teacher():
    cur = con.cursor()
    name = input("Please enter your name: ")
    item_code = int(input("Please enter the Item_Code: "))
    qty = int(input("Please enter the quantity: "))
    z = 0
    item_name = None
    cur.execute("select * from stock order by Sno")
    for row in cur.fetchall():
        if item_code in row:
            item_name = row[2]
            z = 1
    if z == 0:
        print("Item not found. Please enter a valid Item_Code")
        return

    cur.execute("select now()")
    date_time = str(cur.fetchall()[0][0])

    cur.execute("insert into shunt_stock values('{}',NULL,NULL,{},'{}',{},'{}')".format(
        name, item_code, item_name, qty, date_time))
    con.commit()

    cur.execute("insert into all_entries values('{}',NULL,NULL,{},'{}',{},'{}')".format(
        name, item_code, item_name, qty, date_time))
    con.commit()

    cur.execute("update stock set quantity=quantity-{} where Item_Code={}".format(
        qty, item_code))
    con.commit()

    print("Your entry has been recorded")
    cur.execute("select * from shunt_stock")
    for row in cur.fetchall():
        if item_code in row:
            print("-" * 99)
            print(row)
            print("-" * 99)


def return_stock_student():
    cur = con.cursor()
    name = input("Enter student name: ")
    cls = int(input("Enter your class: "))
    section = input("Enter your section: ")
    item_code = int(input("Enter Item_Code: "))
    qty = int(input("Enter quantity of items that you are returning: "))
    z = 0
    cur.execute("select * from shunt_stock")
    for row in cur.fetchall():
        if item_code in row:
            print("Item found")
            z = 1
    if z == 0:
        print("Item not found. Please enter a valid Item_Code")
        return

    cur.execute("update stock set quantity=quantity+{} where Item_Code={}".format(
        qty, item_code))
    con.commit()

    cur.execute("delete from shunt_stock where Item_Code={}".format(item_code))
    con.commit()

    print("Deleted from shunt_stock. Stock updated.")
    print("Thank you for returning")


def return_stock_teacher():
    cur = con.cursor()
    name = input("Enter name: ")
    item_code = int(input("Enter Item_Code: "))
    qty = int(input("Enter quantity of items that you are returning: "))
    z = 0
    cur.execute("select * from shunt_stock")
    for row in cur.fetchall():
        if item_code in row:
            print("Item found")
            z = 1
    if z == 0:
        print("Item not found. Please enter a valid Item_Code")
        return

    cur.execute("update stock set quantity=quantity+{} where Item_Code={}".format(
        qty, item_code))
    con.commit()

    cur.execute("delete from shunt_stock where Item_Code={}".format(item_code))
    con.commit()

    print("Deleted from shunt_stock. Stock updated.")
    print("Thank you for returning")


def teacher_menu():
    print("MAIN MENU")
    print("1.  CREATE STOCK TABLES")
    print("2.  VIEW STOCK TABLE")
    print("3.  ADD EQUIPMENT TO STOCK TABLE")
    print("4.  EDIT THE QUANTITY OF EQUIPMENT")
    print("5.  SORT THE STOCK TABLE")
    print("6.  SEARCH ITEM FROM STOCK TABLE")
    print("7.  BORROW ITEM FROM STOCK TABLE")
    print("8.  RETURN ITEM TO STOCK TABLE")
    print("9.  DELETE ITEM FROM STOCK TABLE")
    print("10. VIEW SHUNT_STOCK (CURRENTLY BORROWED) TABLE")
    print("11. VIEW ALL_ENTRIES (LOG) TABLE")
    print("12. EXIT")
    bh = int(input("PLEASE ENTER YOUR CHOICE: "))
    if bh == 1:
        create_stock()
        create_shunt_stock()
        create_all_entries()
    elif bh == 2:
        view_table_stock()
    elif bh == 3:
        add_stock()
    elif bh == 4:
        edit_stock()
    elif bh == 5:
        sort_stock()
    elif bh == 6:
        search_stock()
    elif bh == 7:
        borrow_stock_teacher()
    elif bh == 8:
        return_stock_teacher()
    elif bh == 9:
        delete_stock()
    elif bh == 10:
        view_table_shunt_stock()
    elif bh == 11:
        view_table_all_stock()
    elif bh == 12:
        print("THANK YOU")
        return False
    else:
        print("ENTER A VALID CHOICE")
    return True


def student_menu():
    print("STUDENT ENTRY:-")
    print("MAIN MENU")
    print("1. VIEW")
    print("2. SEARCH")
    print("3. BORROW")
    print("4. RETURN")
    print("5. EXIT")
    dh = int(input("PLEASE ENTER YOUR CHOICE: "))
    if dh == 1:
        view_table_stock()
    elif dh == 2:
        search_stock()
    elif dh == 3:
        borrow_stock_student()
    elif dh == 4:
        return_stock_student()
    elif dh == 5:
        print("THANK YOU")
        return False
    else:
        print("ENTER A VALID CHOICE")
    return True


def main():
    while True:
        print("-" * 39 + " SPORTS INVENTORY SYSTEM " + "-" * 39)
        print("1. TEACHER ENTRY")
        print("2. STUDENT ENTRY")
        ch = int(input("PLEASE ENTER YOUR CHOICE: "))

        if ch == 1:
            print("TEACHER ENTRY:-")
            passcode = input("PLEASE ENTER YOUR TEACHER PASSCODE: ")
            if passcode == TEACHER_PASSCODE:
                if not teacher_menu():
                    break
            else:
                print("INCORRECT TEACHER CODE. PLEASE TRY AGAIN")
        elif ch == 2:
            if not student_menu():
                break
        else:
            print("ENTER A VALID CHOICE")


if __name__ == "__main__":
    try:
        main()
    finally:
        con.close()
