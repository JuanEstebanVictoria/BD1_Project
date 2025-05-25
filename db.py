import pyodbc

def get_connection():
    try:
        connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-87HFKPA;"  # Cambia si tu instancia es diferente
            "DATABASE=ProyectoBD;"        # Reemplaza con tu base de datos
            "Trusted_Connection=yes;"        # O usa UID y PWD si no usas autenticación de Windows
        )
        return connection
    except Exception as e:
        print("Error en la conexión:", e)
        return None
