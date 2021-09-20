""" This file contains the different transports

:author: Daniel Seifert
:created: 09.09.2021
:copyright: Swisscom
"""
import logging
from typing import Optional, Dict

from requests import Session, Response

from qlient import __about__


class Transport:
    """ This class is used for sending the request """

    logger = logging.getLogger(__about__.__title__)

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
