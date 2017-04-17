from tornado.web import HTTPError


class FnexchangeError(HTTPError):
    def __init__(self, status_code, message, **kwargs):
        log_message = kwargs.pop('log_message', message)
        super(FnexchangeError, self).__init__(status_code, log_message=log_message, **kwargs)
        self.message = message
