import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
#Create user table
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)" #INTEGER PRIMARY KEY gives auto-incrementing id
cursor.execute(create_table)
#Create item table
create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)" #INTEGER PRIMARY KEY gives auto-incrementing id
cursor.execute(create_table)
#testdata = "INSERT INTO items VALUES ('test', 10.9)"
#cursor.execute(testdata)
connection.commit()
connection.close()
