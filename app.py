from flask import Flask, render_template, request, redirect
from db import get_connection
from datetime import datetime
from flask import abort

# Módulos del sistema
from dao.habitacion_dao import HabitacionDAO
from models.habitacion import Habitacion
from dao.reserva_dao import ReservaDAO
from models.reserva import Reserva
from dao.huesped_dao import HuespedDAO
from models.huesped import Huesped
from flask import session, url_for
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario
from utils.decoradores import login_requerido, rol_requerido





app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

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
@login_requerido
@rol_requerido('admin')
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
@login_requerido
def listar_reservas():
    reservas = ReservaDAO.obtener_todas()
    return render_template('reservas.html', reservas=reservas)

@app.route('/reservas/crear', methods=['GET', 'POST'])
def crear_reserva():
    if request.method == 'POST':
        huesped_id = request.form['huesped_id']
        habitacion_id = int(request.form['habitacion_id'])
        fecha_entrada = request.form['fecha_entrada']
        fecha_salida = request.form['fecha_salida']
        estado = request.form['estado']
        reserva = Reserva(
        id=None,
        nombre_huesped="",  # este campo es solo para mostrar, no lo usamos en inserción
        habitacion_id=habitacion_id,
        fecha_entrada=fecha_entrada,
        fecha_salida=fecha_salida,
        estado=estado,
        huesped_id=int(huesped_id)  # 👈 esto es clave
        )
        ReservaDAO.insertar(reserva)
        return redirect('/reservas')
    
    # Obtener lista de habitaciones para mostrar en el formulario
    from dao.habitacion_dao import HabitacionDAO
    from dao.huesped_dao import HuespedDAO
    habitaciones = HabitacionDAO.obtener_todas()
    huespedes = HuespedDAO.obtener_todos()
    return render_template('crear_reserva.html', habitaciones=habitaciones, huespedes=huespedes)

@app.route('/reservas/editar/<int:id>', methods=['GET', 'POST'])
def editar_reserva(id):
    reserva = ReservaDAO.obtener_por_id(id)
    from dao.habitacion_dao import HabitacionDAO
    habitaciones = HabitacionDAO.obtener_todas()
    from dao.huesped_dao import HuespedDAO
    huespedes = HuespedDAO.obtener_todos()

    if request.method == 'POST':
        reserva.huesped_id = request.form['huesped_id']
        reserva.habitacion_id = int(request.form['habitacion_id'])
        reserva.fecha_entrada = request.form['fecha_entrada']
        reserva.fecha_salida = request.form['fecha_salida']
        reserva.estado = request.form['estado']
        ReservaDAO.actualizar(reserva)
        return redirect('/reservas')
    return render_template('editar_reserva.html', reserva=reserva, habitaciones=habitaciones, huespedes= huespedes)

@app.route('/reservas/eliminar/<int:id>')
def eliminar_reserva(id):
    ReservaDAO.eliminar(id)
    return redirect('/reservas')

@app.route('/reservas/checkin/<int:id>')
def checkin_reserva(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Reserva SET check_in = ?, estado = 'ocupada' WHERE id = ?", (datetime.now(), id))
    conn.commit()
    conn.close()
    return redirect('/reservas')

@app.route('/reservas/checkout/<int:id>')
def checkout_reserva(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Reserva SET check_out = ?, estado = 'finalizada' WHERE id = ?", (datetime.now(), id))
    conn.commit()
    conn.close()
    return redirect('/reservas')

@app.route('/reservas/<int:id>/factura')
def factura_reserva(id):
    reserva = ReservaDAO.obtener_por_id(id)
    if not reserva:
        abort(404)

    # Obtener datos de habitación y huésped
    from dao.habitacion_dao import HabitacionDAO
    from dao.huesped_dao import HuespedDAO

    habitacion = HabitacionDAO.obtener_por_id(reserva.habitacion_id)
    huesped = HuespedDAO.obtener_por_id(reserva.huesped_id)

    # Calcular número de noches
    noches = (reserva.fecha_salida - reserva.fecha_entrada).days
    total = noches * habitacion.precio_por_noche

    return render_template('factura.html', reserva=reserva, habitacion=habitacion, huesped=huesped, noches=noches, total=total)

@app.route('/huespedes')
def listar_huespedes():
    huespedes = HuespedDAO.obtener_todos()
    return render_template('huespedes.html', huespedes=huespedes)

@app.route('/huespedes/crear', methods=['GET', 'POST'])
def crear_huesped():
    if request.method == 'POST':
        nombre = request.form['nombre']
        documento = request.form['documento']
        telefono = request.form['telefono']
        correo = request.form['correo']
        nuevo = Huesped(None, nombre, documento, telefono, correo)
        HuespedDAO.insertar(nuevo)
        return redirect('/huespedes')
    return render_template('crear_huesped.html')

@app.route('/huespedes/editar/<int:id>', methods=['GET', 'POST'])
def editar_huesped(id):
    huesped = HuespedDAO.obtener_por_id(id)
    if request.method == 'POST':
        huesped.nombre = request.form['nombre']
        huesped.documento = request.form['documento']
        huesped.telefono = request.form['telefono']
        huesped.correo = request.form['correo']
        HuespedDAO.actualizar(huesped)
        return redirect('/huespedes')
    return render_template('editar_huesped.html', huesped=huesped)

@app.route('/huespedes/eliminar/<int:id>')
def eliminar_huesped(id):
    HuespedDAO.eliminar(id)
    return redirect('/huespedes')

@app.route('/huespedes/<int:id>/reservas')
def reservas_por_huesped(id):
    reservas = ReservaDAO.obtener_por_huesped(id)
    return render_template('reservas_por_huesped.html', reservas=reservas)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']
        nuevo = Usuario(None, nombre, username, password, rol)
        UsuarioDAO.insertar(nuevo)
        return redirect('/login')
    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = UsuarioDAO.buscar_por_username(username)
        if usuario and usuario.password == password:
            session['usuario_id'] = usuario.id
            session['username'] = usuario.username
            session['rol'] = usuario.rol
            return redirect('/')
        else:
            return render_template('login.html', error='Credenciales inválidas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/usuarios')
@login_requerido
@rol_requerido('admin')
def listar_usuarios():
    usuarios = UsuarioDAO.obtener_todos()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
@login_requerido
@rol_requerido('admin')
def crear_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']
        nuevo = Usuario(None, nombre, username, password, rol)
        UsuarioDAO.insertar(nuevo)
        return redirect('/usuarios')
    return render_template('crear_usuario.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
@rol_requerido('admin')
def editar_usuario(id):
    usuario = UsuarioDAO.buscar_por_id(id)
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.username = request.form['username']
        usuario.password = request.form['password']
        usuario.rol = request.form['rol']
        UsuarioDAO.actualizar(usuario)
        return redirect('/usuarios')
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/usuarios/eliminar/<int:id>')
@login_requerido
@rol_requerido('admin')
def eliminar_usuario(id):
    UsuarioDAO.eliminar(id)
    return redirect('/usuarios')

if __name__ == '__main__':
    app.run(debug=True)