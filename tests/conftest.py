import asyncio
import multiprocessing
import time
from typing import List, AsyncGenerator

import fastapi
import fastapi.testclient
import pytest
import strawberry
import uvicorn
from strawberry.asgi import GraphQL

from qlient.http import HTTPClient


@pytest.fixture(scope="session")
def strawberry_schema() -> strawberry.Schema:
    @strawberry.type
    class Book:
        title: str
        author: str

    my_books = [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        )
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

    @strawberry.type
    class Subscription:
        @strawberry.subscription
        async def count(self, target: int = 10) -> AsyncGenerator[int, None]:
            for i in range(target):
                yield i
                await asyncio.sleep(0.1)

    # this line creates the strawberry schema
    return strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)


@pytest.fixture(scope="session", autouse=True)
def qlient_fastapi_app_proc(strawberry_schema):
    def _target():
        app = fastapi.FastAPI()
        graphql_app = GraphQL(strawberry_schema)
        app.add_route("/graphql", graphql_app)
        app.add_websocket_route("/graphql", graphql_app)
        uvicorn.run(app, host="127.0.0.1", port=8080)

    proc = multiprocessing.Process(
        target=_target,
        daemon=True,
    )
    proc.start()

    time.sleep(1)

    yield
    proc.terminate()


@pytest.fixture
def qlient_http_client() -> HTTPClient:
    return HTTPClient("http://127.0.0.1:8080/graphql")
