# from framework.commands.dsl import Validator
from validator.validator import Validator
from sure import expect, ensure

# from framework.commands.assertions.assertions_request import extract
from assertions.assertions_request import extract

import requests_mock
import requests


class TestValidatorCheck:
    def test_custom_input_data_positive(self):
        validator = Validator()

        input_data = {"a": 1}

        validator.check(
            lambda r: r.should.be.equal({"a": 1}),
            await=False,
            multi_asserts=True,
            input_data=input_data)

    def test_custom_input_data_negative(self):
        validator = Validator()

        input_data = {"a": 1}

        expect(validator.check) \
            .when.called_with(lambda r: r.should.be.equal({"a": 2}),
                              await=False,
                              multi_asserts=True,
                              input_data=input_data) \
            .should.have.raised(AssertionError)

    def test_multi_assertions(self):
        validator = Validator()

        input_data = {"a": 1, "b": 2}

        # not throw exception
        validator.check(
            lambda r: r['a'].should.be.equal(1),
            lambda r: r['b'].should.be.equal(2),
            await=False,
            input_data=input_data)

        # make sure it checks all assertions
        expect(validator.check) \
            .when.called_with(
            lambda r: r['a'].should.be.equal("incorrect value"),
            lambda r: r['b'].should.be.equal(2),  # correct one,
            lambda r: r['a'].should.be.equal(1),  # correct one,
            await=False,
            input_data=input_data) \
            .should.have.raised(AssertionError)

        expect(validator.check) \
            .when.called_with(
            lambda r: r['a'].should.be.equal(1),  # correct one,
            lambda r: r['b'].should.be.equal(2),  # correct one,
            lambda r: r['a'].should.be.equal("incorrect value"),
            await=False,
            input_data=input_data) \
            .should.have.raised(AssertionError)

    def test_last_response_await_true_negative(self):
        """
        check last response and await during some period of time until it became sucsess (negative scenario)
        """
        with requests_mock.mock() as m:
            # setup mock
            url = 'http://test.com'
            response_json = {"a": 1, "b": 2}
            m.get(url, json=response_json)

            # test
            validator = Validator(response=requests.get(url=url), await_timeout=2)

            # check it tried to request few times
            expect(validator.check) \
                .when.called_with(
                lambda r: r['a'].should.be.equal("incorrect value"),
                await=True,
                input_data=None) \
                .should.have.raised(AssertionError)

            m.called.should.be.true
            m.call_count.should.be.greater_than(1)  # called more then 1 time

    def test_last_response_await_true_positive(self):
        """
        check last response and await during some period of time until it became sucsess (positive scenario)
        """
        with requests_mock.mock() as m:
            # setup mock
            url = 'http://test.com'
            response_json = {"a": 1, "b": 2}
            m.get(url, json=response_json)

            # test
            validator = Validator(response=requests.get(url=url), await_timeout=2)

            validator.check(
                lambda r: r['a'].should.be.equal(1),  # correct one
                await=True,
                input_data=None
            )

            m.called.should.be.true
            m.call_count.should.be.equal(1)  # called exactly 1 time

    def test_last_response_await_false_positive(self):
        """
        just check last response _without_ waiting until it became success (positive scenario)
        """
        with requests_mock.mock() as m:
            # setup mock
            url = 'http://test.com'
            response_json = {"a": 1, "b": 2}
            m.get(url, json=response_json)

            # test
            validator = Validator(response=requests.get(url=url), await_timeout=2)

            # check it tried to request few times
            validator.check(
                lambda r: r['a'].should.be.equal(1),  # correct one
                await=True,
                input_data=None
            )

            m.called.should.be.true
            m.call_count.should.be.equal(1)  # called exactly 1 time

    def test_last_response_await_false_negative(self):
        """
        just check last response _without_ waiting until it became success (negative scenario)
        """
        with requests_mock.mock() as m:
            # setup mock
            url = 'http://test.com'
            response_json = {"a": 1, "b": 2}
            m.get(url, json=response_json)

            # test
            validator = Validator(response=requests.get(url=url), await_timeout=2)

            # check it tried to request few times
            expect(validator.check) \
                .when.called_with(
                lambda r: r['a'].should.be.equal("incorrect value"),
                await=False,
                input_data=None) \
                .should.have.raised(AssertionError)

            m.called.should.be.true
            m.call_count.should.be.equal(1)  # called exactly 1 time

    def test_few_checks_in_a_row_direct_input_data(self):
        validator = Validator()

        input_data1 = {"a": 1, "b": 2}
        input_data2 = {"c": 3, "d": 4}

        validator \
            .check(lambda r: r['a'].should.be.equal(1),
                   await=False, multi_asserts=True, input_data=input_data1) \
            .check(lambda r: r['c'].should.be.equal(3),
                   lambda r: r.should_not.have.key("a"),
                   await=False, multi_asserts=True, input_data=input_data2)

    def test_few_checks_in_a_row_requests(self):
        with requests_mock.mock() as m:
            # setup mock
            url1 = 'http://test1.com'
            url2 = 'http://test2.com'
            response_json1 = {"a": 1, "b": 2}
            response_json2 = {"c": 3, "d": 4}
            m.get(url1, json=response_json1)
            m.get(url2, json=response_json2)

            # test
            validator = Validator(response=requests.get(url=url1), await_timeout=2)

            validator \
                .check(lambda r: r['a'].should.be.equal(1),
                       await=False) \
                .set_response(response=requests.get(url=url2)) \
                .check(lambda r: r['c'].should.be.equal(3),
                       lambda r: r.should_not.have.key("a"),
                       await=False, )

    def test_append_previous_response_true(self):
        with requests_mock.mock() as m:
            # setup mock
            url1 = 'http://test1.com'
            url2 = 'http://test2.com'
            response_json1 = [{"a": 1, "b": 2}]
            response_json2 = [{"c": 3, "d": 4}]
            m.get(url1, json=response_json1)
            m.get(url2, json=response_json2)

            # test
            validator = Validator(response=requests.get(url=url1), await_timeout=2)

            expect(validator.check) \
                .when.called_with(
                lambda r: r.should.extract({"a": "incorrect value"}),
                await=True,
                append_previous_response=True) \
                .should.have.raised(AssertionError)

            # cause we append all previous responses
            len(validator._input_data).should.be.greater_than(1)

    def test_extended_checks(self):
        input_data = {"a": 1, "b": 2}
        validator = Validator()

        validator.add_checks(lambda r: r['b'].should.be.equal("incorrect value"))

        expect(validator.check) \
            .when.called_with(
            lambda r: r['a'].should.be.equal(1),  # correct one
            await=False,
            input_data=input_data) \
            .should.have.raised(AssertionError) # cause "add checks" added incorrect one
