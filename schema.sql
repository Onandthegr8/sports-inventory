-- Sports Inventory System -- database schema
-- Run this once to create the database and tables:
--     mysql -u root -p < schema.sql
-- (Alternatively, use option 1 in the teacher menu to create the tables.)

CREATE DATABASE IF NOT EXISTS sports_inventory;
USE sports_inventory;

-- Master inventory of all sports equipment.
CREATE TABLE IF NOT EXISTS Stock (
    Sno        INT,
    Item_Code  INT PRIMARY KEY,
    Item_Name  VARCHAR(200),
    Quantity   INT
);

-- Items that are currently issued/borrowed (a row is removed on return).
CREATE TABLE IF NOT EXISTS shunt_stock (
    Name       CHAR(99),
    Class      VARCHAR(4),
    Section    VARCHAR(4),
    Item_Code  INT,
    Item_Name  VARCHAR(99),
    Quantity   INT,
    Date_Time  VARCHAR(200)
);

-- Permanent log of every borrow transaction.
CREATE TABLE IF NOT EXISTS all_entries (
    Name       CHAR(99),
    Class      VARCHAR(4),
    Section    VARCHAR(4),
    Item_Code  INT,
    Item_Name  VARCHAR(99),
    Quantity   INT,
    Date_Time  VARCHAR(200)
);
