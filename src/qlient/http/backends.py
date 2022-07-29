"""This module contains the http backend"""
import logging
import uuid
from typing import Dict, Any
from urllib.parse import urlparse, urlunparse, ParseResult

import qlient.core.__meta__
import requests
import websocket
from qlient.core import (
    Backend,
    GraphQLSubscriptionRequest,
    GraphQLResponse,
    GraphQLRequest,
)

from qlient.http.consts import (
    GRAPHQL_WS_PROTOCOL,
    GRAPHQL_TRANSPORT_WS_PROTOCOL,
    CONNECTION_INIT,
    CONNECTION_ACKNOWLEDGED,
    START,
)
from qlient.http.exceptions import ConnectionRejected
from qlient.http.models import GraphQLSubscriptionResponse
from qlient.http.settings import HTTPSettings

logger = logging.getLogger(qlient.core.__meta__.__title__)


class HTTPBackend(Backend):
    """The HTTPBackend

    Examples:
        >>> backend = HTTPBackend("https://swapi-graphql.netlify.app/.netlify/functions/index")
        >>> result = backend.execute_query(...)
    """

    @staticmethod
    def adapt_ws_endpoint(endpoint: str) -> str:
        """Adapt the normal http endpoint to a websocket endpoint

        Args:
            endpoint: holds the http endpoint. (e.g. "http[s]://...")

        Returns:
            a websocket url. (e.g. "ws[s]://...")
        """
        pr: ParseResult = urlparse(endpoint)
        if pr.scheme == "http":
            pr = pr._replace(scheme="ws")
        if pr.scheme == "https":
            pr = pr._replace(scheme="wss")
        return urlunparse(pr)

    @classmethod
    def generate_subscription_id(cls) -> str:
        """Class method to generate unique subscription ids

        Returns:
            A unique subscription id
        """
        return f"qlient:{cls.__name__}:{uuid.uuid4()}".replace("-", "")

    @staticmethod
    def make_payload(request: GraphQLRequest) -> Dict[str, Any]:
        """Static method for generating the request payload

        Args:
            request: holds the graphql request

        Returns:
            the payload to send as dictionary
        """
        return {
            "query": request.query,
            "operationName": request.operation_name,
            "variables": request.variables,
        }

    def __init__(
        self,
        endpoint: str,
        ws_endpoint: str = None,
        session: requests.Session = None,
        settings: HTTPSettings = None,
    ):
        if settings is None:
            settings = HTTPSettings()

        if session is None:
            session = requests.Session()

        self.settings: HTTPSettings = settings
        self.endpoint: str = endpoint
        self.ws_endpoint: str = ws_endpoint or self.adapt_ws_endpoint(self.endpoint)
        self.session: requests.Session = session

    def execute_query(self, request: GraphQLRequest) -> GraphQLResponse:
        """Method to execute a query on the http server.

        First the request is transformed to a payload.
        >>> {
        >>>     "query": "query X { X { ... } }",
        >>>     "variables": {},
        >>>     "operationName": ""
        >>> }

        Args:
            request: holds the request to execute on the http endpoint

        Returns:
            the query GraphQLResponse
        """
        payload_dict = self.make_payload(request)
        payload_str = self.settings.json_dumps(payload_dict)
        logger.debug(f"Sending request: {payload_str}")

        response = self.session.post(
            self.endpoint,
            data=payload_str,
            headers={"content-type": "application/json; charset=utf-8"},
        )
        response_str = response.text
        response_body = self.settings.json_loads(response_str)
        return GraphQLResponse(request, response_body)

    def execute_mutation(self, request: GraphQLRequest) -> GraphQLResponse:
        """Method to execute a mutation on the http server.

        Because a mutation handles the same as a query over http,
        it just calls the execute_query function without any further changes.

        Args:
            request: holds the request to execute on the http endpoint

        Returns:
            the query GraphQLResponse
        """
        return self.execute_query(request)

    def execute_subscription(
        self, request: GraphQLSubscriptionRequest
    ) -> GraphQLResponse:
        """Initiate a subscription and start listening to messages.

        This opens a websocket connection and starts the initiation sequence.

        First send the "connection_init" request with the request.options.
        Second await the "connection_ack" message from the server.
        Third "start" the subscription and wait for incoming messages.

        Args:
            request: holds the request to execute

        Returns:
            A GraphQLSubscriptionResponse instance that can be iterated
        """
        payload_dict = self.make_payload(request)
        request.subscription_id = (
            request.subscription_id or self.generate_subscription_id()
        )
        ws = websocket.WebSocket()

        logger.debug(f"Connection websocket to '{self.ws_endpoint}'")
        ws.connect(
            self.ws_endpoint,
            subprotocols=[GRAPHQL_WS_PROTOCOL, GRAPHQL_TRANSPORT_WS_PROTOCOL],
        )

        # initiate connection
        logger.debug(f"Sending initiation payload")
        ws.send(
            self.settings.json_dumps(
                {"type": CONNECTION_INIT, "payload": request.options}
            )
        )

        initiation_response = self.settings.json_loads(ws.recv())
        if initiation_response["type"] != CONNECTION_ACKNOWLEDGED:
            logger.critical(f"The server did not acknowledged the connection.")
            raise ConnectionRejected("The server did not acknowledge the connection.")

        # connection acknowledged, start subscription
        logger.debug(f"Connection acknowledged, starting subscription.")
        ws.send(
            self.settings.json_dumps(
                {"type": START, "id": request.subscription_id, "payload": payload_dict}
            )
        )

        return GraphQLSubscriptionResponse(request, ws, settings=self.settings)
