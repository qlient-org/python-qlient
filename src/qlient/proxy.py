""" This file contains the operation proxies

:author: Daniel Seifert
:created: 16.09.2021
"""
import abc
import itertools
from typing import Dict, Iterable, Optional, List

from qlient.builder import TypedGQLQueryBuilder, Fields
from qlient.models import GraphQLResponse
from qlient.schema.types import Field
from qlient.types import GraphQLVariables, GraphQLQuery, GraphQLOperation, GraphQLContext, GraphQLRoot


class OperationProxy(abc.ABC):
    """ Base class for all graphql operations """

    def __init__(self, proxy: "OperationServiceProxy", operation_field: Field):
        self._proxy: "OperationServiceProxy" = proxy
        self.operation_field: Field = operation_field

        self.query_builder: TypedGQLQueryBuilder = TypedGQLQueryBuilder(
            self.operation_type,
            self.operation_field,
            self._proxy.client.schema,
            self._proxy.client.settings,
        )
        self._variables: Dict = {}
        self._context: GraphQLContext = None
        self._root: GraphQLRoot = None

    def select(self, *args, **kwargs) -> "OperationProxy":
        self._variables.update(self.query_builder.fields(*args, **kwargs))
        return self

    def variables(self, **kwargs) -> "OperationProxy":
        self._variables.update(self.query_builder.variables(**kwargs))
        return self

    def context(self, context: GraphQLContext) -> "OperationProxy":
        self._context = context
        return self

    def root(self, root: GraphQLRoot) -> "OperationProxy":
        self._root = root
        return self

    def execute(self) -> GraphQLResponse:
        return self._proxy(
            query=self.query,
            operation=self.operation_field.name,
            variables=self._variables,
            context=self._context,
            root=self._root
        )

    def __str__(self) -> str:
        """ Return a simple string representation of this instance """
        class_name = self.__class__.__name__
        return f"{class_name}(`{self.operation_field.name}`)"

    def __repr__(self) -> str:
        """ Return a detailed string representation of this instance """
        class_name = self.__class__.__name__
        return f"{class_name}(field={self.operation_field})"

    @property
    @abc.abstractmethod
    def operation_type(self) -> str:
        """ Return the operation type.

        :return: Either query, mutation or subscription (Depends on the class name)
        """
        raise NotImplementedError

    @property
    def query(self) -> GraphQLQuery:
        return self.query_builder.build()

    def __gql__(self) -> GraphQLQuery:
        return self.query

    def __call__(
            self,
            _fields: Optional[Fields] = None,
            _context: GraphQLContext = None,
            _root: GraphQLRoot = None,
            **query_variables
    ) -> GraphQLResponse:
        if _fields:
            self.select(_fields)
        if query_variables:
            self.variables(**query_variables)
        if _context:
            self.context(_context)
        if _root:
            self.root(_root)
        return self.execute()


class QueryProxy(OperationProxy):
    """ Represents the operation proxy for queries """

    @property
    def operation_type(self) -> str:
        return "query"


class MutationProxy(OperationProxy):
    """ Represents the operation proxy for mutations """

    @property
    def operation_type(self) -> str:
        return "mutation"


class SubscriptionProxy(OperationProxy):
    """ Represents the operation proxy for subscriptions """

    @property
    def operation_type(self) -> str:
        return "subscription"


class OperationServiceProxy(abc.ABC):
    """ Base class for all service proxies """

    @abc.abstractmethod
    def get_bindings(self) -> Dict[str, OperationProxy]:
        """ Abstract base method to get the service bindings """

    def __init__(self, client):
        """ Instantiate a new instance of ServiceProxy """
        from qlient.client import Client  # type hint here due to circular dependency
        self.client: Client = client
        self.operations: Dict[str, OperationProxy] = self.get_bindings()

    def __contains__(self, key: str) -> bool:
        return key in self.operations

    def __getattr__(self, key: str) -> OperationProxy:
        """ Return the OperationProxy for the given key.

        :param key: holds the operation key
        :return: the according OperationProxy
        :raises: AttributeError when the no operation with that key exists.
        """
        return self[key]

    def __getitem__(self, key: str) -> OperationProxy:
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
            query: GraphQLQuery,
            operation: GraphQLOperation = None,
            variables: GraphQLVariables = None,
            context: GraphQLContext = None,
            root: GraphQLRoot = None,
            *args,
            **kwargs
    ) -> GraphQLResponse:
        """ Send a query to the graphql server """
        response_body = self.client.backend.execute_query(query, variables, operation, context, root)
        return GraphQLResponse(
            response=response_body,
            query=query,
            variables=variables,
            operation_name=operation
        )

    def __str__(self) -> str:
        """ Return a simple string representation of this instance """
        class_name = self.__class__.__name__
        return f"{class_name}(bindings={len(self.operations)})"

    def __repr__(self) -> str:
        """ Return a detailed string representation of this instance """
        class_name = self.__class__.__name__
        return f"{class_name}(bindings={self.supported_bindings})"

    @property
    def supported_bindings(self) -> List[str]:
        return list(self.operations.keys())


class QueryServiceProxy(OperationServiceProxy):
    """ Represents the query service """

    def get_bindings(self) -> Dict[str, OperationProxy]:
        """ Method to get the query service bindings """
        bindings = {}
        if not self.client.schema.query_type:
            return bindings

        for field in self.client.schema.query_type.fields:
            bindings[field.name] = QueryProxy(self, field)
        return bindings


class MutationServiceProxy(OperationServiceProxy):
    """ Represents the mutation service """

    def get_bindings(self) -> Dict[str, OperationProxy]:
        """ Method to get the mutation service bindings """
        bindings = {}
        if not self.client.schema.mutation_type:
            return bindings

        for field in self.client.schema.mutation_type.fields:
            bindings[field.name] = MutationProxy(self, field)
        return bindings
