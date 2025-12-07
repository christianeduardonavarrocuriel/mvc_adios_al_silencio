import os
import web  # type: ignore

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'views')
render = web.template.render(TEMPLATES_DIR, cache=False)

class SaludoAdmin:
    def GET(self):
        return render.saludo_admin()

class SaludoChiquillo:
    def GET(self):
        return render.saludo_chiquillo()

class PresentacionLucas:
    def GET(self):
        return render.presentacion_lucas()

class PresentacionPagina:
    def GET(self):
        return render.presentacion_pagina()

class Lecciones:
    def GET(self):
        return render.lecciones()

class QuienesSomos:
    def GET(self):
        return render.quienes_somos()

class Introduccion:
    def GET(self):
        html_path = os.path.join(TEMPLATES_DIR, 'introduccion.html')
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return "<h1>No se encontró la introducción</h1>"

class LeccionCoordinacion:
    def GET(self):
        return render.leccion_coordinacion()

class LeccionCompletada:
    def GET(self):
        return render.leccion_completada()
