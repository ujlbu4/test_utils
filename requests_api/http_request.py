# from framework.commands.requests.helpers import *
# from framework.commands.settings import ENV, Environment

import logging
from utils.utils import log_response

logger = logging.getLogger(__name__)


class BaseRequestsAPI:
    def __init__(self, bearer=None, assert_status_code=True):
        # instance variable (not class variable)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json;q=0.9,*/*;q=0.8"
        }

        self.authenticate_request(bearer=bearer)

        self.assert_status_code = assert_status_code
        self._timeout = 60

    def authenticate_request(self, bearer):
        if bearer is not None:
            self.headers['Bearer'] = self.bearer = bearer

        return self

    def execute_request(self, method, path, **kwargs):

        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers

        r = method(url=self.base_url + path, timeout=self._timeout, **kwargs)

        log_response(path, r)

        if self.assert_status_code:
            r.status_code.should.be.within(200, 299)
            # r.should.have.status_code(200)

        return r
