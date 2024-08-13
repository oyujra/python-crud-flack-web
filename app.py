from flask import Flask, request, redirect, url_for, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python'


mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM registros')
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', registros=data)

@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        estado = request.form['estado']
        id_ = request.form['id']
        matricula = request.form['matricula']
        razon_social = request.form['razon_social']
        cod_estado_actualizacion = request.form['cod_estado_actualizacion']
        cod_departamento = request.form['cod_departamento']
        id_establecimiento = request.form['id_establecimiento']
        direccion = request.form['direccion']
        respuesta_json = request.form['respuesta_json']
        
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO registros (estado, id, matricula, razon_social, cod_estado_actualizacion, 
                       cod_departamento, id_establecimiento, direccion, respuesta_json) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                       (estado, id_, matricula, razon_social, cod_estado_actualizacion, 
                        cod_departamento, id_establecimiento, direccion, respuesta_json))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))
    
    return render_template('add_record.html')

@app.route('/edit/<int:id_registro>', methods=['GET', 'POST'])
def edit_record(id_registro):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        estado = request.form['estado']
        id_ = request.form['id']
        matricula = request.form['matricula']
        razon_social = request.form['razon_social']
        cod_estado_actualizacion = request.form['cod_estado_actualizacion']
        cod_departamento = request.form['cod_departamento']
        id_establecimiento = request.form['id_establecimiento']
        direccion = request.form['direccion']
        respuesta_json = request.form['respuesta_json']

        cursor.execute('''UPDATE registros SET estado=%s, id=%s, matricula=%s, razon_social=%s, cod_estado_actualizacion=%s, 
                       cod_departamento=%s, id_establecimiento=%s, direccion=%s, respuesta_json=%s 
                       WHERE id_registro=%s''',
                       (estado, id_, matricula, razon_social, cod_estado_actualizacion, 
                        cod_departamento, id_establecimiento, direccion, respuesta_json, id_registro))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))

    # Obtener datos del registro a editar
    cursor.execute('SELECT * FROM registros WHERE id_registro = %s', (id_registro,))
    data = cursor.fetchone()
    cursor.close()
    return render_template('edit_record.html', registro=data)

@app.route('/delete/<int:id_registro>')
def delete_record(id_registro):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM registros WHERE id_registro = %s', (id_registro,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
