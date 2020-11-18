import ast
import sqlite3
import requests
import json

y = 0

while y < 100:
    res = requests.get('https://randomuser.me/api?gender=male&format=json')
    if 'gender' in res.text:
        y = y + 1
        data_file = res.json()
        print(data_file)
        # item = data_file[list(data_file.keys())[1]]["results"]["location"]
        item = str(data_file[list(data_file.keys())[0]])
        item = item[1: -1]
        print(item)
        item = dict(ast.literal_eval(item))
        # with open('data.json', 'w') as file:
        #     json.dump(data_file, file)
        # print(item)
        conn = sqlite3.connect('randomusers.db')
        c = conn.cursor()
        c.execute("insert into result (data) values (?)", [json.dumps(item)])
        conn.commit()
        conn.close()


