from db import connect
import os
import getpass
import bcrypt
from menu import *
import smtplib
from random import randint
import banbot
connection,cursor = connect()


def createuser():
    cin= int(input('Enter your CIN number: '))
    name = input('Enter your name: ')
    surname = input('Enter your surname: ')
    pswd = input('Enter your password: ')
    pswd=bcrypt.hashpw(pswd.encode("utf-8"), bcrypt.gensalt(12))
    mail=input('Enter your email: ')

    cursor.execute(
        '''SELECT * FROM users WHERE CIN = ?''',
        (cin,)
    )

    result = cursor.fetchone()


    if result is None:
        print("we sent u an email to verify that it is u")
        print("pls enter the 6 numbers code we sent ps check ur spam if it didnt appear")
        ver=sendmail(mail)
        ans = int(input())
        if ans==ver :
            cursor.execute(
                '''INSERT INTO users (CIN, name, lastname, password,email)
                   VALUES (?, ?, ?, ?,?)''',
                (cin, name, surname, pswd,mail)
            )
            connection.commit()

            print("User created successfully!")
        else :
            print("wrong code pls try again ")
            print("press 1 to retry and 2 to change ur information")
            answer=int(input("enter your choice"))
            while True :
                if answer==1:
                    oo=sendmail(mail)
                    answer = int(input("pls enter the 6 numbers code we sent ps check ur spam if it didnt appear"))

                    if oo==answer:
                        cursor.execute(
                            '''INSERT INTO users (CIN, name, lastname, password, email)
                               VALUES (?, ?, ?, ?, ?)''',
                            (cin, name, surname, pswd, mail)
                        )
                        connection.commit()

                        print("User created successfully!")
                    else :
                        print("wrong code pls try again ")
                        print("press 1 to retry and 2 to change ur information")
                        answer = int(input("enter your choice"))
                elif answer==2:
                    createuser()
                    break
                else :
                    print("press 1 to retry and 2 to change ur information")


    else:
        print("This user already exists!")
def login():
    cinMail = input('Enter your CIN or mail')
    print("did u forget ur password \n 1-yes \n 2-no")
    bo=int(input())
    while bo not in [1,2]:
        print("wrong choice")
        bo = int(input("enter your choice"))
    if bo == 2:
        pswd = input('Enter your password: ')
        if cinMail.find("@") == -1:
            if not cinMail.isdigit():                      # FIX: letters crashed int()
                print("CIN must be numbers only")
                return
            cinMail = int(cinMail)
            cursor.execute(
                """SELECT * FROM users WHERE CIN = ?""",
                (cinMail,)
            )

            result = cursor.fetchone()

            if result is None:
                print("The user does not exist!")
            else:
                mail = result[4]
                if not banbot.isbanned(mail):
                    stored_password = result[3]

                    if bcrypt.checkpw(
                        pswd.encode("utf-8"),
                        stored_password
                    ):
                        manage(cinMail)
                    else:
                        print("Password not matched!")
                else:
                    print("user banned")
        else:
            if not banbot.isbanned(cinMail):               # FIX: added "not"
                cursor.execute("""select cin from users where email = ?""", (cinMail,))
                cin = cursor.fetchone()
                if cin is None:
                    print("The user does not exist!")
                    print("press 1 to go back to menu or 2 to try again")
                    pol = int(input("enter your choice"))
                    while pol not in [1, 2]:
                        print("wrong choice")
                        pol = int(input("enter your choice"))
                    if pol == 1:
                        return
                    else:
                        login()
                        return
                else:
                    cin = cin[0]
                cursor.execute(
                    """SELECT *
                       FROM users
                       WHERE email = ?""",
                    (cinMail,)
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
            else:
                print("user banned")
                print("press 1 to go back")
                ans = int(input("enter your choice"))
                while ans != 1:
                    ans = int(input("enter your choice"))
                return
    else :
        reset()

def reset():
    mail=input("Enter your mail: ")
    cursor.execute("select * from users where email = ?",(mail,))
    result = cursor.fetchone()
    if result is None:
        print("The mail does not exist!")
    else :
        verif=sendmail(mail)
        print("write bellow ur verification code")
        ans=int(input("enter your choice"))
        for i in range(5):
            if ans==verif :
                print("pls enter your new password ")
                password = input("enter your new password ")
                password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))
                cursor.execute("""update users
                                  set password = ?
                                  where email = ?""", (password, mail))
                connection.commit()
                print("password updated successfully!")
                print("press 1 to go back to main menu")
                iop = int(input())
                while iop != 1:
                    print("press 1 to go back to main menu")
                    iop = int(input())
                break
            else :
                print("code doesnt match")
                print("press 1 to resend code or 2 to return to login")
                answ = int(input("enter your choice"))
                while answ not in [1,2]:
                    answ = int(input("enter your choice"))
                if answ == 1:
                    verif = sendmail(mail)
                    ans = int(input("enter the new verification code"))

                elif answ == 2:
                    login()
                    return
        if i==4:
            banbot.ban(mail)
        else :
            login()
import os  # at the top of main.py

def sendmail(reciever):
    sender = "expenesestracker@gmail.com"      # check this spelling!
    password = os.environ.get("MAIL_PASSWORD")
    verif = randint(100000, 999999)

    if password is None:
        print("MAIL_PASSWORD is not set")
        return None

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        message = "Subject: Verification code\n\nYour verification code is " + str(verif)
        server.sendmail(sender, reciever, message)
        server.quit()
    except smtplib.SMTPException as e:
        print("Could not send the email:", e)
        return None

    return verif
#programme principale
while True:
    print("Welcome to the application!")
    print("press 1 to create a new user or press 2 to login or press 3 to reset ur account and 4 to exit the application")

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
        reset()
    elif choice == 4:
        exit()
    else:
        print("invalid choice, please try again")