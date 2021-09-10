""" 

:author: Daniel Seifert
:created: 09.09.2021
:copyright: Swisscom
"""
import logging
from typing import Optional

from qlient import validators, __about__
from qlient.cache import Cache
from qlient.schema import Schema
from qlient.settings import Settings
from qlient.transport import Transport


class Client:
    """ This class represents the base qlient Client.

    """

    logger = logging.getLogger(__about__.__title__)

    _default_transport = Transport  # holds the default transport factory
    _default_settings = Settings  # holds the default settings factory

    def __init__(
            self,
            endpoint: str,
            transport: Optional[Transport] = None,
            settings: Optional[Settings] = None,
            cache: Optional[Cache] = None
    ):
        if not validators.is_url(endpoint):
            raise ValueError("Parameter `endpoint` must be a URL.")
        self.endpoint: str = endpoint
        self.settings: Settings = settings or self._default_settings()
        self.transport: Transport = transport or self._default_transport(self.endpoint)
        self.cache: Optional[Cache] = cache
        self.schema: Schema = Schema(self.endpoint, transport=self.transport, settings=self.settings, cache=self.cache)
