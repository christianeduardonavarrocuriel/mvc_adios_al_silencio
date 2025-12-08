import os
import web
from models.db import actualizar_tutor
from controllers.sessions import absolute_url

# Local render setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'views')
render = web.template.render(TEMPLATES_DIR)

class EditarPerfil:
    def GET(self):
        return render.editar_perfil_nuevo(None)

    def POST(self):
        data = web.input()
        tutor_id = data.get('tutor_id', '').strip()
        nombres = data.get('nombres', '').strip()
        apellidos = data.get('apellidos', '').strip()
        correo = data.get('correo', '').strip().lower()
        rol = data.get('rol', '').strip()
        password = data.get('password', '').strip()
        verificar_password = data.get('verificar_password', '').strip()
        if not all([tutor_id, nombres, apellidos, correo, rol, password, verificar_password]):
            return "Error: Todos los campos son obligatorios."
        if password != verificar_password:
            return "Error: Las contraseñas no coinciden."
        if len(password) != 6:
            return "Error: La contraseña debe tener exactamente 6 caracteres."
        try:
            actualizar_tutor(int(tutor_id), nombres, apellidos, correo, rol, password)
            nuevo_token = password[:3] + correo[:3]
            raise web.seeother(absolute_url(f'/perfil_admin?tutor_id={tutor_id}&token={nuevo_token}'))
        except web.HTTPError:
            raise
        except Exception as e:
            print(f"Error actualizando perfil: {e}")
            mensaje = str(e)
            if 'duplicate' in mensaje.lower() or 'unique' in mensaje.lower():
                return "Error: El correo ya está registrado."
            return f"Error al actualizar el perfil: {mensaje}"
