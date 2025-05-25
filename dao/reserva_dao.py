from db import get_connection
from models.reserva import Reserva

class ReservaDAO:
    @staticmethod
    def obtener_todas():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reserva")
        reservas = []
        for row in cursor.fetchall():
            reservas.append(Reserva(row.id, row.huesped_id, row.habitacion_id, row.fecha_entrada, row.fecha_salida, row.estado, row.check_in, row.check_out))
        conn.close()
        return reservas

    @staticmethod
    def insertar(reserva):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Reserva (huesped_id, habitacion_id, fecha_entrada, fecha_salida, estado)
            VALUES (?, ?, ?, ?, ?)
        """, (reserva.huesped_id, reserva.habitacion_id, reserva.fecha_entrada, reserva.fecha_salida, reserva.estado))
        conn.commit()
        conn.close()
    @staticmethod
    def obtener_por_id(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reserva WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Reserva(row.id, row.huesped_id, row.habitacion_id, row.fecha_entrada, row.fecha_salida, row.estado)
        return None

    @staticmethod
    def actualizar(reserva):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Reserva
            SET nombre_huesped = ?, habitacion_id = ?, fecha_entrada = ?, fecha_salida = ?, estado = ?
            WHERE id = ?
        """, (reserva.huesped_id, reserva.habitacion_id, reserva.fecha_entrada, reserva.fecha_salida, reserva.estado, reserva.id))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Reserva WHERE id = ?", (id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def obtener_por_huesped(huesped_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, h.nombre AS nombre_huesped, r.habitacion_id, r.fecha_entrada, r.fecha_salida, r.estado
            FROM Reserva r
            JOIN Huesped h ON r.huesped_id = h.id
            WHERE r.huesped_id = ?
        """, (huesped_id,))
        reservas = []
        for row in cursor.fetchall():
            reservas.append(Reserva(row.id, row.nombre_huesped, row.habitacion_id, row.fecha_entrada, row.fecha_salida, row.estado))
        conn.close()
        return reservas

    
