import os
import web
from models.db import insertar_nino, ultimo_tutor_id
from controllers.sessions import get_session_attr, absolute_url

# Local render setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'views')
render = web.template.render(TEMPLATES_DIR)

class RegistrarChiquillo:
    def GET(self):
        return render.registrar_chiquillo()

    def POST(self):
        data = web.input()
        sess = getattr(web.ctx, 'session', None)
        tutor_id = get_session_attr(sess, 'tutor_id')
        if not tutor_id:
            try:
                tutor_id = ultimo_tutor_id()
                if tutor_id and sess:
                    sess.tutor_id = tutor_id
            except Exception as e:
                print('Error en id tutor:', e)
                return 'Error: Registre primero al tutor.'
        if not tutor_id:
            return 'Error: No hay tutor asociado.'

        indices = []
        for k in data.keys():
            if k.startswith('nombre_'):
                try:
                    num = int(k.split('_')[1])
                    if num not in indices:
                        indices.append(num)
                except ValueError:
                    pass
        indices.sort()
        if not indices:
            return 'Error: No se recibieron niños.'

        permitidos = {'ajolote','borrego','oso','perro'}
        registros = []
        try:
            for idx in indices:
                nombre = data.get(f'nombre_{idx}','').strip()
                apellidos = data.get(f'apellidos_{idx}','').strip()
                genero = data.get(f'tipo_usuario_{idx}','').strip()
                password_raw = data.get(f'contraseña_{idx}','').strip()
                if not all([nombre, apellidos, genero, password_raw]):
                    return f'Error: Faltan datos en Niño {idx}.'
                if genero not in ['Ajolotito','Ajolotita']:
                    return f'Error: Género inválido en Niño {idx}.'
                animales = [a for a in password_raw.split(',') if a]
                if len(animales) != 4:
                    return f'Error: La contraseña del Niño {idx} debe tener exactamente 4 animales.'
                if any(a not in permitidos for a in animales):
                    return f'Error: Niño {idx} tiene animales no permitidos.'
                password_figuras = ','.join(animales)
                nino_id = insertar_nino(tutor_id, genero, nombre, apellidos, password_figuras)
                registros.append((nino_id, nombre))
            print(f"Niños insertados: {len(registros)} para tutor {tutor_id}")
            raise web.seeother(absolute_url('/'))
        except web.HTTPError:
            raise
        except Exception as e:
            print('Error registrando niños:', e)
            return 'Error al registrar los niños.'
