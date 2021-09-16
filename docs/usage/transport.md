# Transport

The transport is responsible for communicating with your graphql api. He is the one sending and receiving your queries.

We have decided to use ``requests.Session`` under the hood.

This makes it simple to integrate into your existing projects and allow for session based authentication.

## Basic Authentication

Below is an example that shows how to use a pre-configured ``requests.Session`` with basic authentication for requests.

````python
from requests import Session

from qlient import Client, Transport

my_session = Session()
my_session.auth = ("my-user", "my-password")

my_transport = Transport(session=my_session)

client = Client(endpoint="https://...", transport=my_transport)
````