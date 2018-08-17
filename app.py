import sqlite3
import short_url
from flask import Flask, render_template, request, g, redirect

sqllite_db = 'urls.db'

app = Flask(__name__)

host = 'http://localhost:5000/'


@app.route('/<string:url>')
def get_some_magic(url):
    url_id = short_url.decode_url(url)
    return redirect(get_url_by_id(url_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        full_url = request.form.get('url')
        url_id = insert_url(full_url)
        url = short_url.encode_url(url_id)
        return render_template('get_some_magic.html', full_url=full_url, short_url=request.base_url + url)
    if request.method == 'GET':
        return render_template('get_some_magic.html')


def get_conn():
    if not hasattr(g, 'cur'):
        g.conn = sqlite3.connect(sqllite_db)
        g.cur = g.conn.cursor()
    return g.conn, g.cur


def insert_url(full_url):
    insert_query = 'insert into urls (full_url) values ("%s")' % full_url
    conn, cur = get_conn()
    last_cur = cur.execute(insert_query)
    conn.commit()
    return last_cur.lastrowid


def get_url_by_id(id):
    select_query = 'select full_url from urls where id = %d' % id
    conn, cur = get_conn()
    return cur.execute(select_query).fetchone()[0]


def create_all():
    conn = sqlite3.connect(sqllite_db)
    cur = conn.cursor()
    create_query = """create table IF NOT EXISTS urls (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                                FULL_URL TEXT NOT NULL )"""
    cur.execute(create_query)


create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
