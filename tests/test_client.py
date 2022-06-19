# skipcq: PY-D0003
def test_simple_client(swapi_schema):
    from qlient.client import Client
    from qlient import HTTPBackend
    client = Client(
        "https://swapi-graphql.netlify.app/.netlify/functions/index",
        schema=swapi_schema
    )

    assert isinstance(client.backend, HTTPBackend)
    assert client.backend.endpoint == "https://swapi-graphql.netlify.app/.netlify/functions/index"
    assert "allPeople" in client.query
