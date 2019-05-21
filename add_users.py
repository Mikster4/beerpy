#!/usr/bin/python3
import numpy as np
import sqlite3

first_id = 1000

if len(sys.argv) != 3:
    print("Usage: add_users.py <name_list.csv> <database_name.db>")
if len(sys.argv) == 3:
    students = np.genfromtxt(str(sys.argv[1]), delimiter=',', dtype=(str))

    conn = sqlite3.connect(str(sys.argv[2]))
    c = conn.cursor()

    id = first_id
    for s in students:
        name, level, faction = s
        query = "(" + str(id) + ",\"" + name + "\",\"" + faction + "\"," + level + ")"
        c.execute("INSERT INTO users(id, name, faction, level) VALUES " + query)
        id += 1

        conn.commit()
        conn.close()
