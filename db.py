import sqlite3


conn = sqlite3.connect('randomusers.db')
c = conn.cursor()
# c.execute("drop table result")
c.execute("create table result (data json)")
conn.commit()
conn.close()
