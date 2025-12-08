import web
from controllers.sessions import get_session_attr, limpiar_nino_session, limpiar_tutor_session, absolute_url

class CerrarSesion:
    def GET(self):
        sess = getattr(web.ctx, 'session', None)
        if getattr(sess, 'user_type', None) == 'nino':
            limpiar_nino_session(sess)
        elif getattr(sess, 'user_type', None) == 'admin' or getattr(sess, 'logged_in', False):
            limpiar_tutor_session(sess)
        raise web.seeother(absolute_url('/'))
