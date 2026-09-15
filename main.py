import sqlite3
import bcrypt
from menu import *

connection = sqlite3.connect('expenses.db')
cursor = connection.cursor()

def createuser():
    cin = int(input('Enter your CIN number: '))
    name = input('Enter your name: ')
    surname = input('Enter your surname: ')
    pswd = input('Enter your password: ')
    pswd=bcrypt.hashpw(pswd.encode("utf-8"), bcrypt.gensalt(12))

    cursor.execute(
        '''SELECT * FROM users WHERE CIN = ?''',
        (cin,)
    )

    result = cursor.fetchone()

    if result is None:
        cursor.execute(
            '''INSERT INTO users (CIN, name, lastname, password)
               VALUES (?, ?, ?, ?)''',
            (cin, name, surname, pswd)
        )
        connection.commit()

        print("User created successfully!")

    else:
        print("This user already exists!")
def login():
    cin = int(input('Enter your CIN number: '))
    pswd = input('Enter your password: ')

    cursor.execute(
        """SELECT * FROM users WHERE CIN = ?""",
        (cin,)
    )

    result = cursor.fetchone()

    if result is None:
        print("The user does not exist!")
    else:
        stored_password = result[3]

        if bcrypt.checkpw(
            pswd.encode("utf-8"),
            stored_password
        ):
            manage(cin)
        else:
            print("Password not matched!")
#programme principale
print("Welcome to the application!")
print("press 1 to create a new user or press 2 to login or press 3 to exit")
choice = int(input("enter your choice"))
if choice == 1:
        createuser()
elif choice == 2:
        login()
else :
        exit()