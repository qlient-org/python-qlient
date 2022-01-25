""" This file contains the different transports

:author: Daniel Seifert
:created: 09.09.2021
"""
import abc
import logging
from typing import Optional

import requests

from qlient.types import (
    GraphQLVariables,
    GraphQLQuery,
    GraphQLOperation,
    GraphQLReturnType,
    GraphQLContext,
    GraphQLRoot
)

logger = logging.getLogger("qlient")


class Backend(abc.ABC):

    @abc.abstractmethod
    def execute_query(
            self,
            query: GraphQLQuery,
            variables: GraphQLVariables = None,
            operation_name: GraphQLOperation = None,
            context: GraphQLContext = None,
            root: GraphQLRoot = None,
    ) -> GraphQLReturnType:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def cache_key(self) -> str:
        """ A key that uniquely identifies the schema for a specific backend

        For example this can be a unique url or hostname.
        Or even a static key if the schema remains the same for the backend.

        This cache key is required for the BackendSchemaProvider.

        :return: a string that uniquely identifies the schema
        """
        raise NotImplementedError


class HTTPBackend(Backend):

    def __init__(
            self,
            endpoint: str,
            session: Optional[requests.Session] = None,
            raise_for_status: bool = False
    ):
        self.endpoint: str = endpoint
        self.session: requests.Session = session or requests.Session()
        self.raise_for_status: bool = raise_for_status

    def execute_query(
            self,
            query: GraphQLQuery,
            variables: GraphQLVariables = None,
            operation_name: GraphQLOperation = None,
            context: GraphQLContext = None,
            root: GraphQLRoot = None,
    ) -> GraphQLReturnType:
        """ Send a query to the graphql endpoint

        :param query: holds the query
        :param variables: holds variables that should be sent with in the query
        :param operation_name: holds the name of the operation
        :param context: ignored in http
        :param root: ignored in http
        :return: the response parsed as dictionary
        """
        logger.info(f"Sending operation `{operation_name}` to `{self.endpoint}`")
        logger.debug(f"Query: {query}")
        logger.debug(f"Variables: {variables}")
        response = self.session.post(
            self.endpoint,
            json={
                "query": query,
                "operationName": operation_name,
                "variables": variables
            }
        )
        if self.raise_for_status:
            response.raise_for_status()
        return response.json()

    @property
    def cache_key(self) -> str:
        return self.endpoint

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"<{class_name}(endpoint=`{self.endpoint}`, raise_for_status={self.raise_for_status})>"
