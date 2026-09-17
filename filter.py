from db import connect
import menu
connection,cursor = connect()
import expenses
from datetime import *
def filtercat(cin):
    cursor.execute(
        """select idcat,libelle from categories where cin=?""",
        (cin,))

    tab = cursor.fetchall()

    if not tab:
        print("u dont have any categories")
        menu.ret(cin)
        return

    print("which category do u want to filter ?")

    answer = int(input("enter your choice"))

    while answer < 1 or answer > len(tab):
        print("invalid choice")
        answer = int(input("which category do u want to filter ?"))

    cursor.execute(
        """select * from expenses where idcat=?""",
        (tab[answer - 1][0],))

    tab1 = cursor.fetchall()

    if not tab1:
        print("u dont have any expenses under that category")
        print("press 1 if you want menu and 2 if you want to add expense")

        ans = int(input("enter your choice"))

        # CHANGED: validate choice
        while ans != 1 and ans != 2:
            print("invalid choice")
            ans = int(input("enter your choice"))

        if ans == 1:
            menu.ret(cin)
        else:
            expenses.addexpenses(cin)

    else:
        j = 1

        print("expenses under that category")

        for i in tab1:
            print(str(j) + "-" + i[4] + " " + str(i[1]) + " " + str(i[3]))
            j += 1


def filterdate(cin):
    print("gimme the date u want to filter ?")
    print("use this form pls year-month-day")  # CHANGED

    answer = input("gimme a date")

    cursor.execute("""
                   SELECT e.price, c.libelle, e.description
                   FROM expenses e
                            JOIN categories c
                                 ON e.idcat = c.idcat
                   WHERE c.CIN = ?
                     AND date(e.date) = ?
                   """, (cin, answer))

    tab = cursor.fetchall()

    if not tab:
        print("u dont have any expenses under that date")
        print("press 1 if you want menu")

        ans = int(input("enter your choice"))

        while ans != 1:
            print("invalid choice")
            print("press 1 if you want menu")
            ans = int(input("enter your choice"))

        menu.ret(cin)

    else:
        k = 1

        for i in tab:
            print(str(k) + "|" + i[1] + " " + str(i[2]) + " " + str(i[0]))
            k += 1


def filtermonth(cin):
    print("gimme the month u want to filter ?")

    month = int(input("gimme a month"))


    while month not in range(1, 13):
        print("invalid choice")
        print("press 1 if you want menu and 2 if you want to try again")

        answer = int(input("enter your choice"))

        while answer != 1 and answer != 2:
            print("invalid choice")
            answer = int(input("enter your choice"))

        if answer == 1:
            menu.ret(cin)
            return

        month = int(input("gimme a month"))

    cursor.execute("""
                   SELECT e.price, c.libelle, e.description
                   FROM expenses e
                            JOIN categories c
                                 ON e.idcat = c.idcat
                   WHERE c.CIN = ?
                     AND strftime('%m', e.date) = ?
                   """, (cin, str(month).zfill(2)))

    tab = cursor.fetchall()

    if not tab:
        print("u dont have any expenses under that month")
        print("press 1 if you want menu")

        ans = int(input("enter your choice"))

        while ans != 1:
            print("invalid choice")
            print("press 1 if you want menu")
            ans = int(input("enter your choice"))

        menu.ret(cin)

    else:
        k = 1

        for i in tab:
            print(str(k) + "|" + i[1] + " " + str(i[2]) + " " + str(i[0]))
            k += 1


def filteryear(cin):
    print("gimme the year u want to filter ?")

    now = datetime.now().year

    year = int(input("gimme a year"))

    while year > now:
        print("invalid choice")
        print("press 1 if you want menu and 2 if you want to try again")

        answer = int(input("enter your choice"))

        while answer != 1 and answer != 2:
            print("invalid choice")
            print("press 1 if you want menu and 2 to retry")
            answer = int(input("enter your choice"))

        if answer == 1:
            menu.ret(cin)
            return

        year = int(input("gimme a year"))

    cursor.execute("""
                   SELECT e.price, c.libelle, e.description
                   FROM expenses e
                            JOIN categories c
                                 ON e.idcat = c.idcat
                   WHERE c.CIN = ?
                     AND strftime('%Y', e.date) = ?
                   """, (cin, str(year)))
    tab = cursor.fetchall()

    if not tab:
        print("u dont have any expenses under that year")
        print("press 1 if you want menu")

        ans = int(input("enter your choice"))

        while ans != 1:
            print("invalid choice")
            print("press 1 if you want menu")
            ans = int(input("enter your choice"))

        menu.ret(cin)

    else:
        k = 1

        for i in tab:
            print(str(k) + "|" + i[1] + " " + str(i[2]) + " " + str(i[0]))
            k += 1
def filterboth(cin) :
    pass
def afficher(cin):
    pass