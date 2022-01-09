""" This file contains the operation proxies

:author: Daniel Seifert
:created: 16.09.2021
:copyright: Swisscom
"""
import abc
import itertools
from typing import Dict, Iterable, Optional

from qlient.schema.models import Field


class Operation:
    """ Base class for all graphql operations """

    def __init__(self, proxy: "ServiceProxy", operation_field: Field):
        self._proxy: "ServiceProxy" = proxy
        self.type: Field = operation_field

    def __str__(self) -> str:
        """ Return a simple string representation of this instance """
        class_name = self.__class__.__name__
        return f"{class_name}(`{self.type.name}`)"

    def __repr__(self) -> str:
        """ Return a detailed string representation of this instance """
        class_name = self.__class__.__name__
        return f"{class_name}(type={self.type})"

    def __call__(
            self,
            _fields: Optional = None,
            **kwargs
    ):
        raise NotImplementedError


class Query(Operation):
    """ Represents the operation proxy for queries """

    def __call__(self, *args, **kwargs):
        pass


class Mutation(Operation):
    """ Represents the operation proxy for mutations """

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class Subscription(Operation):
    """ Represents the operation proxy for subscriptions """

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class ServiceProxy(abc.ABC):
    """ Base class for all service proxies """

    @abc.abstractmethod
    def get_bindings(self) -> Dict[str, Operation]:
        """ Abstract base method to get the service bindings """

    def __init__(self, client):
        """ Instantiate a new instance of ServiceProxy """
        self.client = client
        self.operations: Dict[str, Operation] = self.get_bindings()

    def __getattr__(self, key: str) -> Operation:
        """ Return the OperationProxy for the given key.

        :param key: holds the operation key
        :return: the according OperationProxy
        :raises: AttributeError when the no operation with that key exists.
        """
        return self[key]

    def __getitem__(self, key: str) -> Operation:
        """ Return the OperationProxy for the given key.

        :param key: holds the operation key
        :return: the according OperationProxy
        :raises: AttributeError when the no operation with that key exists.
        """
        try:
            return self.operations[key]
        except KeyError:
            self.__missing__(key)

    def __missing__(self, key: str):
        raise AttributeError(f"No operation found for key {key}")

    def __iter__(self):
        """ Return iterator for the services and their callables. """
        return iter(self.operations.items())

    def __dir__(self) -> Iterable[str]:
        """ Return the names of the operations. """
        return list(itertools.chain(dir(super()), self.operations))

    def __call__(
            self,
            query: str,
            operation: Optional[str] = None,
            variables: Optional[Dict] = None,
            *args,
            **kwargs
    ) -> Dict:
        """ Send a query to the graphql server """
        return self.client.transport.send_query(
            endpoint=self.client.endpoint,
            operation_name=operation,
            query=query,
            variables=variables
        )

    def __str__(self) -> str:
        """ Return a simple string representation of this instance """
        class_name = self.__class__.__name__
        return f"{class_name}(bindings={len(self.operations)})"

    def __repr__(self) -> str:
        """ Return a detailed string representation of this instance """
        class_name = self.__class__.__name__
        return f"{class_name}(bindings={list(self.operations.keys())})"


class QueryService(ServiceProxy):
    """ Represents the query service """

    def get_bindings(self) -> Dict[str, Operation]:
        """ Method to get the query service bindings """
        bindings = {}
        if not self.client.schema.query_type:
            return bindings

        for field in self.client.schema.query_type.fields:
            bindings[field.name] = Query(self, field)
        return bindings


class MutationService(ServiceProxy):
    """ Represents the mutation service """

    def get_bindings(self) -> Dict[str, Operation]:
        """ Method to get the mutation service bindings """
        bindings = {}
        if not self.client.schema.query_type:
            return bindings

        for field in self.client.schema.mutation_type.fields:
            bindings[field.name] = Mutation(self, field)
        return bindings
