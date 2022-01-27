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


my_books = [
    Book(title="The Great Gatsby", author="F. Scott Fitzgerald")
]


@strawberry.type
class Query:
    @strawberry.field
    def get_books(self) -> List[Book]:
        return my_books


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        book = Book(title=title, author=author)
        my_books.append(book)
        return book


# this line creates the strawberry schema
my_book_schema = strawberry.Schema(query=Query, mutation=Mutation)


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

# note that the operation is now named "getBooks"
# instead of the actual method "get_books"
# This is due to the automatic camel case conversation in strawberry
# https://strawberry.rocks/docs/types/schema-configurations
response: GraphQLResponse = client.query.getBooks(_fields=["title", "author"])

print(response.data)  # {"getBooks": [{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}]}

response: GraphQLResponse = client.mutation.addBook(
    title="1984",
    author="George Orwell",
    _fields=["title", "author"]
)

print(response.data)
# {
#   "addBook": {
#       "title": "1984",
#       "author": "George Orwell"
#   }
# }

response: GraphQLResponse = client.query.getBooks(_fields=["title", "author"])

print(response.data)
# {
#     "getBooks": [
#         {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
#         {"title": "1984", "author": "George Orwell"}
#     ]
# }
