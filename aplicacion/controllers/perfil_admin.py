import os
import web
from models.db import conectar_db
from controllers.sessions import get_session_attr

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
            raise web.seeother('/inicio_administrador')

        if url_tutor_id and url_token:
            try:
                conn = conectar_db(); cur = conn.cursor()
                cur.execute('''SELECT correo, password FROM tutores WHERE id_tutor = ?''', (url_tutor_id,))
                tutor_check = cur.fetchone(); conn.close()
                if tutor_check:
                    correo, password = tutor_check
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
                        raise web.seeother('/inicio_administrador')
                else:
                    raise web.seeother('/inicio_administrador')
            except Exception as e:
                print(f"Error validando token: {e}")
                raise web.seeother('/inicio_administrador')

        try:
            conn = conectar_db(); cur = conn.cursor()
            tutor_id_int = int(tutor_id)
            cur.execute('''SELECT nombres, apellidos, correo, rol FROM tutores WHERE id_tutor = ?''', (tutor_id_int,))
            tutor_data = cur.fetchone()
            if not tutor_data:
                raise web.seeother('/inicio_administrador')
            cur.execute('''SELECT nombres, apellidos, genero, password_figuras FROM ninos WHERE id_tutor = ? ORDER BY nombres''', (tutor_id_int,))
            ninos_data = cur.fetchall(); conn.close()
            tutor_info = {
                'nombres': tutor_data[0],
                'apellidos': tutor_data[1],
                'correo': tutor_data[2],
                'rol': tutor_data[3]
            }
            ninos_info = [{'nombres': n[0], 'apellidos': n[1], 'genero': n[2], 'password_figuras': n[3]} for n in ninos_data]
            return render.perfil_admin(tutor_info, ninos_info)
        except web.HTTPError:
            raise
        except Exception as e:
            print(f"Error cargando perfil admin: {e}")
            raise web.seeother('/inicio_administrador')
