import os
import web
from urllib.parse import unquote

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

class Favicon:
    def GET(self):
        web.header('Content-Type', 'image/x-icon')
        return b''

class StaticFiles:
    def GET(self, path):
        # Decodificar URL y normalizar para evitar 404 por %20
        safe_path = unquote(path)
        file_path = os.path.normpath(os.path.join(STATIC_DIR, safe_path))

        # Evitar path traversal
        if not file_path.startswith(STATIC_DIR):
            raise web.notfound()

        exists = os.path.exists(file_path) and os.path.isfile(file_path)

        if exists:
            ext = os.path.splitext(file_path)[1].lower()
            mime_types = {
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.mp3': 'audio/mpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp',
                '.svg': 'image/svg+xml',
            }
            web.header('Content-Type', mime_types.get(ext, 'application/octet-stream'))
            with open(file_path, 'rb') as f:
                return f.read()

        raise web.notfound()
