import os
import web

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

class Favicon:
    def GET(self):
        web.header('Content-Type', 'image/x-icon')
        return b''

class StaticFiles:
    def GET(self, path):
        file_path = os.path.join(STATIC_DIR, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            ext = os.path.splitext(path)[1].lower()
            mime_types = {
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.mp3': 'audio/mpeg',
            }
            web.header('Content-Type', mime_types.get(ext, 'application/octet-stream'))
            with open(file_path, 'rb') as f:
                return f.read()
        else:
            raise web.notfound()
