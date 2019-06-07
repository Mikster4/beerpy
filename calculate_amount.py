#!/usr/bin/python3
import barcode
import numpy as np
import sqlite3
import sys, os

db_name = ""

def get_accept():
    char = input("\nAre these values correct? [y]/n: ")
    if char == "y" or char == "Y":
        return True
    elif char == "n" or char == "N":
        return False
    else:
        print("Sorry, I could not read the input. Please try again.")
        get_accept()

def get_integer(value):
    if isinstance(value,int) or isinstance(value,float):
        return int(value)
    else:
        print("So")

def get_prices():
    # Original price
    UNIT_PRICE = []
    # Units bought to the event
    UNIT_OG_COUNT = []
    # Units currently found
    UNIT_PT_COUNT = []
    # Units accounted for
    UNIT_ACC_COUNT = []
    # Price adjusted for loss
    UNIT_PRICE_ADJ = []
    extra_expenses = 0
    offset = 0

    print("\nThe price of each beverage is initially set to:")
    c.execute("SELECT * FROM units")
    UNITS = c.fetchall()
    for u in UNITS:
        print(str(u[1]) + ": " + str(u[2]) + "kr.")
        UNIT_PRICE.append(int(u[2]))
    rep = True
    while not(get_accept()):
        for i in range(0, len(UNITS)):
            UNIT_PRICE[i] = input(str(UNITS[i][1]) + ": " + str(UNIT_PRICE[i]) + "kr. New price: ")

    print("\nIt is registrered that the following amount is accounted for:")
    c.execute("""
        SELECT units.product, units.price, COUNT(userunits.qty) FROM userunits
            INNER JOIN units ON userunits.unit_id = units.id
            INNER JOIN users ON userunits.user_id = users.id
            GROUP BY units.product ORDER BY units.id ASC
        """)
    row = c.fetchall()
    for r in row:
        UNIT_ACC_COUNT.append(int(r[2]))
        print(str(r[0]) + ": " + str(r[2]))

    print("\nHow many of each beverage was brought to the event?")
    for u in UNITS:
        UNIT_OG_COUNT.append(input(str(u[1]) + ": "))
    while not(get_accept()):
        for i in range(0, len(UNITS)):
            UNIT_OG_COUNT[i] = input(str(UNITS[i][1]) + ": " + str(UNIT_OG_COUNT[i]) + " units. New count: ")
    print("\nHow many units of each beverage is left?")
    for u in UNITS:
        UNIT_PT_COUNT.append(input(str(u[1]) + ": "))
    while not(get_accept()):
        for i in range(0, len(UNITS)):
            UNIT_PT_COUNT[i] = input(str(UNITS[i][1]) + ": " + str(UNIT_PT_COUNT[i]) + " units. New count: ")

    if input("Are there any extra expenses that needs to be covered? [y]/n: ") == "y":
        extra_expenses = float(input("How much? "))
        total_units = float(sum(UNIT_ACC_COUNT))
        offset = extra_expenses / total_units

    print("Based on inputs, the new prices are computed:")
    c.execute("""
        SELECT units.product, units.price, COUNT(userunits.qty) FROM userunits
            INNER JOIN units ON userunits.unit_id = units.id
            INNER JOIN users ON userunits.user_id = users.id
            GROUP BY units.product ORDER BY units.id ASC
        """)
    row = c.fetchall()
    id = 0
    for r in row:
        units_missing = (int(UNIT_OG_COUNT[id]) - int(UNIT_PT_COUNT[id]))
        units_not_acc = units_missing - int(UNIT_ACC_COUNT[id])
        new_cost = round(UNIT_PRICE[id] * (units_missing / UNIT_ACC_COUNT[id]) + offset,2)
        UNIT_PRICE_ADJ.append(new_cost)
        c.execute("UPDATE units SET price_adj = " + str(new_cost) + " WHERE units.product = " + "'" + r[0] + "'")
        conn.commit()
        id = id + 1

def save_list():
    print("\nGenerating payment info." )
    print("\nPDFlatex information:")
    os.chdir("PDF/")
    workfile = "payment_list.tex"
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

    c.execute("""
        SELECT users.name, units.product, COUNT(userunits.qty), units.price_adj FROM userunits
            INNER JOIN units ON userunits.unit_id = units.id
            INNER JOIN users ON userunits.user_id = users.id
            GROUP BY users.id, units.product
        """)
    rows = np.asarray(c.fetchall())
    print(rows)
    new = False
    first = True
    F.write("\\begin{table}[H]\n")
    F.write("\t\\begin{tabular}{l|l|r|r|r}\\hline\n")
    F.write("\t\t\\textbf{Deltager} & \\textbf{Produkt} & \\textbf{Antal} & \\textbf{Beregnet pris} & \\textbf{Total}\\\\\\hline")
    for row in rows:
        F.write("\t\t" + str(row[0]) + " & " + row[1] + " & " + row[2] + " & " + row[3] + " & " + str(round(float(row[3]) * float(row[2]),2)) + "\\\\\\hline\n")

    F.write("\t\\end{tabular}\n")
    F.write("\\end{table}\n")
    F.write("\\end{document}\n")
    F.close()
    os.system("pdflatex -interaction batchmode payment_list.tex")
    os.chdir("../")



if len(sys.argv) == 1:
    print("Usage: run.py <database_name.db>")
elif os.path.exists(sys.argv[len(sys.argv)-1]):
    db_name = sys.argv[len(sys.argv)-1]
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    get_prices()
    save_list()
    c.close()
else:
    print(sys.argv[len(sys.argv)-1] + " is not a valid database.")
