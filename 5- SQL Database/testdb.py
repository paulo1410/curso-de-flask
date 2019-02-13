import sqlite3

con = sqlite3.connect('data.db')
cursor = con.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'jose', 'asdf')

insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query, user)

users = [
    (2, 'rolf', 'xasdf'),
    (3, 'anne', 'xyz')
]
cursor.executemany(insert_query, users)  # users tem ser na forma de tupla

select_query = 'SELECT * FROM users'
for row in cursor.execute(select_query):
    print(row)

con.commit()
con.close()
