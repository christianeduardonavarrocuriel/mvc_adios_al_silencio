import os
import web
from models.db import obtener_tutor_por_id, ninos_por_tutor
from controllers.sessions import get_session_attr, absolute_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'views')
render = web.template.render(TEMPLATES_DIR)

class PerfilAdmin:
    def GET(self):
        input_data = web.input()
        url_tutor_id = input_data.get('tutor_id', None)
        url_token = input_data.get('token', None)

        sess = getattr(web.ctx, 'session', None)
        logged_in = get_session_attr(sess, 'logged_in', False)
        session_tutor_id = get_session_attr(sess, 'tutor_id', None)

        tutor_id = session_tutor_id or url_tutor_id
        if not tutor_id:
            raise web.seeother(absolute_url('/inicio_administrador'))

        if url_tutor_id and url_token:
            try:
                tutor_check = obtener_tutor_por_id(int(url_tutor_id))
                if tutor_check:
                    correo = tutor_check['correo']
                    password = tutor_check.get('password', '') if isinstance(tutor_check, dict) else ''
                    expected_token = password[:3] + correo[:3]
                    if url_token == expected_token:
                        tutor_id = url_tutor_id
                        try:
                            sess.logged_in = True
                            sess.tutor_id = int(url_tutor_id)
                            sess.user_type = 'admin'
                        except Exception:
                            pass
                    else:
                        raise web.seeother(absolute_url('/inicio_administrador'))
                else:
                    raise web.seeother(absolute_url('/inicio_administrador'))
            except Exception as e:
                print(f"Error validando token: {e}")
                raise web.seeother(absolute_url('/inicio_administrador'))

        try:
            tutor_id_int = int(tutor_id)
            tutor_data = obtener_tutor_por_id(tutor_id_int)
            if not tutor_data:
                raise web.seeother(absolute_url('/inicio_administrador'))
            ninos_data = ninos_por_tutor(tutor_id_int)
            tutor_info = {
                'nombres': tutor_data.get('nombres'),
                'apellidos': tutor_data.get('apellidos'),
                'correo': tutor_data.get('correo'),
                'rol': tutor_data.get('rol')
            }
            ninos_info = [{'nombres': n['nombres'], 'apellidos': n['apellidos'], 'genero': n['genero'], 'password_figuras': n['password_figuras']} for n in ninos_data]
            return render.perfil_admin(tutor_info, ninos_info)
        except web.HTTPError:
            raise
        except Exception as e:
            print(f"Error cargando perfil admin: {e}")
            raise web.seeother(absolute_url('/inicio_administrador'))
