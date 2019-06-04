#!/usr/bin/python3
import barcode
from barcode.writer import ImageWriter
import numpy as np
import sqlite3
import sys
import os
import shutil

def get_accept():
    char = input("\nAre these values correct? [y]/n: ")
    if char == "y" or char == "Y":
        return True
    elif char == "n" or char == "N":
        return False
    else:
        print("Sorry, I could not read the input. Please try again.")
        get_accept()

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
        if "-C" in sys.argv:
            folder = 'barcodes'
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            print("Removed all barcodes from directory")
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
