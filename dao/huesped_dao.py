from db import get_connection
from models.huesped import Huesped

class HuespedDAO:
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Huesped")
        huespedes = []
        for row in cursor.fetchall():
            huespedes.append(Huesped(row.id, row.nombre, row.documento, row.telefono, row.correo))
        conn.close()
        return huespedes

    @staticmethod
    def insertar(huesped):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Huesped (nombre, documento, telefono, correo)
            VALUES (?, ?, ?, ?)
        """, (huesped.nombre, huesped.documento, huesped.telefono, huesped.correo))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_por_id(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Huesped WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Huesped(row.id, row.nombre, row.documento, row.telefono, row.correo)
        return None

    @staticmethod
    def actualizar(huesped):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Huesped
            SET nombre = ?, documento = ?, telefono = ?, correo = ?
            WHERE id = ?
        """, (huesped.nombre, huesped.documento, huesped.telefono, huesped.correo, huesped.id))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Huesped WHERE id = ?", (id,))
        conn.commit()
        conn.close()
