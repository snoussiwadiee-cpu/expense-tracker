import sqlite3
from datetime import datetime
connection = sqlite3.connect('expenses.db')
cursor = connection.cursor()
def ret(cin):
    print("welcome back")
    print("chose what service u want to use")
    print(
        "1-add categorie\n 2-view categories\n 3-add expenses \n 4-view expenses \n 5-delete expenses \n 6-monthly total() \n 7-categorie statistics \n 8-compare months \n 9-return to main menu")
    answer = int(input("enter your choice"))
    match answer:
        case 1:
            addcat(cin)
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            pass
        case 8:
            pass
        case 9:
            pass
        case _:
            print("Invalid choice")
            ret(cin)

def manage(cin):
    cursor.execute('''select * from users where CIN=?''',(cin,))
    tab = cursor.fetchone()
    fullname = tab[2]+" "+tab[1]
    print("welcome"+fullname)
    print("chose what service u want to use")
    print("1-add categorie\n 2-view categories\n 3-add expenses \n 4-view expenses \n 5-delete expenses \n 6-monthly total() \n 7-categorie statistics \n 8-compare months \n 9-return to main menu")
    answer=int(input("enter your choice"))
    match answer:
        case 1:
            addcat(cin)
        case 2:
            viewcat(cin)
        case 3:
            addexpenses(cin)
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            pass
        case 8:
            pass
        case 9:
            pass
        case _:
            print("Invalid choice")
            ret(cin)
def addcat(cin):
    print("quel categorie vous voulez l ajouter")
    catname=input()
    cursor.execute("""select * from categories where libelle=?""",(catname,))
    tab = cursor.fetchone()
    if tab is not None:
        print("categorie already exists")
        addcat(cin)
    else :
        cursor.execute(
            """INSERT INTO categories (libelle, CIN)
               VALUES (?, ?)""",
                (catname, cin))
        connection.commit()
        print("do you want to go back to the menu or add another category ?")
        print("press 1 if you want menu and 2 if you want to add another category ")
        answer = int(input("enter your choice"))
        if answer == 1:
                ret (cin)
        else:
            addcat(cin)
def  viewcat(cin):
    cursor.execute("""select libelle from categories where cin=?""",(cin,) )
    tab = cursor.fetchall()
    if  not tab:
        print("u dont have any categories u need to add categories ")
        print("press 1 if you want menu and 2 if you want to add  category ")
        answer = int(input("enter your choice"))
        if answer == 1:
            ret (cin)
        else:
            addcat(cin)
    else:
        j=1
        for i in tab :
            print(str(j) + "-" + i[0])
            j+=1

def addexpenses(cin) :
    print("item categorie")
    cursor.execute("""select libelle,idcat from categories where cin=?""",(cin,) )
    tab = cursor.fetchall()
    if not tab:
        print("u dont have any categories u need to add categories pls add categories ")
        print("press 1 if you want menu")
        rep=int(input("enter your choice"))
        if rep == 1:
            ret (cin)
    else :
        print("chosse from those categories u have")
        j=1
        for i in tab:
           print(str(j)+"+"+i[0])
           j+=1
        answer=int(input("enter your choice"))
        while answer < 1 or answer > len(tab):
            print("invalid choice")
            answer=int(input("enter your choice"))
        print("item expense")
        price = float(input())
        datexp=datetime.now()
        print("item description")
        description = input()
        idcat=tab[answer-1][1]
        cursor.execute("""insert into expenses (price,idcat,date,description) values (?, ?, ?,?)""",(price,idcat,datexp,description))
        connection.commit()
        print("expense added successfully")
        print("press 1 if you want menu and 2 if you want to add another expense ")
        answer = int(input("enter your choice"))
        if answer == 1:
            ret (cin)
        else :
            addexpenses(cin)
