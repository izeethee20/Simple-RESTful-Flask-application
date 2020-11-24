import sqlite3
from flask import Flask, render_template, json, request

app = Flask(__name__)


@app.route('/')
def start_page():
    return render_template('startPage.html')


@app.route('/choose', methods=['POST', 'GET'])
def choose():
    if request.method == 'POST':
        first = request.form['st']
        second = request.form['nd'] or ' '
        third = request.form['rd'] or ' '

        res = []
        j = []
        conn = sqlite3.connect('randomusers.db')
        sql = conn.cursor()
        sql.execute("SELECT data FROM result")
        data_file = sql.fetchall()
        for i in range(len(data_file)):
            j.append(i)
            item = json.loads(str(data_file[i][0]))
            if first in item:
                r1 = first, '--->', item[first]
                res.append(r1)
            else:
                raise Exception('Unfortunately, fill in the first field')
            if first in item and second in item[first]:
                r2 = second, '--->', item[first][second]
                res.append(r2)
            else:
                r2 = 'Sorry, you didn`t enter anything in the second field or you entered it incorrectly'
            if first in item and second in item[first] and third in item[first][second]:
                r3 = third, '--->', item[first][second][third]
                res.append(r3)
            else:
                r3 = 'Sorry, you didn`t enter anything in the third field or you entered it incorrectly'

        conn.commit()
        conn.close()

        return render_template("selectEn.html", r1=r1, r2=r2, r3=r3, res=res, items=data_file, j=j)


@app.route('/view_all', methods=['GET', 'POST'])
def view_all():
    conn = sqlite3.connect('randomusers.db')
    cursor = conn.execute('SELECT * FROM result')
    items = cursor.fetchall()
    j = []
    for i in range(len(items)):
        j.append(i)
    return render_template('viewAll.html', items=items, j=j)


@app.route('/delete_one', methods=['GET', 'POST'])
def delete_one():
    if request.method == 'POST':
        first = request.form['st']
        second = request.form['nd'] or ' '
        third = request.form['rd'] or ' '
        n = request.form['n']
        nameOfEntity = request.form['noe']
        r4 = ''
        res = []
        j = []
        conn = sqlite3.connect('randomusers.db')
        sql = conn.cursor()
        sql.execute("SELECT data FROM result")
        items = sql.fetchall()
        for i in range(len(items)):
            j.append(i)
            item = json.loads(str(items[i][0]))
            if first in item and n == '1' and first == nameOfEntity:
                r1 = item
                r1.pop(first)
                res.append(r1)
                r1 = 'You have deleted an entity of the first gradation:', first
            else:
                r1 = "('You haven`t deleted an entity of the first gradation')"
            if first in item and second in item[first] and n == '2' and second == nameOfEntity:
                r2 = item
                r2[first].pop(second)
                res.append(r2)
                r2 = 'You have deleted an entity of the second gradation:', second
            else:
                r2 = "('You haven`t deleted an entity of the second gradation')"
            if first in item and second in item[first] and third in item[first][second] and n == '3' and third == nameOfEntity:
                r3 = item
                r3[first][second].pop(third)
                res.append(r3)
                r3 = 'You have deleted an entity of the third gradation:', third
            else:
                r3 = "('You haven`t deleted an entity of the third gradation')"
        if not res:
            res.append(item)
            j = [0]
            r4 = "('You haven`t deleted anything, let`s go to try again')"
        conn.commit()
        conn.close()
    return render_template('deleteEn.html', r1=r1, r2=r2, r3=r3, r4=r4, res=res, items=items, j=j)


if __name__ == '__main__':
    app.run(debug=True)
