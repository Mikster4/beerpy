#!/usr/bin/python3
import barcode
from barcode.writer import ImageWriter
import numpy as np
import sqlite3
import sys
import os
import shutil

if len(sys.argv) == 1:
    print("Usage: ./generate_barcode.py [-C] <database_name.db>")
elif os.path.exists(sys.argv[len(sys.argv)-1]):
    db_name = sys.argv[len(sys.argv)-1]
    if not os.path.exists('barcodes'):
        os.mkdir('barcodes')
        print("Barecodes directory created")
    else:
        print("Barcodes directory already exists")
        print("Warning: You might want to run with '-C' to clear old barcodes")
        if sys.argv[1] == "-C":
            shutil.rmtree("barcodes/")
            print("Removd all barcodes from directory")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    users = c.fetchall()

    CODE128 = barcode.get_barcode_class('code128')
    count = 0
    for u in users:
        code128 = CODE128(str(u[0]),writer=ImageWriter())
        code128.save("barcodes/" + "_".join(u[1].split(" ")))
        count = count + 1
    conn.close()
    print("Created " + str(count) + " barcodes")
else:
    print("ERROR: Files does not exists: " + str(sys.argv[len(sys.argv)-1]))
