#!/usr/bin/python3
import barcode
from barcode.writer import ImageWriter
import numpy as np
import sqlite3
import os
import glob, os, sys
os.chdir("./")
pics = []

if len(sys.argv) == 1:
    print("Usage: generate_admins.py <database_name.db>")
elif os.path.exists(sys.argv[len(sys.argv)-1]):
    db_name = sys.argv[len(sys.argv)-1]
    if not os.path.exists('PDF'):
        os.mkdir('PDF')
        print("PDF directory created")
    else:
        print("PDF directory already exists")
        print("Warning: You might want to run with '-C' to clear old files")
        if sys.argv[1] == "-C":
            shutil.rmtree("PDF/")
            print("Removed all files from PDF directory")

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT * FROM units")
    units = c.fetchall()
    conn.close()

    os.chdir("PDF/")
    CODE128 = barcode.get_barcode_class('code128')

    for u in units:
        code128 = CODE128(str(u[0]),writer=ImageWriter())
        code128.save(u[1])

    code128 = CODE128("0000",writer=ImageWriter())
    code128.save("ANNULER")
    code128 = CODE128("9999",writer=ImageWriter())
    code128.save("LOGUD")

    for file in glob.glob("*.png"):
        pics.append(os.path.splitext(file)[0])

    workfile = "admins.tex"
    F = open(workfile,"a")
    F.write("\\documentclass[a4paper,11pt]{article}\n")
    F.write("\\usepackage{graphicx}\n")
    F.write("\\usepackage[utf8]{inputenc}\n")
    F.write("\\usepackage[T1]{fontenc}\n")
    F.write("\\usepackage[danish]{babel}\n")
    F.write("\\usepackage{array}\n")
    F.write("\\usepackage{ragged2e}\n")
    F.write("\\begin{document}\n")
    for pic in pics:
        dot = pic.find(".")
        print (pic)
        F.write("\\"+"begin{table}[h!]\n")
        F.write("    \\begin{tabular}{  l l }\n")
        F.write("\\includegraphics[height=3cm,width=0.3\\textwidth]{"+pic+"}\n")
        F.write(" &   \\Huge{"+pic+"}\\\\ \\hline\n")
        F.write("    \\end{tabular}\n")
        F.write("\\end{table}\n")
        F.write(" \n")
        F.write(" \n")



    F.write("\\end{document}")
    F.close()

    dir = os.listdir(".")

    for item in dir:
        if item.endswith(".aux") or item.endswith(".log"):
            os.remove(item)
    os.chdir("../")
else:
    print("ERROR: Files does not exists: " + str(sys.argv[len(sys.argv)-1]))
