from sure import assertion, chain, chainproperty, ensure
# from sure.core import DeepComparison, DeepExplanation
# from sure.compat import safe_repr
# from sure.terminal import red, green, yellow
import requests

# from datetime import timezone
# from dateutil import parser

import pytest
import allure
import humanize

# from framework.commands.requests.helpers import *
# from framework.commands.assertions.constants import *
# from framework.commands.requests.constants import *
from utils.utils import *


@chain
def downloadable(self, allow_redirects=False):
    try:
        with allure.step("check: uri is downloadable"):
            r = requests.head(self.obj, allow_redirects=allow_redirects)

            def print_header(headers):
                return "\n".join(['{0}: {1}'.format(k, v) for k, v in headers.items()])

            allure.attach('request debug log', "\n[request %s]: \n%s\n\n[response]: \n%s\n\n%s" %
                          (self.obj, print_request_as_curl(r.request), r.status_code, print_header(r.headers)))

            r.should.have.status_code(200)
    except Exception as err:
        msg = 'could not download item cause: %s'
        raise AssertionError(msg % err)

    return r


@chain
def image(self, allow_redirects=False):
    result = self.obj

    if isinstance(self.obj, requests.Response):
        with allure.step("check: response is image"):
            self.obj.should.have.header('Content-Type').should.equal('image/jpeg')
    elif isinstance(self.obj, str):
        self.obj \
            .should.be.downloadable(allow_redirects=allow_redirects) \
            .should.be.image()

    return result


@chain
def video(self, allow_redirects=False, size_limit=None):
    r = self.obj.should.be.downloadable(allow_redirects=allow_redirects)

    if size_limit:
        r.headers.should.have.key('Content-Length')
        source_size = int(r.headers['Content-Length'])
        size_limit = int(size_limit)
        with ensure("source files size ({}) should be less limit size ({})".format(humanize.naturalsize(source_size),
                                                                                   humanize.naturalsize(size_limit))):
            source_size.should.be.lower_than(size_limit)
    return r


@chain
def key_exist(self, key, status=AssertionStatus.PENDING):
    try:
        self.obj.should.have.key(key).which.should.be.ok
    except AssertionError:
        msg = "key [{0}] is not present in response or its value is empty".format(key)
        if status == AssertionStatus.PENDING:
            pytest.xfail(msg)
        elif status == AssertionStatus.FAILED:
            raise AssertionError(msg)

    return self
