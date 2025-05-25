from flask import Flask, render_template
from db import get_connection

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

if __name__ == '__main__':
    app.run(debug=True)

