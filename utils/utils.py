import uuid
import random
import string

from datetime import datetime, timedelta, timezone
import time
import pytz

from assertions.constants import AssertionStatus


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
