import os
import web

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'views')

class Index:
    def GET(self):
        # Asegurar que el navegador interprete como HTML
        web.header('Content-Type', 'text/html; charset=utf-8')
        html_path = os.path.join(TEMPLATES_DIR, 'index.html')
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            contenido = contenido.replace('<!--LOGOUT_MARK-->', '')
            return contenido
        return 'No se encontró la página principal'
