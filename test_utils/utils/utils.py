import uuid
import random
import string

from datetime import datetime, timedelta, timezone
import time
import pytz

import allure
import logging

from test_utils.assertions.constants import AssertionStatus

logger = logging.getLogger(__name__)


def uniq_int(bytes=4):
    return uuid.uuid4().int & (1 << 2 ** bytes) - 1


def generate_uniq_name(prefix=""):
    return "{prefix}{name}".format(prefix=prefix, name=str(uuid.uuid4()).replace("-", ""))


def generate_email(domain="mustapp.test.me"):
    return "{login}@{domain}".format(login=uuid.uuid4(), domain=domain)


def generate_password(length=8):
    return "".join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for i in range(length))


def generate_apns_device_token():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=64))


def generate_phone_number(country_code='+6'):
    return "{country_code}{timestamp}".format(country_code=country_code, timestamp=dt_to_ms(datetime.now()))


def generate_uniq_imdb_id(prefix="ttxxx1"):
    return "{prefix}{timestamp}".format(prefix=prefix, timestamp=(time.time() * 1000))


def todict(obj, include_class_attrs=False, convert_private=False, include_none_fields=True):
    """Convert object to dict"""
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, include_class_attrs, convert_private)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast(), convert_private=convert_private)
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, include_class_attrs, convert_private) for v in obj]
    elif hasattr(obj, "__dict__"):
        if convert_private:
            instance_attributes = [(key, value) for key, value in obj.__dict__.items() if not callable(value)]
        else:
            instance_attributes = [(key, value) for key, value in obj.__dict__.items() if not callable(value) and not key.startswith('_')]

        if include_class_attrs and hasattr(obj, "__class__"):
            class_attributes = [(key, value) for key, value in obj.__class__.__dict__.items() if (key[:2] != "__") and (not callable(value))]
        else:
            class_attributes = []

        items = instance_attributes
        items.extend(class_attributes)

        # if include_none_fields or value: for include or exclude none fields
        data = dict([(key, todict(value, include_class_attrs, convert_private, include_none_fields)) for key, value in items if
                     include_none_fields or (value is not None and value != [] and value != "")])

        return data
    else:
        return obj


def is_string_belong_language(string, language):
    # trim all special chars
    str_trimed = ''.join(e for e in string if e.isalpha())

    if len(str_trimed) == 0:
        return True

    res = ''.join(e for e in str_trimed if (e not in language))

    # if string less then 35%
    return True if len(res) * 100.0 / len(str_trimed) < 35.0 else False


def skip_test_if_true(expression, message, status=AssertionStatus.CANCELED):
    import pytest

    if expression:
        if status == AssertionStatus.PENDING:
            pytest.xfail(message)
        elif status == AssertionStatus.CANCELED:
            pytest.skip(message)


def dt_from_ms(ms):
    # utcfromtimestamp will return utc time but with tzinfo=None, which means it is at local timezone, so replace it to utc explicit
    return datetime.utcfromtimestamp(ms / 1000.0).replace(tzinfo=pytz.UTC)


def dt_to_ms(dt):
    delta = dt.astimezone(pytz.UTC) - datetime.utcfromtimestamp(0).astimezone(pytz.UTC)
    return int(delta.total_seconds() * 1000)


def print_request_as_curl(req):
    command = """curl -iL -X {method} \\\n -H {headers} \\\n -d '{data}' \\\n '{uri}'\n"""
    method = req.method
    uri = req.url
    data = req.body if req.body else ""
    req_headers = req.headers.copy()

    if isinstance(data, type(b'')):
        data = ".... <binary data> ...."

    if data:
        data = data.replace("'", '"')
        # limit data output
        limit_len = 500
        if len(data) > limit_len:
            data = data[:limit_len] + ".... artificial truncated (data to long for print: len={len} chars) ...".format(len=len(data))
    if 'Accept-Encoding' in req_headers:
        # for pretty human print in console
        del req_headers['Accept-Encoding']
    if 'Content-Length' in req_headers:
        del req_headers['Content-Length']

    headers = ['"{0}: {1}"'.format(k, v if v else "") for k, v in req_headers.items()]
    headers = " \\\n -H ".join(headers)

    return command.format(method=method, headers=headers, data=data, uri=uri)


def log_response(path, response):
    print_text = True
    if 'Content-Type' in response.headers:
        if "image" in response.headers.get('Content-Type'):
            print_text = False

    # adjust log format
    if len(response.history) > 0:
        initial_request = response.history[0].request
    else:
        initial_request = response.request

    log_format_request = "\n[request %s]: \n\t%s" % (path, print_request_as_curl(initial_request))
    log_format_status_code = "\t[response code]: \n\t%s\n" % response.status_code
    log_format_headers = "\t[response headers]: \n\t%s\n" % response.headers
    log_format_text = "\t[response text]: \n\t%s\n" % (response.text if print_text else "<<omitted by test handlers>>")

    log = "{request}\n{response_code}\n{response_headers}\n{response_text}".format(request=log_format_request,
                                                                                   response_code=log_format_status_code,
                                                                                   response_headers=log_format_headers,
                                                                                   response_text=log_format_text)
    logger.info(log)

    try:
        # if ENV != Environment.PROD:
        #     # for monitoring test purposes
        allure.attach('request debug log', "\n[request %s]: \n%s\n\n[status]: \n%s\n[headers]: \n%s\n[text]: \n%s" %
                      (path,
                       print_request_as_curl(initial_request),
                       response.status_code,
                       response.headers,
                       response.text if print_text else "<<omitted by test handlers>>"))

    except AttributeError as e:
        # workaround for AllureTestListener not initialized during call parametrized fixtures before tests
        pass
