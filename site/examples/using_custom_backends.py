from typing import List

import strawberry  # must be installed additionally

from qlient import Client, GraphQLResponse
from qlient.backend import Backend
from qlient.types import (
    GraphQLVariables,
    GraphQLQuery,
    GraphQLOperation,
    GraphQLReturnType,
    GraphQLContext,
    GraphQLRoot
)


@strawberry.type
class Book:
    title: str
    author: str


def get_books():
    return [Book(title='The Great Gatsby', author='F. Scott Fitzgerald', )]


@strawberry.type
class Query:
    books: List[Book] = strawberry.field(resolver=get_books)


# this line creates the strawberry schema
my_book_schema = strawberry.Schema(query=Query)


# now this is the important part
# down below we create a custom backend for our client
# this backend executes all queries locally using the given strawberry.Schema
class StrawberryBackend(Backend):

    def __init__(self, schema: strawberry.Schema):
        self.schema = schema

    def execute_query(
            self,
            query: GraphQLQuery,
            variables: GraphQLVariables = None,
            operation_name: GraphQLOperation = None,
            context: GraphQLContext = None,
            root: GraphQLRoot = None,
    ) -> GraphQLReturnType:
        # here we execute the given query on the local strawberry schema
        # as described in the testing section of the strawberry documentation
        # https://strawberry.rocks/docs/operations/testing
        result = self.schema.execute_sync(query, variables, context, root, operation_name)
        return {
            "data": result.data,
            "errors": result.errors,
            "extensions": result.extensions,
        }

    @property
    def cache_key(self) -> str:
        # required for caching purposes (not used in this example)
        return "CustomStrawberryBookBackend"


client = Client(StrawberryBackend(my_book_schema))

response: GraphQLResponse = client.query.books(_fields=["title", "author"])

print(response.data)  # {'books': [{'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'}]}
