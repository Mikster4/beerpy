#!/usr/bin/python3
import numpy as np
import sqlite3
import sys
import os

if len(sys.argv) == 1:
    print("Usage: get_status.py [ -Aup ] <database_name.db>")

if os.path.exists(sys.argv[len(sys.argv)-1]):
    db_name = sys.argv[len(sys.argv)-1]
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    if sys.argv[len(sys.argv)-2] == "-A":
        c.execute("""
            SELECT users.name, units.product, COUNT(userunits.qty) FROM userunits
                INNER JOIN units ON userunits.unit_id = units.id
                INNER JOIN users ON userunits.user_id = users.id
                GROUP BY users.id, units.product
            """)
        names = c.fetchall()
        for name in names:
            print("Bruger: " + str(name[0] + ", Vare: " + str(name[1]) + ", antal: " + str(name[2])))
    elif sys.argv[len(sys.argv)-2] == "-u":
        c.execute("SELECT users.id, users.name, users.faction FROM users WHERE 1 ORDER BY users.faction, users.name ASC")
        names = c.fetchall()
        for name in names:
            print(int(name[0]),str(name[1]),str(name[2]))
        c.close()

    elif sys.argv[len(sys.argv)-2] == "-p":
        c.execute("SELECT units.id, units.product, units.price FROM units WHERE 1 ORDER BY units.product ASC")
        names = c.fetchall()
        for name in names:
            print("ID: " + str(name[0]) +", Produkt: " +str(name[1]) +", Pris: " + str(name[2]))
        c.close()

conn.commit()
conn.close()
