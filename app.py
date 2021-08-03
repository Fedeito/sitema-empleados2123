from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema2123'
mysql.init_app(app)

@app.route('/')
def index():
    sql    = "SELECT * FROM `empleados`;"
    conn   = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    empleados = cursor.fetchall()
    #print(empleados)

    return render_template('empleados/index.html', empleados=empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))
    conn.commit()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    conn.commit()

    empleados = cursor.fetchall()

    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto   = request.files['txtFoto']
    _id     = request.form['txtId']

    sql   = "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;"
    datos = (_nombre, _correo, _id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

# EJEMPLO HARDCODEADO
# @app.route('/')
# def index():
#     sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'messi', 'messi@ciudad.com.ar', 'messi.jpg'); "
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     return render_template('empleados/index.html')

# EJEMPLO AUTOMATIZADO
@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto   = request.files['txtFoto']

    now    = datetime.now()
    tiempo = now.strftime("%Y%H%M%S") # now.stringformattime("%YEAR%HOUR%MINUTE%SECOND")

    if _foto.filename !='':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql   = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s); "
    datos = (_nombre, _correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    # mysql.connect().cursor().execute(sql, datos)
    # mysql.connect().commit()

    return render_template('empleados/index.html')

if __name__=='__main__':
    app.run(debug=True)
