from qlient import Client, HTTPBackend, Schema

client = Client("https://swapi-graphql.netlify.app/.netlify/functions/index")

isinstance(client.schema, Schema)
isinstance(client.backend, HTTPBackend)
