import sqlite3
import requests
import json

y = 0

while y < 5:
    res = requests.get('https://randomuser.me/api?gender=male&format=json')
    if 'gender' in res.text:
        y = y + 1
        data_file = res.json()
        print(data_file, '\n')
        # with open('data.json', 'w') as file:
        #     json.dump(data_file, file)
        conn = sqlite3.connect('randomusers.db')
        c = conn.cursor()
        c.execute("insert into result (data) values (?)", [json.dumps(res.json())])
        conn.commit()
        conn.close()
