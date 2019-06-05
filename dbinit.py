#!/usr/bin/python3
import sys
import sqlite3 as sqlite
import os
import datetime

if len(sys.argv) != 2:
    print("Usage: dbinit.py <database_name.py>")
if len(sys.argv) == 2:
    db_name = str(sys.argv[1])
    if os.path.exists(db_name):
        os.rename (db_name, "backups/" + db_name + str(datetime.datetime.now()) + ".backup")

    f = open(db_name, "w").write("")

    conn = sqlite.connect(db_name)
    c = conn.cursor()

    c.execute("CREATE TABLE users (id int, name text, faction text, level int)")
    c.execute("CREATE TABLE units (id INTEGER PRIMARY KEY, product text, price int, price_adj float)")
    c.execute("CREATE TABLE userunits (user_id int, unit_id int, dato datetime, qty int)")

    conn.commit()
    conn.close()
