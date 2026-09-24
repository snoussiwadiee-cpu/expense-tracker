from db import connect
import os
import bcrypt
from menu import *
import smtplib
import secrets
import banbot

connection, cursor = connect()


def createuser():
    cin = input("Enter your CIN number: ")

    # Validate CIN before converting it to an integer
    if not cin.isdigit():
        print("CIN must contain numbers only!")
        return

    cin = int(cin)

    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    pswd = input("Enter your password: ")

    # Hash password before storing it
    pswd = bcrypt.hashpw(
        pswd.encode("utf-8"),
        bcrypt.gensalt(12)
    )

    mail = input("Enter your email: ")

    cursor.execute(
        """SELECT * FROM users WHERE CIN = ?""",
        (cin,)
    )

    result = cursor.fetchone()

    if result is not None:
        print("This user already exists!")
        return

    print("We sent you an email to verify that it is you.")
    print("Please enter the 6 numbers code we sent. Check your spam if it didn't appear.")

    ver = sendmail(mail)

    if ver is None:
        print("Verification email could not be sent.")
        return

    while True:

        try:
            ans = int(input("Enter the verification code: "))
        except ValueError:
            print("The code must contain numbers only.")
            continue

        if ans == ver:
            cursor.execute(
                """INSERT INTO users
                   (CIN, name, lastname, password, email)
                   VALUES (?, ?, ?, ?, ?)""",
                (cin, name, surname, pswd, mail)
            )

            connection.commit()

            print("User created successfully!")
            return

        print("Wrong code. Please try again.")
        print("1 - Resend code")
        print("2 - Change your information")
        print("3 - Cancel")

        answer = input("Enter your choice: ")

        while answer not in ["1", "2", "3"]:
            print("Wrong choice.")
            answer = input("Enter your choice: ")

        if answer == "1":
            ver = sendmail(mail)

            if ver is None:
                print("Verification email could not be sent.")
                return

        elif answer == "2":
            createuser()
            return

        else:
            return


def login():
    cinMail = input("Enter your CIN or mail: ")

    print("Did you forget your password?")
    print("1 - Yes")
    print("2 - No")

    bo = input("Enter your choice: ")

    while bo not in ["1", "2"]:
        print("Wrong choice.")
        bo = input("Enter your choice: ")

    # Password reset
    if bo == "1":
        reset()
        return

    pswd = input("Enter your password: ")

    # =========================================================
    # LOGIN WITH CIN
    # =========================================================

    if "@" not in cinMail:

        if not cinMail.isdigit():
            print("CIN must contain numbers only.")
            return

        cinMail = int(cinMail)

        cursor.execute(
            """SELECT * FROM users WHERE CIN = ?""",
            (cinMail,)
        )

        result = cursor.fetchone()

        if result is None:
            print("The user does not exist!")
            return

        # Based on your database structure:
        # result[3] = password
        # result[4] = email

        stored_password = result[3]
        mail = result[4]

        if banbot.isbanned(mail):
            print("User banned.")
            return

        if bcrypt.checkpw(
            pswd.encode("utf-8"),
            stored_password
        ):
            print("Login successful!")
            manage(cinMail)
            return
        else:
            print("Password not matched!")
            return

    # =========================================================
    # LOGIN WITH EMAIL
    # =========================================================

    else:

        cursor.execute(
            """SELECT * FROM users WHERE email = ?""",
            (cinMail,)
        )

        result = cursor.fetchone()

        if result is None:
            print("The user does not exist!")
            return

        # Based on your database structure:
        # result[0] = CIN
        # result[3] = password
        # result[4] = email

        cin = result[0]
        stored_password = result[3]
        mail = result[4]

        if banbot.isbanned(mail):
            print("User banned.")
            return

        if bcrypt.checkpw(
            pswd.encode("utf-8"),
            stored_password
        ):
            print("Login successful!")
            manage(cin)
            return
        else:
            print("Password not matched!")
            return


def reset():
    mail = input("Enter your mail: ")

    cursor.execute(
        """SELECT * FROM users WHERE email = ?""",
        (mail,)
    )

    result = cursor.fetchone()

    if result is None:
        print("The mail does not exist!")
        return

    verif = sendmail(mail)

    if verif is None:
        print("We could not send the verification code.")
        return

    print("We sent you a verification code to your email.")

    for attempt in range(5):

        try:
            ans = int(input("Enter the verification code: "))
        except ValueError:
            print("The code must contain numbers only.")
            continue

        if ans == verif:

            print("Please enter your new password.")

            password = input("Enter your new password: ")

            password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt(12)
            )

            cursor.execute(
                """UPDATE users
                   SET password = ?
                   WHERE email = ?""",
                (password, mail)
            )

            connection.commit()
    
            print("Password updated successfully!")
            return

        print("Code doesn't match.")

        # Don't offer options after the final attempt
        if attempt < 4:
            print("1 - Resend code")
            print("2 - Return to login")

            answ = input("Enter your choice: ")

            while answ not in ["1", "2"]:
                print("Wrong choice.")
                answ = input("Enter your choice: ")

            if answ == "1":
                verif = sendmail(mail)

                if verif is None:
                    print("Could not resend the verification code.")
                    return

            else:
                return

    # All 5 attempts failed
    print("Too many incorrect attempts.")
    banbot.ban(mail)


def sendmail(reciever):
    sender = "expenesestracker@gmail.com"
    password = os.environ.get("MAIL_PASSWORD")

    # Generate a 6-digit security code
    verif = secrets.randbelow(900000) + 100000

    if password is None:
        print("MAIL_PASSWORD is not set")
        return None

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender, password)

        message = (
            "Subject: Verification code\n\n"
            "Your verification code is " + str(verif)
        )

        server.sendmail(
            sender,
            reciever,
            message
        )

        server.quit()

    except smtplib.SMTPException as e:
        print("Could not send the email:", e)
        return None

    return verif


# =============================================================
# MAIN PROGRAM
# =============================================================

while True:

    print("\n===== EXPENSE TRACKER =====")
    print("1 - Create a new user")
    print("2 - Login")
    print("3 - Reset your account")
    print("4 - Exit")

    choice = input("Enter your choice: ")

    if not choice.isdigit():
        print("Invalid choice, please try again.")
        continue

    choice = int(choice)

    if choice == 1:
        createuser()

    elif choice == 2:
        login()

    elif choice == 3:
        reset()

    elif choice == 4:
        print("Goodbye!")
        break

    else:
        print("Invalid choice, please try again.")