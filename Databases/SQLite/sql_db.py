import sqlite3

connection = sqlite3.connect("data.db") #creates a db in the current directory (lite=single file)

cursor = connection.cursor() #used to execure queries

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, "richard", "asda")
users = [
    (1, "richard", "asda"),
    (2, "ralf", "assada")
]

insert_query = "INSERT INTO users VALUES (?, ?, ?)"

#cursor.execute(insert_query,user) #query will be formatted with the data structure in user
cursor.executemany(insert_query,users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

connection.commit() #need to tell cursor to save by commit changes
connection.close() #also good to close connection
