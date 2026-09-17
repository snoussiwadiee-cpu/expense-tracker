from db import connect
import bcrypt
from menu import *
connection,cursor = connect()


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
while True:
    print("Welcome to the application!")
    print("press 1 to create a new user or press 2 to login or press 3 to exit")

    choice = input("enter your choice")

    if not choice.isdigit():
        print("invalid choice, please try again")
        continue

    choice = int(choice)

    if choice == 1:
        createuser()
    elif choice == 2:
        login()
    elif choice == 3:
        print("Goodbye!")
        break
    else:
        print("invalid choice, please try again")