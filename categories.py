import menu
from db import connect
connection,cursor = connect()
def addcat(cin):
    print("quel categorie vous voulez l ajouter")
    catname = input()

    cursor.execute("""
                   SELECT *
                   FROM categories
                   WHERE libelle = ?
                     AND CIN = ?
                   """, (catname, cin))

    tab = cursor.fetchone()

    if tab is not None:
        print("categorie already exists")
        while True:
            catname = input("gimme another category: ")

            cursor.execute("""
                           SELECT *
                           FROM categories
                           WHERE libelle = ?
                             AND CIN = ?
                           """, (catname, cin))

            tab = cursor.fetchone()

            if tab is None:
                break

            print("categorie already exists")

    cursor.execute(
        """INSERT INTO categories (libelle, CIN)
           VALUES (?, ?)""",
        (catname, cin))

    connection.commit()

    print("do you want to go back to the menu or add another category ?")
    print("press 1 if you want menu and 2 if you want to add another category")

    answer = int(input("enter your choice"))
    while answer != 1 and answer != 2:
        print("Invalid choice")
        answer = int(input("enter your choice"))

    if answer == 1:
        menu.ret(cin)
    else:
        addcat(cin)


def viewcat(cin):
    cursor.execute(
        """select idcat,libelle from categories where cin=?""",
        (cin,))

    tab = cursor.fetchall()

    if not tab:
        print("u dont have any categories")
        print("press 1 if you want menu and 2 if you want to add category")

        while True:
            answer = int(input("enter your choice"))

            if answer == 1:
                menu.ret(cin)
                break

            elif answer == 2:
                addcat(cin)
                break

            else:
                print("Invalid choice")

    else:
        j = 1

        for i in tab:
            print(str(j) + "-" + i[1])
            j += 1
            print("press 1 to go back to menu")
            ans=int(input("enter your choice"))
            while ans != 1 :
                print("Invalid choice")
                ans = int(input("enter your choice"))
            menu.ret(cin)