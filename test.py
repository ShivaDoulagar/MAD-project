import sqlite3

db = sqlite3.connect('project.db')
users = db.execute('SELECT * FROM users WHERE mail =?  AND password =?',('shiva@gmail.com','shiva123')).fetchone()
users = list(users)
print(users)