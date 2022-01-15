""" This file contains the graphql client

:author: Daniel Seifert
:created: 09.09.2021
"""
import logging
from typing import Optional

from qlient import validators
from qlient.cache import Cache
from qlient.proxy import QueryService, MutationService
from qlient.schema import Schema
from qlient.settings import Settings
from qlient.transport import Transport


class Client:
    """ This class represents the base qlient Client.

    """

    logger = logging.getLogger("qlient")

    _default_transport = Transport  # holds the default transport factory
    _default_settings = Settings  # holds the default settings factory

    def __init__(
            self,
            endpoint: str,
            schema: Optional[Schema] = None,
            transport: Optional[Transport] = None,
            settings: Optional[Settings] = None,
            cache: Optional[Cache] = None,
    ):
        self.settings: Settings = settings or self._default_settings()
        if self.settings.validate_url:
            if not validators.is_url(endpoint):
                raise ValueError("Parameter `endpoint` must be a URL.")
        self.endpoint: str = endpoint
        self.transport: Transport = transport or self._default_transport()
        self.cache: Optional[Cache] = cache
        self.schema: Schema = schema or Schema(self.endpoint, self.transport, self.settings, self.cache)

        self._query_service: Optional[QueryService] = None
        self._mutation_service: Optional[MutationService] = None

    @property
    def query(self) -> QueryService:
        """ Cached property for the query service

        If the :ref:`_query_service` is None, create a new QueryService.

        :return: the query service in use
        """
        if self._query_service is None:
            self._query_service = QueryService(self)
        return self._query_service

    @property
    def mutation(self) -> MutationService:
        """ Cached property for the mutation service

        if the ref:`_mutation_service` is None, create a new MutationService.

        :return: the mutation service to use
        """
        if self._mutation_service is None:
            self._mutation_service = MutationService(self)
        return self._mutation_service

    def __str__(self) -> str:
        """ Return a simple string representation of the client """
        class_name = self.__class__.__name__
        return f"{class_name}(endpoint=`{self.endpoint}`)"

    def __repr__(self) -> str:
        """ Return a detailed string representation of the client """
        class_name = self.__class__.__name__
        props = ", ".join([
            f"endpoint=`{self.endpoint}`",
            f"settings={self.settings}",
            f"transport={self.transport}",
            f"cache={self.cache}",
            f"schema={self.schema}"
        ])
        return f"<{class_name}({props})>"
