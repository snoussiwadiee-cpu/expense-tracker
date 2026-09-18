import filter
from db import connect
import menu
connection,cursor = connect()
from datetime import *
from filter import filtercat,filterdate,filterboth,filteryear,filtermonth,afficher
def addexpenses(cin):
    print("item categorie")

    cursor.execute(
        """select libelle,idcat from categories where cin=?""",
        (cin,))

    tab = cursor.fetchall()

    if not tab:
        print("u dont have any categories u need to add categories pls add categories")
        print("press 1 if you want menu")

        rep = int(input("enter your choice"))

        while rep != 1:  # CHANGED
            print("invalid choice")
            rep = int(input("enter your choice"))

        menu.ret(cin)

    else:
        print("chosse from those categories u have")

        j = 1

        for i in tab:
            print(str(j) + "+" + i[0])
            j += 1

        answer = int(input("enter your choice"))

        while answer < 1 or answer > len(tab):
            print("invalid choice")
            answer = int(input("enter your choice"))

        print("item expense")
        price = float(input())

        datexp = datetime.now()

        print("item description")
        description = input()

        idcat = tab[answer - 1][1]

        cursor.execute(
            """insert into expenses
               (price,idcat,date,description)
               values (?, ?, ?,?)""",
            (price, idcat, datexp, description))

        connection.commit()

        print("expense added successfully")
        print("press 1 if you want menu and 2 if you want to add another expense")
        answer = int(input("enter your choice"))
        while answer != 1 and answer != 2:
            print("invalid choice")
            answer = int(input("enter your choice"))

        if answer == 1:
            menu.ret(cin)
        else:
            addexpenses(cin)


def viewexpenses(cin):
    print("filer your choice of expenses")
    print(
        "press 1 if u want to filer by category and 2 if u want to filter by date and 3 if u want both and 4 if u want to see all ur expenses and 5 if u want to return to main menu")

    answer = int(input("enter your choice"))
    while answer < 1 or answer > 5:
        print("Invalid choice")
        answer = int(input("enter your choice"))

    if answer == 1:
        filtercat(cin)

    elif answer == 2:
        filterdate(cin)

    elif answer == 3:
        filterboth(cin)

    elif answer == 4:
        afficher(cin)
    else :
        menu.ret(cin)

def deleteexpenses(cin):
    print("delete your choice of expenses")
    print("press 1 if u want to filter ur expenses and 2 to go back to main menu")

    answer = int(input("enter your choice"))

    while answer not in [1, 2]:
        print("invalid choice")
        answer = int(input("enter your choice"))

    if answer == 1:
        print("select which type of filter u want")
        print("1-filtercat \n2-filterdate \n3-filterboth")

        answer = int(input("enter your choice"))

        while answer not in [1, 2, 3]:
            print("invalid choice")
            answer = int(input("enter your choice"))

        if answer == 1:
            tab = filter.filtercat(cin)

        elif answer == 2:
            tab = filter.filterdate(cin)

        else:
            tab = filter.filterboth(cin)

        j = 1

        for i in tab:
            print(str(j) + "+" + str(i[1]) + " " + i[3] + " " + str(i[4]))
            j += 1

        print("which one u want to delete")

        ans = int(input("enter your choice"))

        while ans not in range(1, j):
            print("invalid choice")
            ans = int(input("enter your choice"))
        expense = tab[ans - 1]

        cursor.execute("""
            delete from expenses
            where idcat = ?
            and date = ?
            and description = ?
        """, (expense[2], expense[3], expense[4]))

        connection.commit()

        print("expense deleted successfully")
        print("press 1 if you want menu and 2 if you want to delete another expense")

        answer = int(input("enter your choice"))

        while answer != 1 and answer != 2:
            print("invalid choice")
            answer = int(input("enter your choice"))

        if answer == 1:
            menu.ret(cin)
        else:
            deleteexpenses(cin)

    else:
        menu.ret(cin)



