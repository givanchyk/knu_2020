import sqlite3
import cgi
con = sqlite3.connect('DATABASE.db')
cur = con.cursor()
cur.execute("""CREATE TABLE employee (
    name TEXT NOT NULL PRIMARY KEY,
    year INT,
    address TEXT,
    unit TEXT,
    position TEXT
   );""")
cur.execute("""CREATE TABLE unit (
    name TEXT PRIMARY KEY,
    count INT
   );""")
cur.execute("""CREATE TABLE position (
    name TEXT PRIMARY KEY
   );""")
cur.execute("""CREATE TABLE order1 (
    name TEXT PRIMARY KEY
   );""")
con.commit()
con.close()
