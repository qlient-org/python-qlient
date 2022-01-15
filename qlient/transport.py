""" This file contains the different transports

:author: Daniel Seifert
:created: 09.09.2021
"""
import logging
from typing import Optional, Dict

from requests import Session, Response


class Transport:
    """ This class is used for sending the request """

    logger = logging.getLogger("qlient")

    _default_session = Session

    def __init__(self, session: Optional[Session] = None):
        self.session: Session = session or self._default_session()

    def send_query(self, endpoint: str, operation_name: str, query: str, variables: Dict) -> Dict:
        """ Send a query to the graphql endpoint

        :param endpoint: holds the endpoint to send the query to
        :param operation_name: holds the name of the operation
        :param query: holds the query
        :param variables: holds variables that should be sent with in the query
        :return: the response parsed as dictionary
        """
        self.logger.info(f"Sending operation `{operation_name}` to `{endpoint}`")
        self.logger.debug(f"Query: {query}")
        self.logger.debug(f"Variables: {variables}")
        query_response: Response = self.session.post(
            endpoint,
            json={
                "query": query,
                "operationName": operation_name,
                "variables": variables
            }
        )
        query_response.raise_for_status()
        return query_response.json()

    def __str__(self) -> str:
        """ Return a simple string representation of the transport instance """
        return repr(self)

    def __repr__(self) -> str:
        """ Return a detailed string representation of the transport instance """
        class_name = self.__class__.__name__
        return f"{class_name}(session={self.session})"
