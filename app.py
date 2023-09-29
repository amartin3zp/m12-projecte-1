from flask import Flask ,render_template ,g ,request, redirect, url_for
import sqlite3
import datetime

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

@app.route("/products/create", methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        datos       = request.form
        title       = datos.get('title')
        description = datos.get('description')
        price       = int(datos.get('price'))
        foto        = 'hola'
        created     = datetime.datetime.now()
        updated     = datetime.datetime.now()
        
        with get_db() as conn:
            sql = "INSERT INTO products (title, description, photo, price, created, updated) VALUES (?, ?, ?, ?, ?, ?)"
            # app.logger.info('SQL: %s', sql)
            conn.execute(sql, (title, description, foto, price, created, updated))
        return redirect(url_for('list'))
    else:
        return render_template('products/create.html')
    
@app.route("/products/read/<int:id>")
def read(id):
    app.logger.debug("INT" if (type(id) is int) else "OTHER")
    with get_db() as conn:
        sql = "SELECT * FROM products WHERE id = " + str(id)
        resultat = conn.execute(sql)
        items = resultat.fetchall()
    return render_template("products/list.html",items = items)


# @app.route("/products/update/<int:id>")
# def read(id):
#      with get_db() as conn:
#         sql = "UPDATE * FROM products WHERE id=?"
#         conn.execute(sql, (id))