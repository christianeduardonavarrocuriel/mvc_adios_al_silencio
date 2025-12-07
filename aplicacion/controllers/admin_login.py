import os
import web
from models.db import conectar_db

# Local render setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'views')
render = web.template.render(TEMPLATES_DIR)

class InicioAdministrador:
    def GET(self):
        return render.inicio_administrador()

    def POST(self):
        data = web.input()
        correo = data.get('correo', '').strip().lower()
        password = data.get('contraseña', '').strip()
        if not correo or not password:
            with open(os.path.join(TEMPLATES_DIR, 'inicio_administrador.html'), 'r', encoding='utf-8') as f:
                html_content = f.read()
            return html_content + "<script>alert('Error: Por favor ingresa tu correo y contraseña.');</script>"
        try:
            conn = conectar_db(); cur = conn.cursor()
            cur.execute('''SELECT id_tutor, nombres, apellidos, rol, correo, password 
                           FROM tutores 
                           WHERE lower(correo) = ? AND password = ? 
                           LIMIT 1''', (correo, password))
            tutor = cur.fetchone(); conn.close()
            if tutor:
                tutor_id, nombres, apellidos, rol, correo_db, password_db = tutor
                sess = getattr(web.ctx, 'session', None)
                sess.logged_in = True
                sess.tutor_id = tutor_id
                sess.user_type = 'admin'
                sess.tutor_nombres = nombres
                sess.tutor_apellidos = apellidos
                sess.tutor_rol = rol
                sess.tutor_correo = correo_db
                token = password[:3] + correo[:3]
                raise web.seeother(f'/perfil_admin?tutor_id={tutor_id}&token={token}')
            else:
                with open(os.path.join(TEMPLATES_DIR, 'inicio_administrador.html'), 'r', encoding='utf-8') as f:
                    html_content = f.read()
                return html_content + "<script>alert('Error: Correo o contraseña incorrectos.');</script>"
        except web.HTTPError:
            raise
        except Exception:
            with open(os.path.join(TEMPLATES_DIR, 'inicio_administrador.html'), 'r', encoding='utf-8') as f:
                html_content = f.read()
            return html_content + "<script>alert('Error del sistema. Intenta de nuevo.');</script>"
