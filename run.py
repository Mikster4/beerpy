#!/usr/bin/python3
# coding=utf-8
import numpy as np
import sqlite3
import random
import os, sys
import time

cancel = "0000"
submit = "9999"

greetings = ['Hvad så, hvem er du?',
             'Hvad så, kommer du tit her? Hvad hedder du?',
             'Hyggeligt at møde dig, hvad hedder du?',
             'Kæft du ser godt ud, hvad hedder du?',
             'Jeg var også ved at blive tørstig. Hvad må jeg kalde dig?',
             'Tørstig? Scan din stregkode.',
             'BUND! Nåe nej, du skal lige købe noget først. Scan din stregkode.']

bartender_requests = ['Velkommen til baren, _! Hvad skulle det være?',
                      'Hvad skulle det være?',
                      'Hvad ønsker du dig mest, _?',
                      'Hvordan kan jeg hjælpe dig, _?',
                      '_, min ven!',
                      '_! _! Skål!',
                      'Det er farligt derude, her, køb en bajs.']

bartender_replies = ['Dit køb er godkendt',
                     'Nyd dine drikkevarer',
                     'Skål smukke!',
                     'Skål!',
                     'Så meget kan du da slet ikke drikke?',
                     'Du tør ikke bunde!',
                     'Jeg kan bunde hurtigere end dig.',
                     'Det er noteret, at du nu har større sandsyndlighed for at vinde ølpokalen.',
                     'Tillykke! Du har vundet retten til at købe en øl mere! Kom igang!',
                     'Bund.']

def grab_a_beer():
    nameID = input("{0}\n".format(greetings[random.randint(0, len(greetings) - 1)]))
    c.execute("SELECT name FROM users WHERE id =" + nameID)
    name = c.fetchone()
    if name is None:
        print("Du står vist ikke på listen? Få lige fat i en SVEDIG.")
        time.sleep(5)
        os.system("clear")
        grab_a_beer()

    # Everything went well!
    name = name[0]

    # Person specific messages.
    if name == "Magnus Gilsborg":
        print("\n\tFückboi.\n")
    if name == "Sebastian Lokmann":
        print("\n\tSvagdrikker.\n")

    beer = input("{0}\n".format(bartender_requests[random.randint(0, len(bartender_requests) - 1)]).replace("_", name))

    # First warning
    if beer == nameID:
        print("\n" + name + ", du er allerede logget ind.")
        beer = input("Scan din drikkevare i stedet!\n")

    # Second warning
    if beer == nameID:
        print("\n" + name + ", homie, min ven, stive-lis, du er allerede logget ind.")
        beer = input("Prøv igen. Scan din drikkevare!\n")

    # The person scanned is clearly retarded and does not deserve a beer
    if beer == nameID:
        print("\n\t"+name +", DNUR pls\n")
        print("Vent venligst")
        time.sleep(5)
        os.system("clear")
        grab_a_beer()

    if beer == cancel:
        print("Okay, jeg vil holde dine drikkevarer kolde til dig. Kom igen snart!")
        print("Intet køb registreret. Vent et øjeblik.")
        time.sleep(3)
        os.system("clear")
        grab_a_beer()

    try:
        buying = 1
        while buying:
            c.execute("SELECT id, product FROM units WHERE id =" + beer)
            product = c.fetchone()
            print("Du har valgt en " + product[1])
            query = "(\"" + nameID + "\"," + str(product[0]) + ",1)"
            c.execute("INSERT INTO userunits(user_id, unit_id, qty) VALUES " + query)
            beer = input("Ønsker du at købe mere, så scan det nu. . Ellers afslut købet ved at scanne 'LOG OUT' stregkoden.\n")

            if beer == submit:
                conn.commit()
                print("{0}".format(bartender_replies[random.randint(0, len(bartender_replies) - 1)]))
                buying = 0
                time.sleep(4)
                os.system("clear")
            if beer == cancel:
                conn.rollback()
                print("Jeg er skuffet. Kom snart igen.")
                print("Intet køb registreret. Vent venligst.")
                time.sleep(2)
                os.system("clear")
                buying = 0
    except:
        print("Noget gik galt. Prøv igen. Intet køb registreret.")
        conn.rollback()
        time.sleep(3)
        os.system("clear")
    grab_a_beer()

if len(sys.argv) == 1:
    print("Usage: run.py <database_name.db>")
elif os.path.exists(sys.argv[len(sys.argv)-1]):
    db_name = sys.argv[len(sys.argv)-1]

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    grab_a_beer()
else:
    print(sys.argv[len(sys.argv)-1] + " is not a valid database.")
