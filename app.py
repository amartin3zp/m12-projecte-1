from flask import Flask ,render_template ,g
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route("/products")
def hello_world():
    return render_template('hello.html')

DATABASE = '/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db