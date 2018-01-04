# from framework.commands.requests.helpers import *

# from framework.commands.settings import ENV, Settings
# from framework.commands.requests.helpers import log_response
from test_utils.utils.utils import log_response

import allure
import pytest
import logging
import requests
import datetime
from datetime import timedelta
import time
from enum import Enum
import inspect

from test_utils import configs

logger = logging.getLogger(__name__)
config = configs.load(__file__)


class Validator:
    class Assertion:
        class Status(Enum):
            PASS = "pass"
            FAILED = "failed"
            XFAIL = "xfail"
            CANCELED = "canceled"

        def __init__(self, status, source, error=None):
            self.status = status
            self.error = error
            self.source = source

    def __init__(self, response=None, await_timeout=None):
        if await_timeout is None:
            await_timeout = config['validator.await_timeout_secs']

        self._await_timeout = await_timeout
        self._sleep_time = 1
        self._last_response = response
        self._assertions = []
        self._input_data = None
        self._multi_asserts = True
        self._checks = []

    def await(self, *checks, input_data=None, expected_status=Assertion.Status.PASS, append_previous_response=False):
        success = False
        wait_until = datetime.datetime.now() + timedelta(seconds=self._await_timeout)
        is_expired = False

        self._input_data = input_data

        while not success and not is_expired:
            is_expired = datetime.datetime.now() > wait_until

            try:
                self.check(*checks, await=False, multi_asserts=self._multi_asserts, input_data=self._input_data, expected_status=expected_status,
                           append_previous_response=append_previous_response)
                success = True
            except AssertionError:
                time.sleep(self._sleep_time)
                with requests.Session() as s:
                    # todo: refactor this
                    with allure.step("[retrying last request]"):
                        logger.info("[retrying last request]")
                        self._last_response = s.send(self._last_response.request)
                        log_response(self._last_response.url, self._last_response)

                        if append_previous_response and isinstance(self._input_data, list):
                            self._input_data.extend(self._last_response.json())
                        else:
                            self._input_data = self._last_response.json()

        if not success and is_expired:
            msg_assertions = ""
            for idx, assertion in enumerate(self._assertions):
                if assertion.status == Validator.Assertion.Status.FAILED:
                    msg_assertions += "Assertion {idx}: {source}\n{error}\n\n".format(idx=idx, source=assertion.source, error=assertion.error)

                if assertion.status == Validator.Assertion.Status.XFAIL:
                    pytest.xfail(assertion.error)

                if assertion.status == Validator.Assertion.Status.CANCELED:
                    pytest.skip(assertion.error)

            raise AssertionError(
                "\n\nTime awaiting things matched has expired. There were follow mismatches: \n\n{errors}".format(errors=msg_assertions))

        return self

    def check(self, *checks, await=False, multi_asserts=True, input_data=None, expected_status=Assertion.Status.PASS, append_previous_response=False):

        if input_data is None:
            input_data = self._last_response.json()

        self._input_data = input_data

        self._multi_asserts = multi_asserts

        if await:
            self.await(*checks, input_data=self._input_data, expected_status=expected_status, append_previous_response=append_previous_response)
            # input_data = self._last_response.json()

        self._assertions = []

        extended_checks = self._checks.copy()
        extended_checks.extend(checks)
        for check in extended_checks:
            try:
                # check(self._input_data)
                check(self._input_data)
                assertion = Validator.Assertion(status=Validator.Assertion.Status.PASS,
                                                source=inspect.getsource(check))
            except Exception as err:
                status = Validator.Assertion.Status.FAILED

                assertion = Validator.Assertion(status=status,
                                                source=inspect.getsource(check),
                                                error=err)

                if not multi_asserts:
                    self._assertions.clear()

            self._assertions.append(assertion)

        # skip if needed:
        if expected_status in [Validator.Assertion.Status.XFAIL, Validator.Assertion.Status.CANCELED]:
            assertion = Validator.Assertion(status=expected_status,
                                            source=None,
                                            error="[waiting for fix tests or backend (look for linked issues)")
            self._assertions.append(assertion)

        # assert if there were FAILED asserttions
        failed_assertions = [assertion for assertion in self._assertions if assertion.status != Validator.Assertion.Status.PASS]
        if len(failed_assertions) > 0:
            msg_assertions = ""
            for idx, assertion in enumerate(failed_assertions):
                if assertion.status == Validator.Assertion.Status.FAILED:
                    msg_assertions += "Assertion {idx}: {source}\n{error}\n\n".format(idx=idx, source=assertion.source, error=assertion.error)

                if assertion.status == Validator.Assertion.Status.XFAIL:
                    pytest.xfail(assertion.error)

                if assertion.status == Validator.Assertion.Status.CANCELED:
                    pytest.skip(assertion.error)

            raise AssertionError(
                "\n\nThere were follow mismatches: \n\n{errors}".format(errors=msg_assertions))

        # # clear input data
        # self._input_data = None

        return self

    def add_checks(self, *checks):
        for check in checks:
            self._checks.append(check)

        return self

    def set_await_timeout(self, await_timeout):
        self._await_timeout = await_timeout
        return self

    def sleep(self, sleep_sec=1):
        time.sleep(sleep_sec)
        return self

    def set_response(self, response):
        self._last_response = response
        return self

    def get_last_response(self):
        return self._last_response
