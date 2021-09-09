""" 

:author: Daniel Seifert
:created: 09.09.2021
:copyright: Swisscom
"""
from typing import Optional

from qlient.cache import Cache
from qlient.settings import Settings
from qlient.transport import Transport


class Client:
    """ This class represents the base qlient Client.

    """

    def __init__(
            self,
            endpoint: str,
            ws_endpoint: Optional[str] = None,
            transport: Optional[Transport] = None,
            settings: Optional[Settings] = None,
            cache: Optional[Cache] = None
    ):
        pass
