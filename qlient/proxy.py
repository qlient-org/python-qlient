""" This file contains the operation proxies

:author: Daniel Seifert
:created: 16.09.2021
:copyright: Swisscom
"""
import itertools
from typing import Dict, Iterable, Any, Optional

from qlient.schema.models import Field


class Operation:
    """ Base class for all graphql operations """

    def __init__(self, service: "ServiceProxy", operation_field: Field):
        if not isinstance(service, ServiceProxy):
            raise TypeError(f"Argument service must be of type {ServiceProxy.__name__}")
        self.service_proxy: "ServiceProxy" = service
        self.type: Field = operation_field


class Query(Operation):
    """ Represents the operation proxy for queries """


class Mutation(Operation):
    """ Represents the operation proxy for mutations """


class Subscription(Operation):
    """ Represents the operation proxy for subscriptions """


class ServiceProxy:
    """ Base class for all service proxies """

    def __init__(self, client, bindings: Dict[str, Operation]):
        """
        Instantiate a new instance of ServiceProxy
        :param bindings: holds a dictionary with all available operations
        """
        from qlient.client import Client  # only for type check
        if not isinstance(client, Client):
            raise TypeError(f"client must be of type {Client.__name__}")
        self.client: Client = client
        self.bindings: Dict[str, Operation] = bindings

    def __getattr__(self, key: str) -> Operation:
        """
        Return the OperationProxy for the given key.
        :param key: holds the operation key
        :return: the according OperationProxy
        :raises: AttributeError when the no operation with that key exists.
        """
        return self[key]

    def __getitem__(self, key: str) -> Operation:
        """
        Return the OperationProxy for the given key.
        :param key: holds the operation key
        :return: the according OperationProxy
        :raises: AttributeError when the no operation with that key exists.
        """
        try:
            return self.bindings[key]
        except KeyError:
            self.__missing__(key)

    def __missing__(self, key: str):
        raise AttributeError(f"No operation found for key {key}")

    def __iter__(self):
        """ Return iterator for the services and their callables. """
        return iter(self.bindings.items())

    def __dir__(self) -> Iterable[str]:
        """ Return the names of the operations. """
        return list(itertools.chain(dir(super()), self.bindings))

    def __call__(self, operation: str, query: str, variables: Optional[Dict] = None, *args, **kwargs) -> Dict:
        """ Send a query to the graphql server """
        return self.client.transport.send_query(
            endpoint=self.client.endpoint,
            operation_name=operation,
            query=query,
            variables=variables
        )


class QueryService(ServiceProxy):
    """ Represents the query service """

    def __init__(self, client: Any):
        from qlient.client import Client  # only for type check
        if not isinstance(client, Client):
            raise TypeError(f"client must be of type {Client.__name__}")

        bindings = {
            field.name: Query(self, field)
            for field in self.client.schema.query_type.fields
        }

        super(QueryService, self).__init__(client, bindings)


class MutationService(ServiceProxy):
    """ Represents the mutation service """

    def __init__(self, client: Any):
        from qlient.client import Client  # only for type check
        if not isinstance(client, Client):
            raise TypeError(f"client must be of type {Client.__name__}")

        bindings = {
            field.name: Mutation(self, field)
            for field in self.client.schema.mutation_type.fields
        }

        super(MutationService, self).__init__(client, bindings)
