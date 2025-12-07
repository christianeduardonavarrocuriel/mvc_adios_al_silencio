import os
import sys
import web
import sqlite3

# Directorios base y recursos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ensure local packages (controllers, models) are importable regardless of cwd
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
TEMPLATES_DIR = os.path.join(BASE_DIR, 'views')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Render local opcional (los controladores definen su propio render)
render = web.template.render(TEMPLATES_DIR, cache=False)

"""
Importación centralizada de modelos, helpers y controladores.
Mantén estos nombres sincronizados con los archivos reales en controllers/.
"""

# Models
from models.db import conectar_db, init_db

# Session helpers
from controllers.sessions import (
    set_nino_session,
    limpiar_nino_session,
    limpiar_tutor_session,
    get_session_attr,
)

# Controllers (clases manejadoras de rutas)
from controllers.index import Index
from controllers.cerrar_sesion import CerrarSesion
from controllers.registrar_tutor import RegistrarTutor
from controllers.registrar_chiquillo import RegistrarChiquillo
from controllers.admin_login import InicioAdministrador
from controllers.perfil_admin import PerfilAdmin
from controllers.editar_perfil import EditarPerfil
from controllers.iniciar_sesion import IniciarSesion
from controllers.static_pages import (
    SaludoAdmin,
    SaludoChiquillo,
    PresentacionLucas,
    PresentacionPagina,
    Lecciones,
    QuienesSomos,
    Introduccion,
    LeccionCoordinacion,
    LeccionCompletada,
)
from controllers.assets import Favicon, StaticFiles

# CONFIGURACIÓN DE URLS Y APLICACIÓN
# Mapeo de rutas URL a clases controladoras
urls = (
    '/', 'Index',                                    # Página principal
    '/registrar_tutor', 'RegistrarTutor',           # Registro de tutores/padres
    '/registrar_chiquillo', 'RegistrarChiquillo',   # Registro de niños
    '/inicio_administrador', 'InicioAdministrador', # Login de administradores
    '/saludo_admin', 'SaludoAdmin',                 # Saludo para administradores
    '/saludo_chiquillo', 'SaludoChiquillo',         # Saludo para niños
    '/cerrar_sesion', 'CerrarSesion',               # Cerrar sesión
    '/presentacion_lucas', 'PresentacionLucas',     # Presentación del personaje Lucas
    '/presentacion_pagina', 'PresentacionPagina',   # Presentación de la página
    '/lecciones', 'Lecciones',                      # Página de lecciones
    '/perfil_admin', 'PerfilAdmin',                 # Perfil del administrador
    '/editar_perfil', 'EditarPerfil',               # Editar perfil del administrador
    '/iniciar_sesion', 'IniciarSesion',             # Login de niños
    '/quienes_somos', 'QuienesSomos',               # Página "Quiénes Somos"
    '/introduccion', 'Introduccion',                # Lección de introducción
    '/leccion_coordinacion', 'LeccionCoordinacion', # Lección de coordinación
    '/leccion_completada', 'LeccionCompletada',     # Página de lección completada
    '/favicon.ico', 'Favicon',                      # Icono del sitio
    '/static/(.*)', 'StaticFiles',                  # Archivos estáticos
)

# Crear instancia de la aplicación web
app = web.application(urls, globals())

# Configuración de sesiones (usar ruta absoluta y manejo robusto)
SESSIONS_DIR = os.path.join(BASE_DIR, 'sessions')
os.makedirs(SESSIONS_DIR, exist_ok=True)
print(f"[SESION] Directorio de sesiones: {SESSIONS_DIR}")

# Initializer completo con todos los atributos necesarios
session_initializer = {
    'tutor_id': None, 
    'user_type': None,
    'nino_id': None,
    'nino_nombre': None,
    'nino_apellidos': None,
    'nino_activo': False,
    # Atributos para administrador
    'logged_in': False,
    'tutor_nombres': None,
    'tutor_apellidos': None,
    'tutor_rol': None,
    'tutor_correo': None
}

try:
    session = web.session.Session(app, web.session.DiskStore(SESSIONS_DIR),
                                  initializer=session_initializer)
    print(f"[SESION] Sesión inicializada correctamente con DiskStore")
    # Hacer disponible la sesión como web.ctx.session en cada request
    def _load_session():
        web.ctx.session = session
    app.add_processor(web.loadhook(_load_session))
except PermissionError as e:
    print(f"[SESION] No se pudo inicializar la sesión por permisos: {e}")
    # Fallback a memoria (no persistente)
    class DummyStore(dict):
        def __contains__(self, key):
            return dict.__contains__(self, key)
    session = web.session.Session(app, DummyStore(), initializer=session_initializer)
    print(f"[SESION] Usando DummyStore (memoria) - sesiones no persistentes")

# PUNTO DE ENTRADA PRINCIPAL

# Crear función WSGI para deployment
application = app.wsgifunc()

if __name__ == "__main__":
    try:
        # Inicializar la base de datos al arrancar el servidor
        print("Inicializando base de datos...")
        init_db()
        print("Base de datos inicializada correctamente")
        
        # Configurar puerto del servidor
        PORT = 80
        HOST = '127.0.0.1'
        
        print(f"Servidor iniciando en http://{HOST}:{PORT}")
        print("Presiona Ctrl+C para detener el servidor")
        
        # Iniciar el servidor web
        import sys
        sys.argv = ['app.py', f'{HOST}:{PORT}']  # Configurar argumentos
        app.run()  # Iniciar el servidor
        
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")  # Cuando presionan Ctrl+C
    except Exception as e:
        print(f"Error al iniciar servidor: {e}")
        print("Verifica que el puerto 8081 no esté en uso")
        import traceback
        traceback.print_exc()  # Mostrar detalles completos del error