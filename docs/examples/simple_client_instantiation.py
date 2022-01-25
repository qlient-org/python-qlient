from qlient import Client, HTTPBackend, Schema

client = Client("https://swapi-graphql.netlify.app/.netlify/functions/index")

assert isinstance(client.schema, Schema)
assert isinstance(client.backend, HTTPBackend)
