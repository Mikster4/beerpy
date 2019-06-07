#!/usr/bin/python3
import barcode
from barcode.writer import ImageWriter
import numpy as np
import sqlite3
import os
import glob, os, sys
import shutil
os.chdir("./")

if len(sys.argv) == 1:
    print("Usage: printable_barcodes.py <database_name.db>")
elif os.path.exists(sys.argv[len(sys.argv)-1]):
    db_name = sys.argv[len(sys.argv)-1]
    if not os.path.exists('PDF'):
        os.mkdir('PDF')
        print("PDF directory created")
    else:
        print("PDF directory already exists")
        print("Warning: You might want to run with '-C' to clear old files")
        if sys.argv[1] == "-C":
            folder = 'PDF'
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            print("Removed all files from PDF directory")


    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT users.name, users.faction FROM users WHERE 1 ORDER BY users.id ASC")
    names = c.fetchall()
    names = np.asarray(names)

    barcodes = []
    factions = []
    for n in names:
        barcodes.append(n[0].replace(' ', '_'))
        factions.append(n[1].replace(' ', '_'))

    print("\nGenerating " + str(len(barcodes)) + " barcodes." )
    print("\nPDFlatex information:")
    os.chdir("PDF/")
    workfile = "printable_barcodes.tex"
    F = open(workfile,"w")
    F.write("\\documentclass[a4paper,11pt]{article}\n")
    F.write("\\usepackage{graphicx}\n")
    F.write("\\usepackage[utf8]{inputenc}\n")
    F.write("\\usepackage[T1]{fontenc}\n")
    F.write("\\usepackage[danish]{babel}\n")
    F.write("\\usepackage{array}\n")
    F.write("\\usepackage{ragged2e}\n")
    F.write("\\usepackage{subcaption}\n")
    F.write("\\usepackage{float}\n")
    F.write("\\usepackage[margin=0.5in]{geometry}\n")
    F.write("\\begin{document}\n")


    c = 0
    new = False
    first = True
    F.write("\\begin{figure}[H]\n")
    row = ""
    while c < len(barcodes):
        if c % 4 == 0 and not first:
            F.write("\\end{figure}\n")
            F.write("\\begin{figure}[H]\n")
            row = ""
        row += "\t\\begin{subfigure}[t]{0.24\\textwidth}\n"
        row += "\t\t\\centering\n"
        row += "\t\t\\fbox{\\includegraphics[scale=0.6]{../barcodes/" + barcodes[c] + ".png}}\n"
        row += "\t\t\\caption*{" + barcodes[c].replace('_', ' ') + " \\\ " + factions[c].replace('_',' ') + "}\n"
        row += "\t\\end{subfigure}\n"
        F.write(row)
        row = ""
        first = False
        c += 1

    F.write("\\end{figure}\n")
    F.write("\\end{document}")
    F.close()

    os.system("pdflatex -interaction batchmode printable_barcodes.tex")
    #os.remove("printable_barcodes.tex")
    os.remove("printable_barcodes.aux")
    os.remove("printable_barcodes.log")
