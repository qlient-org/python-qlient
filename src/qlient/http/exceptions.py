"""This module contains all qlient.http related exceptions"""
from qlient.core.exceptions import QlientException


class SubscriptionException(QlientException):
    """Base class for all subscription related exceptions"""


class ConnectionRejected(SubscriptionException):
    """Indicates that the server did not acknowledge (rejected) the connection"""
