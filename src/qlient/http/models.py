"""This module contains the specific qlient.http models"""
from typing import AsyncGenerator, Optional

import websocket
from qlient.core import GraphQLResponse, GraphQLSubscriptionRequest

from qlient.http.consts import (
    CONNECTION_TERMINATE,
    CONNECTION_ERROR,
    COMPLETE,
    CONNECTION_KEEP_ALIVE,
    STOP,
)
from qlient.http.settings import HTTPSettings


class GraphQLSubscriptionResponse(GraphQLResponse):
    """Model for a subscription response"""

    request: GraphQLSubscriptionRequest

    def __init__(
        self,
        request: GraphQLSubscriptionRequest,
        socket: websocket.WebSocket,
        settings: Optional[HTTPSettings] = None,
    ):
        if settings is None:
            settings = HTTPSettings()

        self.__active: bool = False
        self.ws: websocket.WebSocket = socket
        self.settings: HTTPSettings = settings

        super(GraphQLSubscriptionResponse, self).__init__(
            request, self.message_generator()
        )

    def message_generator(self) -> AsyncGenerator:
        """The message generator

        This method yields incoming subscription messages from the websocket.

        Yields:
            GraphQLResponse instances containing the messages
        """
        for msg in self.ws:
            if not msg:
                continue

            data = self.settings.json_loads(msg)
            data_type = data["type"]

            if data_type in (CONNECTION_TERMINATE, CONNECTION_ERROR, COMPLETE):
                # break the iterator
                self.close()
                break

            if data_type == CONNECTION_KEEP_ALIVE:
                continue

            yield GraphQLResponse(self.request, data["payload"])

    def stop(self):
        """Method to end the subscription

        This sends one last stop
        """
        if not self.ws.connected:
            return
        self.ws.send(
            self.settings.json_dumps({"type": STOP, "id": self.request.subscription_id})
        )

    def close(self):
        """Method to close the websocket

        This will stop the subscription before closing the socket.
        """
        self.stop()
        self.ws.close()
