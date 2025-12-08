import web

def absolute_url(path: str) -> str:
    """Construye URL absoluta usando los encabezados del proxy para evitar duplicar puertos."""
    try:
        env = getattr(web.ctx, 'env', {}) or {}
        proto = env.get('HTTP_X_FORWARDED_PROTO') or env.get('wsgi.url_scheme') or 'http'
        host = env.get('HTTP_X_FORWARDED_HOST') or env.get('HTTP_HOST') or ''
        if not host:
            return path
        if path.startswith('http://') or path.startswith('https://'):
            return path
        if not path.startswith('/'):
            path = '/' + path
        return f"{proto}://{host}{path}"
    except Exception:
        return path

# Helpers de sesión para niño y tutor/admin

def set_nino_session(session, row):
    try:
        session.nino_id = row[0]
        session.nino_nombre = row[1]
        session.nino_apellidos = row[2]
        session.tutor_id = row[3]
        session.user_type = 'nino'
        session.nino_activo = True
        return True
    except Exception as e:
        print(f"[SESION] Error guardando información: {e}")
        return False


def limpiar_nino_session(session):
    try:
        had = bool(getattr(session, 'nino_activo', False) or getattr(session, 'nino_id', None))
        session.nino_activo = False
        for attr in ['nino_id', 'nino_nombre', 'nino_apellidos']:
            if hasattr(session, attr):
                setattr(session, attr, None)
        if getattr(session, 'user_type', None) == 'nino':
            session.user_type = None
        if hasattr(session.store, 'root'):
            try:
                session.kill()
            except Exception as e:
                print(f"[SESION] Error eliminando archivo de sesión: {e}")
        return had
    except Exception as e:
        print(f"[SESION] Error en limpiar_nino_session: {e}")
        return False


def limpiar_tutor_session(session):
    try:
        had = bool(getattr(session, 'logged_in', False) or getattr(session, 'tutor_id', None))
        session.logged_in = False
        for attr in ['tutor_id', 'tutor_nombres', 'tutor_apellidos', 'tutor_rol', 'tutor_correo']:
            if hasattr(session, attr):
                setattr(session, attr, None)
        if getattr(session, 'user_type', None) == 'admin':
            session.user_type = None
        if hasattr(session.store, 'root'):
            try:
                session.kill()
            except Exception as e:
                print(f"[SESION] Error eliminando archivo de sesión de tutor: {e}")
        return had
    except Exception as e:
        print(f"[SESION] Error en limpiar_tutor_session: {e}")
        return False


def get_session_attr(session, name, default=None):
    try:
        return getattr(session, name, default)
    except Exception:
        return default

def nino_sesion_activa(session):
    """Devuelve True si hay un niño autenticado en la sesión dada."""
    try:
        if session is None:
            return False
        return bool(getattr(session, 'nino_activo', False) or getattr(session, 'nino_id', None))
    except Exception as e:
        print(f"[SESION] Error verificando niño en sesión: {e}")
        return False
