from flask import Flask ,render_template ,g ,request
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'


def get_db():
    # sqlite3_database_path = DATABASE
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route("/list")
def list():
    with get_db() as conn:
        results = conn.execute("SELECT * FROM products ORDER BY id ASC")
        items = results.fetchall()
    return render_template("products/list.html",items = items)
