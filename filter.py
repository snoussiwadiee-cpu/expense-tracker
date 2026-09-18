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
    return tab1

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
        return tab


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
        return tab

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
        return tab
def filterboth(cin):
    cursor.execute(
        """select idcat, libelle
           from categories
           where cin = ?""",
        (cin,))

    tab = cursor.fetchall()

    if not tab:
        print("u dont have any categories")
        menu.ret(cin)

    print("which category do u want to filter ?")

    answer = int(input("enter your choice"))

    while answer < 1 or answer > len(tab):
        print("invalid choice")
        answer = int(input("enter your choice"))

    print("press 1 if u want to filter on day")
    print("press 2 if u want to filter on month")
    print("press 3 if u want to filter on year")

    ans = int(input("enter your choice"))

    while ans < 1 or ans > 3:
        print("invalid choice")
        ans = int(input("enter your choice"))

    if ans == 1:
        print("gimme the date u want to filter ?")
        print("use this form pls year-month-day")

        Date = input("gimme a date sous la forme de aaaa-mm-dd")

        cursor.execute("""
            select e.price, c.libelle, e.description
            from expenses e
            join categories c
            on e.idcat = c.idcat
            where c.CIN = ?
            and e.idcat = ?
            and date(e.date) = ?
        """, (cin, tab[answer - 1][0], Date))

        tab = cursor.fetchall()
        if not tab:
            print("u dont have any expenses under these conditions")
            print("press 1 if you want menu")

            ans = int(input("enter your choice"))

            while ans != 1:
                print("invalid choice")
                ans = int(input("enter your choice"))

            menu.ret(cin)

        else:
            j = 1
            for i in tab:
                print(str(j) + "|" + str(i[0]) + " " + i[1] + " " + str(i[2]))
                j += 1
    elif ans == 2:
        print("gimme the month u want to filter ?")
        month = input()

        cursor.execute("""
                       select e.price, c.libelle, e.description
                       from expenses e
                                join categories c
                                     on e.idcat = c.idcat
                       where c.CIN = ?
                         and e.idcat = ?
                         and strftime('%m', e.date) = ?
                       """, (cin, tab[answer - 1][0], month))

        tab = cursor.fetchall()
        if not tab:
            print("u dont have any expenses under these conditions")
            print("press 1 if you want menu")

            ans = int(input("enter your choice"))

            while ans != 1:
                print("invalid choice")
                ans = int(input("enter your choice"))

            menu.ret(cin)

        else:
            j = 1
            for i in tab:
                print(str(j) + "|" + str(i[0]) + " " + i[1] + " " + str(i[2]))
                j += 1
    elif ans == 3:
        print("gimme the year u want to filter ?")
        year = input()
        cursor.execute("""
                       select e.price, c.libelle, e.description
                       from expenses e
                                join categories c
                                     on e.idcat = c.idcat
                       where c.CIN = ?
                         and e.idcat = ?
                         and strftime('%Y', e.date) = ?
                       """, (cin, tab[answer - 1][0], year))

        tab = cursor.fetchall()
        if not tab:
            print("u dont have any expenses under these conditions")
            print("press 1 if you want menu")

            ans = int(input("enter your choice"))

            while ans != 1:
                print("invalid choice")
                ans = int(input("enter your choice"))

            menu.ret(cin)

        else:
            j = 1
            for i in tab:
                print(str(j) + "|" + str(i[0]) + " " + i[1] + " " + str(i[2]))
                j += 1
            return tab

def afficher(cin):
    print("voici tous vos expenses ")
    cursor.execute("""select e.price, c.libelle, e.description from expenses e join categories c on e.idcat = c.idcat where c.cin=?""",(cin,))
    tab = cursor.fetchall()
    if not tab:
        print("u dont have any expenses")
        print("press 1 if you want menu")
        ans = int(input("enter your choice"))
        while ans != 1:
            print("invalid choice")
            ans = int(input("enter your choice"))
        menu.ret(cin)
    else :
        j=1
        for i in tab :
            print(str(j) + "|" + str(i[0]) + " " + i[1] + " " + str(i[2]))
            j += 1
        print("press 1 to go back to menu")
        ans = int(input("enter your choice"))
        while ans != 1:
            print("invalid choice")
            ans = int(input("enter your choice"))
        menu.ret(cin)
        return tab