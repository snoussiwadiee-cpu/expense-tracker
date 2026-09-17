import sqlite3
def connect():
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()
    return connection, cursor