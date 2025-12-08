import web
from controllers.sessions import get_session_attr, limpiar_nino_session, limpiar_tutor_session, absolute_url

class CerrarSesion:
    def GET(self):
        sess = getattr(web.ctx, 'session', None)
        if getattr(sess, 'user_type', None) == 'nino':
            activo = bool(getattr(sess,'nino_activo',False) or getattr(sess,'nino_id',None))
            print(f"[LOGOUT] Estado antes: niño conectado={activo} id={get_session_attr(sess,'nino_id')} nombre={get_session_attr(sess,'nino_nombre')}")
            had = limpiar_nino_session(sess)
            nuevo = bool(getattr(sess,'nino_activo',False) or getattr(sess,'nino_id',None))
            print(f"[LOGOUT] Resultado -> se desconectó={had} ahora conectado={nuevo}")
        elif getattr(sess, 'user_type', None) == 'admin' or getattr(sess, 'logged_in', False):
            activo = bool(getattr(sess, 'logged_in', False) or getattr(sess, 'tutor_id', None))
            print(f"[LOGOUT] Estado antes: tutor/admin conectado={activo} id={get_session_attr(sess,'tutor_id')} nombre={get_session_attr(sess,'tutor_nombres')}")
            had = limpiar_tutor_session(sess)
            print(f"[LOGOUT] Resultado -> se desconectó={had} ahora conectado={get_session_attr(sess,'logged_in', False)}")
        raise web.seeother(absolute_url('/'))
