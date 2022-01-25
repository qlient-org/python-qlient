import requests

from qlient import Client, HTTPBackend

session = requests.Session()
session.auth = ("username", "password")

authenticated_backend = HTTPBackend(endpoint="https://...", session=session)

client = Client(authenticated_backend)

assert isinstance(client.backend, HTTPBackend)
assert client.backend.session == session
