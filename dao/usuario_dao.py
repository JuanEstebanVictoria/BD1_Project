from db import get_connection
from models.usuario import Usuario

class UsuarioDAO:
    @staticmethod
    def insertar(usuario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Usuario (nombre, username, password, rol)
            VALUES (?, ?, ?, ?)
        """, (usuario.nombre, usuario.username, usuario.password, usuario.rol))
        conn.commit()
        conn.close()

    @staticmethod
    def buscar_por_username(username):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(row.id, row.nombre, row.username, row.password, row.rol)
        return None

    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario")
        usuarios = []
        for row in cursor.fetchall():
            usuarios.append(Usuario(row.id, row.nombre, row.username, row.password, row.rol))
        conn.close()
        return usuarios
    
    @staticmethod
    def buscar_por_id(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(row.id, row.nombre, row.username, row.password, row.rol)
        return None

    @staticmethod
    def actualizar(usuario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Usuario SET nombre = ?, username = ?, password = ?, rol = ?
            WHERE id = ?
        """, (usuario.nombre, usuario.username, usuario.password, usuario.rol, usuario.id))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuario WHERE id = ?", (id,))
        conn.commit()
        conn.close()

