import os
import web
from models.db import obtener_nino_login
from controllers.sessions import set_nino_session, absolute_url

# Local render setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'views')
render = web.template.render(TEMPLATES_DIR)

class IniciarSesion:
    def GET(self):
        return render.iniciar_sesion()

    def POST(self):
        data = web.input()
        nombre = data.get('nombre','').strip()
        apellidos = data.get('primer_apellido-y-segundo-apellido','').strip()
        password_animales = (data.get('password_animales','') or data.get('contraseña','')).strip()

        if not (nombre and apellidos and password_animales):
            raise web.seeother(absolute_url('/iniciar_sesion?error=campos'))

        animales = [a for a in password_animales.split(',') if a]
        permitidos = {'ajolote','borrego','oso','perro'}
        if len(animales) != 4:
            raise web.seeother(absolute_url('/iniciar_sesion?error=pass'))
        if any(a not in permitidos for a in animales):
            raise web.seeother(absolute_url('/iniciar_sesion?error=animales'))

        try:
            row = obtener_nino_login(nombre, apellidos, password_animales)

            if not row:
                raise web.seeother(absolute_url('/iniciar_sesion?error=credenciales'))

            sess = getattr(web.ctx, 'session', None)
            set_nino_session(sess, row)
            activo = bool(getattr(sess,'nino_activo',False) or getattr(sess,'nino_id',None))
            raise web.seeother(absolute_url('/saludo_chiquillo'))
        except web.HTTPError:
            raise
        except Exception as e:
            print('Error autenticando niño:', e)
            raise web.seeother(absolute_url('/iniciar_sesion?error=sistema'))
