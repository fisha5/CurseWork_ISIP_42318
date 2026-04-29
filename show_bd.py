import sqlite3

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

print(' ВРАЧИ ')
for row in c.execute('SELECT * FROM users'):
    print(dict(row))

print('\n ЗАПИСИ ')
for row in c.execute('SELECT * FROM appointments'):
    print(dict(row))

conn.close()