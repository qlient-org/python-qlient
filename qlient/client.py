""" 

:author: Daniel Seifert
:created: 09.09.2021
:copyright: Swisscom
"""
import logging
from typing import Optional

from qlient import validators, __about__
from qlient.cache import Cache
from qlient.proxy import QueryService, MutationService
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
            schema: Optional[Schema] = None,
            transport: Optional[Transport] = None,
            settings: Optional[Settings] = None,
            cache: Optional[Cache] = None
    ):
        if not validators.is_url(endpoint):
            raise ValueError("Parameter `endpoint` must be a URL.")
        self.endpoint: str = endpoint
        self.settings: Settings = settings or self._default_settings()
        self.transport: Transport = transport or self._default_transport()
        self.cache: Optional[Cache] = cache
        self.schema: Schema = schema or Schema(self.endpoint, self.transport, self.settings, self.cache)

        self._query_service: Optional[QueryService] = None
        self._mutation_service: Optional[MutationService] = None

    @property
    def query(self) -> QueryService:
        if self._query_service is None:
            self._query_service = QueryService(self)
        return self._query_service

    @property
    def mutation(self) -> MutationService:
        if self._mutation_service is None:
            self._mutation_service = MutationService(self)
        return self._mutation_service
