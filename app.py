from flask import Flask, render_template, request, redirect
from db import get_connection

# Módulos del sistema
from dao.habitacion_dao import HabitacionDAO
from models.habitacion import Habitacion
from dao.reserva_dao import ReservaDAO
from models.reserva import Reserva


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

@app.route('/reservas')
def listar_reservas():
    reservas = ReservaDAO.obtener_todas()
    return render_template('reservas.html', reservas=reservas)

@app.route('/reservas/crear', methods=['GET', 'POST'])
def crear_reserva():
    if request.method == 'POST':
        nombre_huesped = request.form['nombre_huesped']
        habitacion_id = int(request.form['habitacion_id'])
        fecha_entrada = request.form['fecha_entrada']
        fecha_salida = request.form['fecha_salida']
        estado = request.form['estado']
        reserva = Reserva(None, nombre_huesped, habitacion_id, fecha_entrada, fecha_salida, estado)
        ReservaDAO.insertar(reserva)
        return redirect('/reservas')
    
    # Obtener lista de habitaciones para mostrar en el formulario
    from dao.habitacion_dao import HabitacionDAO
    habitaciones = HabitacionDAO.obtener_todas()
    return render_template('crear_reserva.html', habitaciones=habitaciones)

@app.route('/reservas/editar/<int:id>', methods=['GET', 'POST'])
def editar_reserva(id):
    reserva = ReservaDAO.obtener_por_id(id)
    from dao.habitacion_dao import HabitacionDAO
    habitaciones = HabitacionDAO.obtener_todas()

    if request.method == 'POST':
        reserva.nombre_huesped = request.form['nombre_huesped']
        reserva.habitacion_id = int(request.form['habitacion_id'])
        reserva.fecha_entrada = request.form['fecha_entrada']
        reserva.fecha_salida = request.form['fecha_salida']
        reserva.estado = request.form['estado']
        ReservaDAO.actualizar(reserva)
        return redirect('/reservas')
    return render_template('editar_reserva.html', reserva=reserva, habitaciones=habitaciones)

@app.route('/reservas/eliminar/<int:id>')
def eliminar_reserva(id):
    ReservaDAO.eliminar(id)
    return redirect('/reservas')




if __name__ == '__main__':
    app.run(debug=True)