"""This file contains the different qlient backends"""
import abc
import logging
import multiprocessing
from typing import Optional

import requests
import websocket

from qlient import __meta__, Settings
from qlient.types import (
    GraphQLVariables,
    GraphQLQuery,
    GraphQLOperation,
    GraphQLReturnType,
    GraphQLReturnTypeIterator,
    GraphQLContext,
    GraphQLRoot,
)
from qlient.utils import convert_to_websocket_url

logger = logging.getLogger(__meta__.__title__)


class Backend(abc.ABC):
    """Abstract base class for all graphql backend.

    In order to create your own custom graphql backend you must overwrite the `execute_query`
    method down below.

    This is useful in cases where your backend is not reachable via http.
    """

    def __init__(
            self,
            settings: Optional[Settings] = None,
    ):
        self.settings: Settings = settings or Settings()

    @abc.abstractmethod
    def execute_query(
            self,
            query: GraphQLQuery,
            variables: GraphQLVariables = None,
            operation_name: GraphQLOperation = None,
            context: GraphQLContext = None,
            root: GraphQLRoot = None,
    ) -> GraphQLReturnType:
        """Abstract method to execute a query statement on this backend.

        Args:
            query: holds the graphql query
            variables: optional, holds variables that are mentioned in the query
            operation_name: optional, holds the name of this specific operation
            context: optional, holds a graphql context
            root: optional, holds a root value for this query

        Returns:
            the query result of the graphql backend
        """
        raise NotImplementedError

    def execute_mutation(
            self,
            query: GraphQLQuery,
            variables: GraphQLVariables = None,
            operation_name: GraphQLOperation = None,
            context: GraphQLContext = None,
            root: GraphQLRoot = None,
    ) -> GraphQLReturnType:
        """Method to execute a mutation statement on this backend

        In most cases, the mutation has the same implementation as the query.
        Therefore, this method will forward the call by default.

        To change this behaviour, you must create your own
        custom Backend.

        Args:
            query: holds the graphql query
            variables: optional, holds variables that are mentioned in the query
            operation_name: optional, holds the name of this specific operation
            context: optional, holds a graphql context
            root: optional, holds a root value for this query

        Returns:
            the mutation result of the graphql backend
        """
        return self.execute_query(query, variables, operation_name, context, root)

    @abc.abstractmethod
    def execute_subscription(
            self,
            query: GraphQLQuery,
            variables: GraphQLVariables = None,
            operation_name: GraphQLOperation = None,
            context: GraphQLContext = None,
            root: GraphQLRoot = None,
    ) -> GraphQLReturnTypeIterator:
        """Abstract method to execute a subscription statement on this backend

        Args:
            query: holds the graphql query
            variables: optional, holds variables that are mentioned in the query
            operation_name: optional, holds the name of this specific operation
            context: optional, holds a graphql context
            root: optional, holds a root value for this query

        Returns:
            a generator that yields incoming messages
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def cache_key(self) -> str:
        """A key that uniquely identifies the schema for a specific backend

        For example this can be a unique url or hostname.
        Or even a static key if the schema remains the same for the backend.

        This cache key is required for the BackendSchemaProvider.

        Returns:
            a string that uniquely identifies the schema
        """
        raise NotImplementedError


class HTTPBackend(Backend):
    """A backend implementation that communicates with a http server.

    The HTTPBackend uses pythons requests package under the hood for making requests.
    """

    def __init__(
            self,
            endpoint: str,
            ws_endpoint: Optional[str] = None,
            session: Optional[requests.Session] = None,
            raise_for_status: bool = False,
            settings: Optional[Settings] = None
    ):
        super(HTTPBackend, self).__init__(settings=settings)
        if ws_endpoint is None:
            ws_endpoint = convert_to_websocket_url(endpoint)
        self.endpoint: str = endpoint
        self.ws_endpoint: str = ws_endpoint
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
        """Send a query to the http graphql backend

        Args:
            query: holds the query
            variables: holds variables that should be sent with in the query
            operation_name: holds the name of the operation
            context: ignored in http
            root: ignored in http

        Returns:
            the response parsed as dictionary
        """
        logger.info(f"Sending operation `{operation_name}` to `{self.endpoint}`")
        logger.debug(f"Query: {query}")
        logger.debug(f"Variables: {variables}")
        response = self.session.post(
            self.endpoint,
            json={
                "query": query,
                "operationName": operation_name,
                "variables": variables,
            },
        )
        if self.raise_for_status:
            response.raise_for_status()
        return self.settings.json_loads(response.text)

    def execute_subscription(
            self,
            query: GraphQLQuery,
            variables: GraphQLVariables = None,
            operation_name: GraphQLOperation = None,
            context: GraphQLContext = None,
            root: GraphQLRoot = None,
    ) -> GraphQLReturnTypeIterator:
        """Send a subscription query to the web server and listen to messages.



        Args:
            query:
            variables:
            operation_name:
            context:
            root:

        Returns:

        """
        message_queue = multiprocessing.Queue()

        def on_message_wrapper(_, message: str):
            """

            Args:
                _:
                message:

            Returns:

            """
            message_queue.put(self.settings.json_loads(message))

        socket = websocket.WebSocketApp(
            self.ws_endpoint,
            subprotocols=["graphql-ws"],
            on_message=on_message_wrapper
        )
        socket.run_forever()

        return GraphQLReturnTypeIterator(message_queue)

    @property
    def cache_key(self) -> str:
        """The http backend uses the http server uri as the unique cache key.

        Returns:
            the endpoint where the graphql server is running.
        """
        return self.endpoint

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"<{class_name}(endpoint=`{self.endpoint}`, ws_endpoint=`{self.ws_endpoint}`, raise_for_status={self.raise_for_status})>"
