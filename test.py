import sqlite3

db = sqlite3.connect('project.db')
users = db.execute('SELECT * FROM users WHERE mail = ?',('shva@gmail.com',)).fetchone()

print(users)