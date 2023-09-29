from flask import Flask ,render_template ,g ,request, redirect, url_for
import sqlite3, datetime, os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
DATABASE = 'database.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        datos           = request.form
        title           = datos.get('title')
        description     = datos.get('description')
        price           = int(datos.get('price'))
        fotoBD          = request.files['photo'].filename
        archivo         = request.files['photo']
        created         = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated         = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")         
        filename        = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        with get_db() as conn:
            sql = "INSERT INTO products (title, description, photo, price, created, updated) VALUES (?, ?, ?, ?, ?, ?)"
            # app.logger.info('SQL: %s', sql)
            conn.execute(sql, (title, description, fotoBD, price, created, updated))
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


@app.route("/products/update/<int:id>", methods = ['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        with get_db() as conn:
            results = conn.execute("SELECT * FROM products WHERE id = " + str(id))
            items = results.fetchall()
        return render_template('products/update.html', items = items)
    
    elif request.method == 'POST':
        with get_db() as conn:
            datos           = request.form
            description     = datos.get('description')
            title           = datos.get('title')
            price           = int(datos.get('price'))
            foto            = 'hola'
            updated         = datetime.datetime.now()
            conn.execute("UPDATE products SET title = ?, description = ?, photo = ?, price = ?, updated = ? WHERE id = ?", 
                (title, description, foto, price, updated, id))
        return redirect(url_for('list'))

        