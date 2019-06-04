#!/usr/bin/python3
import numpy as np
import sqlite3
import sys, os

first_id = 1000

if len(sys.argv) == 1:
    print("Usage: ./add_users.py <name_list> [-a <int>] <database_name.db>")
elif os.path.exists(sys.argv[len(sys.argv)-1]):
    db_name = str(sys.argv[len(sys.argv)-1])
    students = np.genfromtxt(str(sys.argv[1]), delimiter=',', dtype=(str))
    if "-a" in sys.argv:
        amount = int(sys.argv[(int(sys.argv.index("-a") + 1))])
        for i in range(0,amount):
            students = np.append(students, [['Ukendt ' + str(i), '0', 'Deltager']], axis=0)

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    id = first_id
    for s in students:
        name, level, faction = s
        query = "(" + str(id) + ",\"" + name + "\",\"" + faction + "\"," + level + ")"
        c.execute("INSERT INTO users(id, name, faction, level) VALUES " + query)
        id += 1

    conn.commit()
    conn.close()
