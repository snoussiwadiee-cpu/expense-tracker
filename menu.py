import sqlite3
from datetime import datetime
from dis import CALL_INTRINSIC_1
from tokenize import tabsize
from db import connect
import categories
import expenses
connection,cursor = connect()

def ret(cin):
    print("welcome back")
    print("chose what service u want to use")
    print(
        "1-add categorie\n 2-view categories\n 3-add expenses \n 4-view expenses \n 5-delete expenses \n 6-monthly total \n 7-categorie statistics \n 8-compare months \n 9-logout")

    answer = int(input("enter your choice"))

    match answer:
        case 1:
            categories.addcat(cin)
        case 2:
            categories.viewcat(cin)
        case 3:
            expenses.addexpenses(cin)
        case 4:
            expenses.viewexpenses(cin)
        case 5:
            expenses.deleteexpenses(cin)
        case 6:
            pass
        case 7:
            pass
        case 8:
            pass
        case 9:
            exit()
        case _:
            print("Invalid choice")
            ret(cin)


def manage(cin):
    cursor.execute('''select * from users where CIN=?''', (cin,))
    tab = cursor.fetchone()

    fullname = tab[2] + " " + tab[1]
    print("welcome " + fullname)

    print("chose what service u want to use")
    print(
        "1-add categorie\n 2-view categories\n 3-add expenses \n 4-view expenses \n 5-delete expenses \n 6-monthly total \n 7-categorie statistics \n 8-compare months \n 9-logout")

    answer = int(input("enter your choice"))
    match answer:
        case 1:
            categories.addcat(cin)
        case 2:
            categories.viewcat(cin)
        case 3:
            expenses.addexpenses(cin)
        case 4:
            expenses.viewexpenses(cin)
        case 5:
            expenses.deleteexpenses(cin)
        case 6:
            pass
        case 7:
            pass
        case 8:
            pass
        case 9:
            exit()
        case _:
            print("Invalid choice")
            ret(cin)