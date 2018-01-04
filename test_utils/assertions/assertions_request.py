from sure import assertion, chain
from sure.core import DeepComparison, DeepExplanation
from sure.compat import safe_repr
from sure.terminal import red, green

from datetime import datetime, timezone
from dateutil import parser

import operator

from test_utils.utils.utils import dt_from_ms


@assertion
def status_code(self, expected_status_code):
    if self.negative:
        assert expected_status_code != self.obj.status_code, 'Expected return code matches'
    else:
        assert expected_status_code == self.obj.status_code, \
            'Expected return code [%s] does not match real status code [%s]' % (
                expected_status_code, self.obj.status_code)

    return True


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def convert_to_datetime(value):
    if type(value) == int:
        return dt_from_ms(value)
    elif type(value) == datetime:
        return value
    elif type(value) == str:
        if is_integer(value):
            # unix epoch timestamp
            return dt_from_ms(int(value))
        else:
            return parser.parse(value)


def normalize_input_datetime(value):
    return convert_to_datetime(value).astimezone(timezone.utc)


@assertion
def almost_equal(self, expected_datetime, acceptable_delta_sec=10):
    """
    Compare actual and expected datetimes.
    Input datetime could be a string (example: '2017-09-07 09:41:20.714918') or unix epoch timestamp in ms(example: 1504788133167)
    """
    expected_datetime = normalize_input_datetime(expected_datetime)
    actual_datetime = normalize_input_datetime(self.obj)

    timedelta = abs(actual_datetime - expected_datetime).seconds

    if self.negative:
        assert timedelta > acceptable_delta_sec, 'Dates should not be equal: real [%s] == expected [%s] ' \
                                                 % (actual_datetime, expected_datetime)
    else:
        assert timedelta < acceptable_delta_sec, 'Dates not equals as expected: real [%s] != expected [%s]' \
                                                 % (actual_datetime, expected_datetime)

    return True


@chain
def header(self, header_name):
    # check if header name actually exists
    self.obj.headers.should.have.key(header_name)
    # return header value
    return self.obj.headers[header_name]


class ComparisonWrapper(DeepComparison):
    """
    Extending `Sure` library by custom methods 
    """

    def compare_dicts(self, X, Y):
        """
        Difference from parent class is that it could do partial matching
        
        :param X: first dict
        :param Y: second dict
        :return: True if comparing is succesfull, otherwise it will throw AssertionError
        """
        c = self.get_context()

        x_keys = list(sorted(X.keys()))
        y_keys = list(sorted(Y.keys()))

        diff_y = list(set(y_keys).difference(set(x_keys)))
        if diff_y:
            msg = "Filter Param%s has the key %%r whereas Source Item%s does not" % (
                red(c.current_X_keys),
                green(c.current_Y_keys),
            ) % safe_repr(diff_y[0])
            return DeepExplanation(msg).as_assertion(X, Y)

        elif X == Y:
            return True
        else:
            for key in y_keys:
                self.key_X = key
                self.key_Y = key
                value_X = X[key]
                value_Y = Y[key]

                child = ComparisonWrapper(
                    value_X,
                    value_Y,
                    epsilon=self.epsilon,
                    parent=self,
                ).compare()

                if isinstance(child, DeepExplanation):
                    return child.as_assertion(value_X, value_Y)

            return True


@chain
def extract(self, filter_param):
    """
    Extract only one (first one) element which has been matched
    
    :param self: `sure` object
    :param filter_param: param by which it will be matching
    :return: list of items, otherwise exception will throw 
    """

    comparison = False
    result = None
    for item in self.obj:
        if isinstance(filter_param, dict):
            try:
                comparison = ComparisonWrapper(item, filter_param).compare()
            except AssertionError:
                pass

            if comparison:
                result = item
                break
        else:
            raise TypeError('Expecting dict type for filter_param parameter instead of [%s]' % type(filter_param))

    if self.negative:
        if comparison:
            raise AssertionError('Found [%s] in source items, but not expected to find it' % filter_param)
    else:
        if not comparison:
            raise AssertionError('Did not find [{filter_param}] in source items: {source_items}'.format(filter_param=filter_param,
                                                                                                        source_items=self.obj))

    return result


@chain
def filter(self, filter_param):
    """
    Will return a list of matched elements from source collection
    
    :param self: 
    :param filter_param: 
    :return: list of items, otherwise exception will throw
    """

    result = []

    if not isinstance(self.obj, list):
        raise TypeError('Expected list type, not [%s] type' % type(self.obj))

    for item in self.obj:
        comparison = False
        if isinstance(filter_param, dict):
            try:
                comparison = ComparisonWrapper(item, filter_param).compare()
            except AssertionError:
                pass

            if comparison:
                result.append(item)
        else:
            raise TypeError('Expecting dict type for filter_param parameter instead of [%s]' % type(filter_param))

    return result


@assertion
def sorted_by(self, compare=operator.ge, key=lambda x: x):
    # todo: check self.obj if is_iterable
    lst = self.obj

    compared_list = [compare(key(lst[i]), key(lst[i + 1])) for i in range(len(lst) - 1)]
    is_sorted = all(compared_list)
    if self.negative:
        assert is_sorted is False, 'Expected list would not be sorted as [{operator}], but it was: [{lst}]' \
            .format(lst=compared_list,
                    operator=compare.__name__)
    else:
        assert is_sorted is True, \
            'Expected list would be sorted as [{operator}], but it was not: [{lst}]' \
                .format(lst=compared_list,
                        operator=compare.__name__)

    return True
