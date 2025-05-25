from db import get_connection
from models.habitacion import Habitacion

class HabitacionDAO:
    @staticmethod
    def obtener_todas():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Habitacion")
        habitaciones = []
        for row in cursor.fetchall():
            habitaciones.append(Habitacion(row.id, row.numero, row.categoria, row.capacidad, row.precio_por_noche, row.estado))
        conn.close()
        return habitaciones

    @staticmethod
    def insertar(habitacion):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Habitacion (numero, categoria, capacidad, precio_por_noche, estado)
            VALUES (?, ?, ?, ?, ?)
        """, (habitacion.numero, habitacion.categoria, habitacion.capacidad, habitacion.precio_por_noche, habitacion.estado))
        conn.commit()
        conn.close()
    @staticmethod
    def obtener_por_id(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Habitacion WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Habitacion(row.id, row.numero, row.categoria, row.capacidad, row.precio_por_noche, row.estado)
        return None

    @staticmethod
    def actualizar(habitacion):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Habitacion SET numero = ?, categoria = ?, capacidad = ?, precio_por_noche = ?, estado = ?
            WHERE id = ?
        """, (habitacion.numero, habitacion.categoria, habitacion.capacidad, habitacion.precio_por_noche, habitacion.estado, habitacion.id))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Habitacion WHERE id = ?", (id,))
        conn.commit()
        conn.close()
