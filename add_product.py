#!/usr/bin/python3

import sys
import numpy as np
import sqlite3

# Check lenght of input
if len(sys.argv) != 4:
    print("Usage: add_product.py <datebase.db> <product name> <product prize>")


if len(sys.argv) == 4:
    # Check if price is an integer
    if isinstance(sys.argv[3], int):
        print("Third argument must be of type int")

    else:
        product = [str(sys.argv[2]),str(sys.argv[3])]

        conn = sqlite3.connect(str(sys.argv[1]))
        c = conn.cursor()

        query = "(\"" + product[0] + "\"," + str(product[1]) + ")"
        c.execute("INSERT INTO units(product, price) VALUES " + query)

        conn.commit()
        conn.close()
