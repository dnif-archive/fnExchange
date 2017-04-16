import tornado.httpserver
import tornado.ioloop
import tornado.web
import logging

from tornado.web import HTTPError


class APIHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(APIHandler, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger('fnexchange.server.handlers.api')

    # noinspection PyAttributeOutsideInit
    def initialize(self, registry, auth_required, auth_tokens, upstream_timeout=None, **kwargs):
        self.auth_required = auth_required
        self.auth_tokens = auth_tokens
        self.registry = registry
        self.upstream_timeout = upstream_timeout

    def __authorize(self):
        if self.auth_required:
            # check request token
            if 'TOKEN_HERE' not in self.auth_tokens:
                raise HTTPError(403, 'Unauthorized access')

    def post(self):
        self.__authorize()
        self.write("Hello world")


def get_app(port, app_settings, handlers_settings):
    url_patterns = [
        (r"/", APIHandler, handlers_settings[APIHandler]),
    ]
    app = tornado.web.Application(url_patterns, **app_settings)
    app.listen(port)
    return app


def start_app(port, app_settings, handlers_settings):
    app = get_app(port, app_settings, handlers_settings)
    print('Starting server, listening on port {0}'.format(port))
    tornado.ioloop.IOLoop.instance().start()
