from flask import Flask, render_template, request, redirect
from db import get_connection

# Módulos del sistema
from dao.habitacion_dao import HabitacionDAO
from models.habitacion import Habitacion

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_connection()
    if conn:
        mensaje = "Conexión a la base de datos exitosa 🎉"
        conn.close()
    else:
        mensaje = "Error de conexión 😢"
    return render_template('index.html', mensaje=mensaje)

@app.route('/habitaciones')
def listar_habitaciones():
    habitaciones = HabitacionDAO.obtener_todas()
    return render_template('habitaciones.html', habitaciones=habitaciones)

@app.route('/habitaciones/crear', methods=['GET', 'POST'])
def crear_habitacion():
    if request.method == 'POST':
        numero = request.form['numero']
        categoria = request.form['categoria']
        capacidad = int(request.form['capacidad'])
        precio = float(request.form['precio'])
        estado = request.form['estado']
        habitacion = Habitacion(None, numero, categoria, capacidad, precio, estado)
        HabitacionDAO.insertar(habitacion)
        return redirect('/habitaciones')
    return render_template('crear_habitacion.html')
@app.route('/habitaciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_habitacion(id):
    habitacion = HabitacionDAO.obtener_por_id(id)
    if request.method == 'POST':
        habitacion.numero = request.form['numero']
        habitacion.categoria = request.form['categoria']
        habitacion.capacidad = int(request.form['capacidad'])
        habitacion.precio_por_noche = float(request.form['precio'])
        habitacion.estado = request.form['estado']
        HabitacionDAO.actualizar(habitacion)
        return redirect('/habitaciones')
    return render_template('editar_habitacion.html', habitacion=habitacion)

@app.route('/habitaciones/eliminar/<int:id>')
def eliminar_habitacion(id):
    HabitacionDAO.eliminar(id)
    return redirect('/habitaciones')


if __name__ == '__main__':
    app.run(debug=True)