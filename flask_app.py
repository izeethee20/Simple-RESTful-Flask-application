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

        conn = sqlite3.connect('randomusers.db')
        sql = conn.cursor()
        sql.execute("SELECT data FROM result")
        data_file = sql.fetchall()
        for i in range(len(data_file)):
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

        return render_template("result.html", r1=r1, r2=r2, r3=r3, res=res, items=data_file)


@app.route('/view_all', methods=['GET', 'POST'])
def view_all():
    conn = sqlite3.connect('randomusers.db')
    cursor = conn.execute('SELECT * FROM result')
    items = cursor.fetchall()
    j = []
    for i in range(len(items)):
        j.append(i)
    return render_template('viewAll.html', items=items, i=j)


@app.route('/delete_one', methods=['GET', 'POST'])
def delete_one():
    return render_template('delete_one.html')


if __name__ == '__main__':
    app.run(debug=True)
