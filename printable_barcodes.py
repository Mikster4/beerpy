#!/usr/bin/python3
import barcode
from barcode.writer import ImageWriter
import numpy as np
import sqlite3
import os
import glob, os, sys
os.chdir("./")

if len(sys.argv) == 1:
    print("Usage: printable_barcodes.py <name_list.csv>")
elif os.path.exists(sys.argv[len(sys.argv)-1]):
    name_list = sys.argv[len(sys.argv)-1]
    if not os.path.exists('PDF'):
        os.mkdir('PDF')
        print("PDF directory created")
    else:
        print("PDF directory already exists")
        print("Warning: You might want to run with '-C' to clear old files")
        if sys.argv[1] == "-C":
            shutil.rmtree("PDF/")
            print("Removed all files from PDF directory")

    names = open(name_list).readlines()
    barcodes = []
    factions = []
    for n in names:
        barcodes.append(n.split(',')[0].replace(' ', '_'))
        factions.append(n.split(',')[2].replace(' ', '_'))

    os.chdir("PDF/")
    workfile = "printable_barcodes.tex"
    F = open(workfile,"a")
    F.write("\\documentclass[a4paper,11pt]{article}")
    F.write("\\usepackage{graphicx}")
    F.write("\\usepackage[utf8]{inputenc}")
    F.write("\\usepackage[T1]{fontenc}")
    F.write("\\usepackage[danish]{babel}")
    F.write("\\usepackage{array}")
    F.write("\\usepackage{ragged2e}")
    F.write("\\usepackage{subcaption}")
    F.write("\\usepackage{float}")
    F.write("\\begin{document}")


    c = 0
    new = False
    first = True
    F.write("\\begin{figure}[H]\n")
    row = ""
    while c < len(barcodes):
        if c % 3 == 0 and not first:
            F.write(row)
            F.write("\\end{figure}\n")
            F.write("\\begin{figure}[H]\n")
            row = ""
        row += "\\begin{subfigure}[t]{0.3\\textwidth}\n"
        row += "\\centering\n"
        row += "\\fbox{\\includegraphics[scale=0.6]{../barcodes/" + barcodes[c] + ".png}}\n"
        row += "\\caption*{" + barcodes[c].replace('_', ' ') + " \\\ " + factions[c].replace('_',' ') + "}\n"
        row += "\\end{subfigure}\n"

        first = False
        c += 1

    print(type(barcodes[0]))
    F.write("\\end{figure}\n")
    F.write("\\end{document}")
    F.close()

    os.system("pdflatex printable_barcodes.tex")
    #os.remove("output.tex")
    os.remove("printable_barcodes.aux")
    os.remove("printable_barcodes.log")
