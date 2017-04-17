import tornado.ioloop
import tornado.web

from fnexchange.server.handlers import APIHandler


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
