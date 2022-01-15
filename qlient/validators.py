""" This file contains the validators

URL Validator:
- https://github.com/kvesteri/validators/blob/master/validators/url.py

:author: Daniel Seifert
:created: 10.09.2021
"""
import re

IP_MIDDLE_OCTET = r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
IP_LAST_OCTET = r"(?:\.(?:0|[1-9]\d?|1\d\d|2[0-4]\d|25[0-5]))"

URL_PATTERN = re.compile(  # noqa: W605
    "".join([  # formatter messes up everything when using string concatenation
        r"^",
        # protocol identifier,
        r"(?:(?:https?|ftp)://)",
        # user:pass authentication,
        r"(?:[-a-z\u00a1-\uffff0-9._~%!$&'()*+,;=:]+",
        r"(?::[-a-z0-9._~%!$&'()*+,;=:]*)?@)?",
        r"(?:",
        r"(?P<private_ip>",
        # IP address exclusion,
        # private & local networks,
        r"(?:(?:10|127)" + IP_MIDDLE_OCTET + r"{2}" + IP_LAST_OCTET + r")|",
        r"(?:(?:169\.254|192\.168)" + IP_MIDDLE_OCTET + IP_LAST_OCTET + r")|",
        r"(?:172\.(?:1[6-9]|2\d|3[0-1])" + IP_MIDDLE_OCTET + IP_LAST_OCTET + r"))",
        r"|",
        # private & local hosts,
        r"(?P<private_host>",
        r"(?:localhost))",
        r"|",
        # IP address dotted notation octets,
        # excludes loopback network 0.0.0.0,
        # excludes reserved space >= 224.0.0.0,
        # excludes network & broadcast addresses,
        # (first & last IP address of each class),
        r"(?P<public_ip>",
        r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])",
        r"" + IP_MIDDLE_OCTET + r"{2}",
        r"" + IP_LAST_OCTET + r")",
        r"|",
        # IPv6 RegEx from https://stackoverflow.com/a/17871737,
        r"\[(",
        # 1:2:3:4:5:6:7:8,
        r"([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|",
        # 1::                              1:2:3:4:5:6:7::,
        r"([0-9a-fA-F]{1,4}:){1,7}:|",
        # 1::8             1:2:3:4:5:6::8  1:2:3:4:5:6::8,
        r"([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|",
        # 1::7:8           1:2:3:4:5::7:8  1:2:3:4:5::8,
        r"([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|",
        # 1::6:7:8         1:2:3:4::6:7:8  1:2:3:4::8,
        r"([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|",
        # 1::5:6:7:8       1:2:3::5:6:7:8  1:2:3::8,
        r"([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|",
        # 1::4:5:6:7:8     1:2::4:5:6:7:8  1:2::8,
        r"([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|",
        # 1::3:4:5:6:7:8   1::3:4:5:6:7:8  1::8,
        r"[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|",
        # ::2:3:4:5:6:7:8  ::2:3:4:5:6:7:8 ::8       ::,
        r":((:[0-9a-fA-F]{1,4}){1,7}|:)|",
        # fe80::7:8%eth0   fe80::7:8%1,
        # (link-local IPv6 addresses with zone index),
        r"fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|",
        r"::(ffff(:0{1,4}){0,1}:){0,1}",
        r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}",
        # ::255.255.255.255   ::ffff:255.255.255.255  ::ffff:0:255.255.255.255,
        # (IPv4-mapped IPv6 addresses and IPv4-translated addresses),
        r"(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|",
        r"([0-9a-fA-F]{1,4}:){1,4}:",
        r"((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}",
        # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33,
        # (IPv4-Embedded IPv6 Address),
        r"(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])",
        r")\]|",
        # host name,
        r"(?:(?:(?:xn--)|[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]-?)*",
        r"[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]+)",
        # domain name,
        r"(?:\.(?:(?:xn--)|[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]-?)*",
        r"[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]+)*",
        # TLD identifier,
        r"(?:\.(?:(?:xn--[a-z\u00a1-\uffff\U00010000-\U0010ffff0-9]{2,})|",
        r"[a-z\u00a1-\uffff\U00010000-\U0010ffff]{2,}))",
        r")",
        # port number,
        r"(?::\d{2,5})?",
        # resource path,
        r"(?:/[-a-z\u00a1-\uffff\U00010000-\U0010ffff0-9._~%!$&'()*+,;=:@/]*)?",
        # query string,
        r"(?:\?\S*)?",
        # fragment,
        r"(?:#\S*)?",
        r"$",
    ]),
    re.UNICODE | re.IGNORECASE
)


def is_url(value: str) -> bool:
    """ Validate whether any given value is a valid domain

    :param value: holds the value to check
    :return: True if the given value matches the domain pattern defined at the top
    """
    if value is None:
        return False
    return bool(URL_PATTERN.match(value))


def is_local_path(location: str) -> bool:
    """ Check if the given location is a local path

    :param location: holds the location of the schema definition
    :return: True if the schema is a local path
    """
    import pathlib
    try:
        return pathlib.Path(location).exists()
    except OSError:
        # when something goes wrong, the location is most likely not a local file
        return False
