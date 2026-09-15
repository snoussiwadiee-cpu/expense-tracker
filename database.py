import sqlite3

connection = sqlite3.connect('expenses.db')
print("connected")

cursor = connection.cursor()
cursor.execute('''create table expenses (
        numexpe integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        amount INTEGER NOT NULL,
        idcat INTEGER NOT NULL,
        date date NOT NULL,
        description TEXT NOT NULL,
        foreign key(idcat) REFERENCES categories (idcat))''')
connection.commit()