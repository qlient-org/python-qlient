""" This file contains the graphql client

:author: Daniel Seifert
:created: 09.09.2021
"""
import logging
from typing import Optional, Union

from qlient.backend import Backend, HTTPBackend
from qlient.cache import Cache
from qlient.proxy import QueryService, MutationService
from qlient.schema.providers import BackendSchemaProvider
from qlient.schema.schema import Schema
from qlient.settings import Settings

logger = logging.getLogger("qlient")


class Client:
    """ This class represents the base qlient Client. """

    def __init__(
            self,
            backend: Union[str, Backend],
            schema: Optional[Schema] = None,
            settings: Optional[Settings] = None,
            cache: Optional[Cache] = None,
    ):
        self.settings: Settings = settings or Settings()

        if isinstance(backend, str):
            backend = HTTPBackend(backend)
        if not isinstance(backend, Backend):
            raise TypeError(f"backend must be of type `{Backend.__name__}`")

        self.backend: Backend = backend
        self.cache: Optional[Cache] = cache

        if schema is None:
            provider = BackendSchemaProvider(self.backend, introspect=self.settings.introspect)
            schema = Schema(provider, settings=self.settings, cache=self.cache)
        if not isinstance(schema, Schema):
            raise TypeError(f"Schem must be of type `{Schema.__name__}`")

        self.schema: Schema = schema

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
        return f"{class_name}(backend=`{self.backend}`)"

    def __repr__(self) -> str:
        """ Return a detailed string representation of the client """
        class_name = self.__class__.__name__
        props = ", ".join([
            f"endpoint=`{self.backend}`",
            f"settings={self.settings}",
            f"cache={self.cache}",
            f"schema={self.schema}"
        ])
        return f"<{class_name}({props})>"
