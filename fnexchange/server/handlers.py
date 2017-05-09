import json
import logging
import tornado.web

from fnexchange.server.exceptions import FnexchangeError


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

    def __get_response_body(self, status_code, message, payload=None):
        body = dict()
        body['status'] = status_code
        body['message'] = message
        if payload:
            body['payload'] = payload

        return json.dumps(body, separators=(',', ':'))

    def write_error(self, status_code, **kwargs):
        message = 'Internal Error'
        if "exc_info" in kwargs:
            e = kwargs["exc_info"][1]
            if isinstance(e, FnexchangeError):
                message = e.message

        self.set_header('Content-Type', 'application/json')
        self.set_status(status_code, None)
        self.finish(self.__get_response_body(status_code, message))

    def __get_param(self, param):
        """
        :param param: parameter name to look for in request body
        :type param: str
        :rtype: str
        """
        try:
            return self.request_json[param]
        except KeyError:
            raise FnexchangeError(400, 'Bad request: {0} is required'.format(param))

    def __authorize(self):
        if self.auth_required:
            token = self.__get_param('token')
            if token not in self.auth_tokens:
                raise FnexchangeError(403, 'Unauthorized')

    def __get_plugin(self):
        alias = self.__get_param('alias')
        try:
            return self.registry[alias]
        except KeyError:
            raise FnexchangeError(400, 'No plugin configured for alias {0}'.format(alias))

    def __get_plugin_action(self, plugin):
        action = self.__get_param('action')
        error = False

        # action should only try to access public methods, in order to guard against malicious calls
        if action.startswith('_') or action.endswith('_'):
            error = True

        method = getattr(plugin, action, None)
        if not method:
            error = True

        if error:
            raise FnexchangeError(400, 'Action {0} is not valid'.format(action))
        else:
            return method

    def post(self):
        try:
            # noinspection PyAttributeOutsideInit
            self.request_json = json.loads(self.request.body)
        except:
            raise FnexchangeError(400, "Bad Request")

        self.__authorize()
        plugin = self.__get_plugin()
        plugin_action = self.__get_plugin_action(plugin)

        request_payload = self.__get_param('payload')

        try:
            response_payload = plugin_action(request_payload)
        except:
            msg = 'Runtime error while processing {0}.{1}. Is your payload in the correct format?'
            msg = msg.format(plugin.__class__.__name__, plugin_action.__name__)
            self.logger.exception(msg, exc_info=True)
            raise FnexchangeError(500, msg)

        self.set_header('Content-Type', 'application/json')
        self.finish(self.__get_response_body(200, 'OK', response_payload))
