import os
import web
from models.db import conectar_db
from controllers.sessions import set_nino_session

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

        print(f"[LOGIN] Datos recibidos -> nombre='{nombre}' apellidos='{apellidos}' password='{password_animales}'")
        if not (nombre and apellidos and password_animales):
            raise web.seeother('/iniciar_sesion?error=campos')

        animales = [a for a in password_animales.split(',') if a]
        permitidos = {'ajolote','borrego','oso','perro'}
        if len(animales) != 4:
            raise web.seeother('/iniciar_sesion?error=pass')
        if any(a not in permitidos for a in animales):
            raise web.seeother('/iniciar_sesion?error=animales')

        try:
            conn = conectar_db()
            cur = conn.cursor()
            cur.execute('''SELECT id_nino, nombres, apellidos, id_tutor, password_figuras FROM ninos
                           WHERE lower(nombres)=? AND lower(apellidos)=? AND password_figuras=? LIMIT 1''',
                        (nombre.lower(), apellidos.lower(), password_animales))
            row = cur.fetchone()
            conn.close()

            print(f"[LOGIN] Resultado query -> {row}")
            if not row:
                raise web.seeother('/iniciar_sesion?error=credenciales')

            sess = getattr(web.ctx, 'session', None)
            set_nino_session(sess, row)
            activo = bool(getattr(sess,'nino_activo',False) or getattr(sess,'nino_id',None))
            print(f"[LOGIN OK] Niño autenticado id={row[0]} nombre='{row[1]}' sesion_activa={activo}")
            raise web.seeother('/saludo_chiquillo')
        except web.HTTPError:
            raise
        except Exception as e:
            print('Error autenticando niño:', e)
            raise web.seeother('/iniciar_sesion?error=sistema')
