from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'agenda'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()

@app.route('/usuarios')
def ver_usuarios():
    cursor.execute("SELECT * from usuarios")
    data = cursor.fetchall()
    return render_template('usuarios.html', usuarios = data )

@app.route('/contactos')
def ver_contactos():
    cursor.execute("SELECT usu_nombre, con_nombre, con_apellido, con_direccion, con_telefono, con_email " +
                    "FROM usuarios as usu " + 
                    "INNER JOIN contactos as con on (usu.usu_id = con.usu_id) ")
    data = cursor.fetchall()
    return render_template('contactos.html', contactos = data )

@app.route('/citas')
def ver_citas():
    cursor.execute("SELECT usu_nombre, con_nombre, con_apellido, con_telefono, cit_lugar, cit_fecha, cit_hora, cit_descripcion " +
                    "FROM usuarios as usu " + 
                    "LEFT JOIN contactos as con on (usu.usu_id = con.usu_id) " +
                    "LEFT JOIN citas as cit on (con.con_id = cit.con_id)")
    data = cursor.fetchall()
    return render_template('citas.html', citas = data )

@app.route('/todos')
def ver_todos():
    cursor.execute("SELECT usu_nombre, con_nombre, con_apellido, con_telefono, cit_lugar, cit_fecha " +
                    "FROM usuarios as usu " + 
                    "LEFT JOIN contactos as con on (usu.usu_id = con.usu_id) " +
                    "LEFT JOIN citas as cit on (con.con_id = cit.con_id)")
    data = cursor.fetchall()
    return render_template('todos.html', citas = data )

@app.route("/agregar_usuario", methods = ['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form["nombre"]
        clave = request.form["clave"]
        cursor.execute("""INSERT INTO `usuarios`(`usu_nombre`, `usu_clave`) VALUES (%s, sha1(%s));""", (nombre, clave)) 
        conn.commit()
        return redirect(url_for('ver_usuarios'))
    else:
        return render_template('agregar_usuario.html')

@app.route('/actualizar_usuario', methods=['GET', 'POST'])
def actualizar_usuario():
    if request.method == 'POST':
        id = request.form["id"]
        nombre = request.form["nombre"]
        clave = request.form["clave"]
        cursor.execute("""UPDATE `usuarios` SET `usu_nombre`=%s,`usu_clave`=sha1(%s) WHERE `usu_id`= %s""", (nombre, clave, id)) 
        conn.commit()
        return redirect(url_for('ver_usuarios'))
    else:
        id = request.args["id"]
        cursor.execute("SELECT usu_id, usu_nombre from usuarios where usu_id = " + id)
        usuario = cursor.fetchone()
        return render_template('editar_usuario.html', usuario=usuario)
        

@app.route('/eliminar_usuario', methods=['GET'])
def eliminar_usuario():
    if request.method == 'GET':
        id = request.args["id"]
        cursor.execute("DELETE from usuarios where usu_id = " + id)
        conn.commit()
        return redirect(url_for('ver_usuarios'))

@app.route("/agregar_contacto", methods = ['GET', 'POST'])
def agregar_contacto():
    if request.method == 'POST':
        id_cont = request.form["id_cont"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        cursor.execute("""INSERT INTO `contactos` (`usu_id`, `con_nombre`, `con_apellido`, `con_direccion`, `con_telefono`, `con_email`) VALUES (%s, %s, %s, %s, %s, %s);""", (id_cont, nombre, apellido, direccion, telefono, email))
        conn.commit()
        return redirect(url_for('ver_contactos'))
    else:
        return render_template('agregar_contacto.html')

@app.route('/actualizar_contacto', methods=['GET', 'POST'])
def actualizar_contacto():
    if request.method == 'POST':
        id = request.form["id"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        cursor.execute("""UPDATE `contactos` SET `con_nombre` =%s, `con_apellido` =%s, `con_direccion` =%s, `con_telefono` =%s, `con_email` =%s WHERE `contactos`.`con_id` =%s""", (nombre, apellido, direccion, telefono, email, id))
        conn.commit()
        return redirect(url_for('ver_contactos'))
    else:
        id = request.args["id"]
        cursor.execute("SELECT con_id, con_nombre, con_apellido, con_direccion, con_telefono, con_email from contactos where con_id = " + id)
        contacto = cursor.fetchone()
        return render_template('editar_contacto.html', contacto=contacto)    

@app.route('/eliminar_contacto')
def eliminar_contacto():
    if request.method == 'GET':
        id = request.args["id"]
        cursor.execute("DELETE from `contactos` where con_id = " + id)
        conn.commit()
        return redirect(url_for('ver_contactos'))

@app.route("/agregar_cita", methods = ['GET', 'POST'])
def agregar_cita():
    if request.method == 'POST':
        id_cita = request.form["id_cita"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        telefono = request.form["telefono"]
        lugar = request.form["lugar"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        descripcion = request.form["descripcion"]
        cursor.execute("""INSERT INTO `citas` (`con_id`, `con_nombre`, `con_apellido`, `con_telefono`, `cit_lugar`, `cit_fecha`, `cit_hora`, `cit_descripcion`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
        (id_cita, nombre, apellido, telefono, lugar, fecha, hora, descripcion))
        conn.commit()
        return redirect(url_for('ver_citas'))
    else:
        return render_template('agregar_cita.html')

@app.route('/actualizar_cita', methods=['GET', 'POST'])
def actualizar_cita():
    if request.method == 'POST':
        id = request.form["id"]
        nombre = request.form["nombre"]
        clave = request.form["clave"]
        cursor.execute("""UPDATE `usuarios` SET `usu_nombre`=%s,`usu_clave`=sha1(%s) WHERE `usu_id`= %s""", (nombre, clave, id)) 
        conn.commit()
        return redirect(url_for('ver_citas'))
    else:
        id = request.args["id"]
        cursor.execute("SELECT usu_id, usu_nombre from citas where cit_id = " + id)
        usuario = cursor.fetchone()
        return render_template('editar_cita.html', usuario=usuario)

@app.route('/eliminar_cita')
def eliminar_cita():
    if request.method == 'GET':
        id = request.args["id"]
        #"DELETE FROM `citas` WHERE `citas`.`cit_id` = 12"
        cursor.execute("DELETE from citas where citas.cit_id = " + id)
        conn.commit()
        return redirect(url_for('ver_citas'))
        


if __name__ == '__main__':
    app.run(debug=True)
