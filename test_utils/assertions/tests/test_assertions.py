from . import *  # import common imports from __init__

from sure import expect, ensure
from test_utils.assertions.assertions_request import *

from dateutil.tz import tzoffset
import allure
import datetime


@allure.feature('framework assertions')
@allure.story('assertion extract')
class TestExtract:
    def test_extract_elem_by_one_field(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).extract({"a": 1}).should.be.equal({"a": 1, "b": 2, "c": 3})

    def test_extract_elem_by_two_fields(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).extract({"a": 1, "b": 2}).should.be.equal({"a": 1, "b": 2, "c": 3})

    def test_extract_elem_from_middle_array(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"l": 10, "m": 20, "n": 30},
                  {"x": 50, "y": 60, "z": 70}]

        expect(result).extract({"l": 10}).should.be.equal({"l": 10, "m": 20, "n": 30})

    def test_extract_elem_by_mismatch_key_field(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).extract.when.called_with({"F": 77}).should.have.raised(AssertionError)

    def test_extract_elem_by_mismatch_value(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).extract.when.called_with({"a": 77}).should.have.raised(AssertionError)

    def test_extract_elem_with_dict_inside(self):
        result = [{"a": 1, "b": {"l": 4, "m": 5}, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).extract({"b": {"l": 4, "m": 5}}).should.be.equal({"a": 1, "b": {"l": 4, "m": 5}, "c": 3})

    def test_extract_elem_with_dict_inside_partial_matching(self):
        result = [{"a": 1, "b": {"l": 4, "m": 5}, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).extract({"b": {"m": 5}}).should.be.equal({"a": 1, "b": {"l": 4, "m": 5}, "c": 3})

    def test_matched_float_values(self):
        result = [{"a": 1, "x": 10.0},
                  {"b": 2},
                  {"c": 3},
                  {"a": 1, "y": 20},
                  {"a": 1, "z": 30}]

        expect(result).extract({'a': 1, 'x': 10.0}).should.have.equal({"a": 1, "x": 10.0})

    def test_not_matched_float_values(self):
        result = [{"a": 1, "x": 10.0},
                  {"b": 2},
                  {"c": 3},
                  {"a": 1, "y": 20},
                  {"a": 1, "z": 30}]

        expect(result).extract.when.called_with({'a': 1, 'x': 15.0}).should.have.raised(AssertionError)


@allure.feature('framework assertions')
@allure.story('assertion filter')
class TestFilter:
    def test_dict_full_match(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).should.have.length_of(2)
        expect(result).filter({"a": 1, "b": 2, "c": 3}).should.have.length_of(1)
        expect(result).filter({"a": 1, "b": 2, "c": 3}).should.have.equal([{"a": 1, "b": 2, "c": 3}])

    def test_dict_partial_match(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).should.have.length_of(2)
        expect(result).filter({"b": 2, "c": 3}).should.have.length_of(1)
        expect(result).filter({"b": 2, "c": 3}).should.have.equal([{"a": 1, "b": 2, "c": 3}])

    def test_filter_first_element(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).should.have.length_of(2)
        expect(result).filter({'a': 1}).should.have.length_of(1)
        expect(result).filter({'a': 1}).should.have.equal([{"a": 1, "b": 2, "c": 3}])

    def test_filter_middle_element(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"l": 10, "m": 20, "n": 30},
                  {"x": 50, "y": 60, "z": 70}]

        expect(result).filter({'m': 20}).should.have.length_of(1)
        expect(result).filter({'m': 20}).should.have.equal([{"l": 10, "m": 20, "n": 30}])

    def test_filter_last_element(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"l": 10, "m": 20, "n": 30},
                  {"x": 50, "y": 60, "z": 70}]

        expect(result).filter({'z': 70}).should.have.length_of(1)
        expect(result).filter({'z': 70}).should.have.equal([{"x": 50, "y": 60, "z": 70}])

    def test_match_few_elements(self):
        result = [{"a": 1, "x": 10},
                  {"b": 2},
                  {"c": 3},
                  {"a": 1, "y": 20},
                  {"a": 1, "z": 30}]

        expect(result).filter({'a': 1}).should.have.length_of(3)
        expect(result).filter({'a': 1}).should.have.equal([{'a': 1, 'x': 10}, {'a': 1, 'y': 20}, {'a': 1, 'z': 30}])

    def test_have_no_key_match(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).filter({'mmm': 1}).should.have.length_of(0)
        expect(result).filter({'mmm': 1}).should.have.equal([])

    def test_have_no_value_match(self):
        result = [{"a": 1, "b": 2, "c": 3},
                  {"x": 5, "y": 6, "z": 7}]

        expect(result).filter({'a': 10}).should.have.length_of(0)
        expect(result).filter({'a': 10}).should.have.equal([])

    def test_matched_float_values(self):
        result = [{"a": 1, "x": 10.0},
                  {"b": 2},
                  {"c": 3},
                  {"a": 1, "y": 20},
                  {"a": 1, "z": 30}]

        expect(result).filter({'a': 1, 'x': 10.0}).should.have.length_of(1)
        expect(result).filter({'a': 1, 'x': 10.0}).should.have.equal([{"a": 1, "x": 10.0}])

    def test_not_matched_float_values(self):
        result = [{"a": 1, "x": 10.0},
                  {"b": 2},
                  {"c": 3},
                  {"a": 1, "y": 20},
                  {"a": 1, "z": 30}]

        expect(result).filter({'a': 1, 'x': 15.0}).should.have.length_of(0)
        expect(result).filter({'a': 1, 'x': 15.0}).should.have.equal([])


@allure.feature('framework assertions')
@allure.story('assertion almost_equal: datetime format')
class TestAlmostEqual:
    test_now_datetime = datetime.datetime(2017, 3, 30, 20, 0, 5, 1234, tzinfo=tzoffset(None, 10800))

    def test_dates_are_equal(self):
        result = '2017-03-30 20:00:05.001234+03:00'
        expect(result).should.be.almost_equal(self.test_now_datetime)

    def test_source_less_than_expected(self):
        result = '2017-03-30 20:00:05.001234+03:00'
        expect(result).should.be.almost_equal(self.test_now_datetime + datetime.timedelta(seconds=+5))

    def test_source_grater_than_expected(self):
        result = '2017-03-30 20:00:05.001234+03:00'
        expect(result).should.be.almost_equal(self.test_now_datetime + datetime.timedelta(seconds=-5))

    def test_difference_large_than_acceptable_delta(self):
        result = '2017-03-30 20:00:05.001234+03:00'
        expect(result).almost_equal.when.called_with(self.test_now_datetime + datetime.timedelta(seconds=+11),
                                                     acceptable_delta_sec=10).should.have.raised(AssertionError)

    def test_different_timezones(self):
        actual = '2017-03-30T18:00:05.492391+01:00'
        expected = datetime.datetime(2017, 3, 30, 20, 0, 5, 1234, tzinfo=tzoffset(None, 10800))  # +3
        expect(actual).should.be.almost_equal(expected)


@allure.feature('framework assertions')
@allure.story('assertion almost_equal: unix format')
class TestAlmostEqualUnixEpochFormat:
    test_now_datetime = 1504699386507  # '2017-09-06 12:03:06.507000'

    def test_dates_are_equal(self):
        result = self.test_now_datetime
        expect(result).should.be.almost_equal(self.test_now_datetime)

    def test_source_less_than_expected(self):
        result = self.test_now_datetime
        expect(result).should.be.almost_equal(self.test_now_datetime + 5 * 1000)  # ms

    def test_source_grater_than_expected(self):
        result = self.test_now_datetime
        expect(result).should.be.almost_equal(self.test_now_datetime - 5 * 1000)  # ms

    def test_difference_large_than_acceptable_delta(self):
        result = self.test_now_datetime
        expect(result).almost_equal.when.called_with(self.test_now_datetime + 11 * 1000,  # ms
                                                     acceptable_delta_sec=10).should.have.raised(AssertionError)


@allure.feature('framework assertions')
@allure.story('assertion almost_equal: mixed format')
class TestAlmostEqualMixedDates:
    test_now_datetime = datetime.datetime(2017, 9, 30, 20, 0, 5, 1234, tzinfo=tzoffset(None, 10800))

    def test_dates_are_equal(self):
        result = 1506790805001  # '2017-09-30 17:00:05.001000' UTC
        expect(result).should.be.almost_equal(self.test_now_datetime)

    def test_source_less_than_expected(self):
        result = 1506790805001  # '2017-09-30 17:00:05.001000' UTC
        expect(result).should.be.almost_equal(self.test_now_datetime + datetime.timedelta(seconds=+5))

    def test_source_grater_than_expected(self):
        result = 1506790805001  # '2017-09-30 17:00:05.001000' UTC
        expect(result).should.be.almost_equal(self.test_now_datetime + datetime.timedelta(seconds=-5))

    def test_difference_large_than_acceptable_delta(self):
        result = 1506790805001  # '2017-09-30 17:00:05.001000' UTC
        expect(result).almost_equal.when.called_with(self.test_now_datetime + datetime.timedelta(seconds=+11),
                                                     acceptable_delta_sec=10).should.have.raised(AssertionError)


class TestSorted:
    def test_positive_ge(self):
        lst = [3, 3, 2, 1]
        lst.should.be.sorted_by(compare=operator.ge)

    def test_negative_ge(self):
        lst = [1, 3, 3, 2, 1]
        expect(lst).sorted_by.when.called_with(compare=operator.ge).should.have.raised(AssertionError)

    def test_positive_le(self):
        lst = [1, 2, 3, 3, 4]
        lst.should.be.sorted_by(compare=operator.le)

    def test_negative_le(self):
        lst = [1, 3, 3, 2]
        expect(lst).sorted_by.when.called_with(compare=operator.le).should.have.raised(AssertionError)

    def test_negative_le_opposite(self):
        lst = [1, 3, 3, 2]
        lst.should_not.be.sorted_by(compare=operator.le)

    def test_negative_ge_opposite(self):
        lst = [3, 2, 1, 1, 4]
        lst.should_not.be.sorted_by(compare=operator.ge)

    def test_positive_le_dicts(self):
        lst = [{'id': 1, 'b': 'abc'},
               {'id': 2, 'b': 'dbe'},
               {'id': 3, 'c': 'xyz'}, ]

        lst.should.be.sorted_by(compare=operator.le, key=lambda x: x['id'])

    def test_positive_le_dicts_negative(self):
        lst = [{'id': 1, 'b': 'abc'},
               {'id': 3, 'c': 'xyz'},
               {'id': 2, 'b': 'dbe'}, ]

        expect(lst).sorted_by.when.called_with(compare=operator.le, key=lambda x: x['id']).should.have.raised(AssertionError)

    def test_positive_ge_dicts(self):
        lst = [{'id': 3, 'c': 'xyz'},
               {'id': 2, 'b': 'dbe'},
               {'id': 1, 'b': 'abc'}, ]

        lst.should.be.sorted_by(compare=operator.ge, key=lambda x: x['id'])

    def test_positive_ge_dicts_negative(self):
        lst = [{'id': 1, 'b': 'abc'},
               {'id': 3, 'c': 'xyz'},
               {'id': 2, 'b': 'dbe'}, ]

        expect(lst).sorted_by.when.called_with(compare=operator.ge, key=lambda x: x['id']).should.have.raised(AssertionError)
