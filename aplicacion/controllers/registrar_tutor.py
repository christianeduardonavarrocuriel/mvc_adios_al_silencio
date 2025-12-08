import os
import web  # type: ignore
from models.db import insertar_tutor
from controllers.sessions import absolute_url

# Local template renderer for Pylance/runtime self-sufficiency
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'views')
render = web.template.render(TEMPLATES_DIR)

class RegistrarTutor:
    def GET(self):
        return render.registrar_tutor()

    def POST(self):
        data = web.input()
        nombres = data.get('nombres','').strip()
        apellidos = data.get('apellidos','').strip()
        correo = data.get('correo','').strip().lower()
        password = data.get('password','').strip()
        rol = data.get('rol','').strip()
        if not all([nombres, apellidos, correo, password, rol]):
            return "Error: Todos los campos son obligatorios."
        if len(password) != 6:
            return "Error: La contraseña debe tener exactamente 6 caracteres."
        if '@' not in correo or '.' not in correo:
            return "Error: Formato de correo inválido."
        try:
            if rol.lower() in ['padre','madre','padre/madre']:
                rol_normalizado = 'Padre'
            elif rol.lower()=='tutor':
                rol_normalizado='Tutor'
            elif rol.lower()=='maestro':
                rol_normalizado='Maestro'
            else:
                rol_normalizado='Padre'

            tutor_id = insertar_tutor(rol_normalizado, nombres, apellidos, correo, password)
            web.ctx.session.tutor_id = tutor_id
            raise web.seeother(absolute_url('/registrar_chiquillo'))
        except web.HTTPError:
            raise
        except Exception as e:
            print("Error registrando tutor:", e)
            mensaje = str(e)
            lowered = mensaje.lower()
            if 'duplicate' in lowered or 'unique' in lowered or 'correo' in lowered:
                return "Error: El correo ya está registrado."
            return f"Error al registrar el tutor: {mensaje}"
