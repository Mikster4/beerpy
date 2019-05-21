#!/usr/bin/python3
import numpy as np
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute("""
            SELECT users.name, units.product, COUNT(units.id) FROM userunits
                INNER JOIN units ON userunits.unit_id = units.id
                INNER JOIN users ON userunits.user_id = users.id
                GROUP BY users.id, units.product
            """)
names = c.fetchall()
for name in names:
    print(name)

conn.commit()
conn.close()
