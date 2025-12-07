import os
import web  # type: ignore
import sqlite3
from models.db import conectar_db

# Local template renderer for Pylance/runtime self-sufficiency
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'views')
render = web.template.render(TEMPLATES_DIR)

class RegistrarTutor:
    def GET(self):
        return render.registrar_tutor()

    def POST(self):
        data = web.input()
        print("Información del tutor recibida:", dict(data))
        nombres = data.get('nombres','').strip()
        apellidos = data.get('apellidos','').strip()
        correo = data.get('correo','').strip().lower()
        password = data.get('password','').strip()
        rol = data.get('rol','').strip()
        print(f"Información procesada -> nombres='{nombres}' apellidos='{apellidos}' correo='{correo}' password='{password}' rol='{rol}'")
        if not all([nombres, apellidos, correo, password, rol]):
            return "Error: Todos los campos son obligatorios."
        if len(password) != 6:
            return "Error: La contraseña debe tener exactamente 6 caracteres."
        if '@' not in correo or '.' not in correo:
            return "Error: Formato de correo inválido."
        try:
            conn = conectar_db()
            cur = conn.cursor()
            if rol.lower() in ['padre','madre','padre/madre']:
                rol_normalizado = 'Padre'
            elif rol.lower()=='tutor':
                rol_normalizado='Tutor'
            elif rol.lower()=='maestro':
                rol_normalizado='Maestro'
            else:
                rol_normalizado='Padre'
            cur.execute('''INSERT INTO tutores (rol,nombres,apellidos,correo,password) VALUES (?,?,?,?,?)''',
                        (rol_normalizado,nombres,apellidos,correo,password))
            tutor_id = cur.lastrowid
            conn.commit()
            conn.close()
            web.ctx.session.tutor_id = tutor_id
            print(f"Tutor registrado exitosamente: {tutor_id} {nombres} {apellidos} {rol_normalizado}")
            raise web.seeother('/registrar_chiquillo')
        except sqlite3.IntegrityError:
            try:
                conn.rollback(); conn.close()
            except Exception:
                pass
            return "Error: El correo ya está registrado."
        except web.HTTPError:
            raise
        except Exception as e:
            try:
                conn.rollback(); conn.close()
            except Exception:
                pass
            print("Error registrando tutor:", e)
            return "Error al registrar el tutor."
