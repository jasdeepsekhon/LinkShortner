from flask import Flask, render_template, request, redirect, flash, url_for
import psycopg2

from flask import Flask, render_template, request, url_for, redirect

import random
import secrets

app = Flask(__name__, static_url_path="/static", static_folder='static')


def randid(length):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    id = ""
    range2 = len(chars)

    for i in range(length):
        x = secrets.randbelow(range2)
        id += chars[x]
    return id


def get_db_connection():
    conn = psycopg2.connect(database="jasdeepsekhon",
                            host="localhost",
                            user="jasdeepsekhon",
                            password="Jasdeep506",
                            port="5400")
    return conn


conn = get_db_connection()
cursor = conn.cursor()


cursor.execute('INSERT INTO URLSHORT (id, original_url)'
               'VALUES (%s, %s)',
               (randid(10),
                   'test123123@test.com',
                )
               )

conn.commit()


@app.route('/', methods=['GET'])
def index():
    return render_template("url.html")


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        original_url = request.form['original_url']

        conn = get_db_connection()
        cursor = conn.cursor()
        print(original_url)

        randomid = randid(10)

        cursor.execute('INSERT INTO URLSHORT (id, original_url)'
                       'VALUES (%s, %s)',
                       (randomid,
                           original_url,
                        )
                       )
        conn.commit()

        url = f"{randomid}"

        conn.close()
        # return redirect(url_for('create'))
        return render_template('url.html', url=url)
    return render_template('url.html')


@app.route('/<id>', methods=['GET'])
def get_long_url(id):
    print(id + " redirect")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            'UPDATE URLSHORT SET clicks = clicks + 1 WHERE id = %s RETURNING ORIGINAL_URL', (id,))
        conn.commit()

        original_url = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return redirect(original_url)

    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/clicks/<id>', methods=['GET'])
def get_clicks(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT clicks FROM URLSHORT WHERE id = %s;", (id,))
        clicks = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return f"Total Clicks for URL with ID {id}: {clicks}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
