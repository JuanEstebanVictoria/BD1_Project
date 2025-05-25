from functools import wraps
from flask import session, redirect, url_for

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorador

def rol_requerido(rol_permitido):
    def decorador_externo(f):
        @wraps(f)
        def decorador(*args, **kwargs):
            if 'rol' not in session or session['rol'] != rol_permitido:
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorador
    return decorador_externo
