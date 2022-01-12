# Proxy

Proxying is a really important part of this library and i am not talking about server proxies.

It enables us to create callable instance that execute a given query.

## Service Proxy

For each operation there is a specific service proxy. the `client.query` is of type `QueryService` and
the `client.mutation` is of type `MutationService`.

if you want to find out which bindings a service supports, you can use the `supported_bindings` property.

```python
client = ...

print(client.query.supported_bindings)
# ["launchesPast", "landpads", "..."]
```

## Operation

An operation represents either a query, mutation or subscription on the server.

### Query

This operation makes requests to the graphql server to **get** data.

Let's have a look at the spacex graphql. This graphql api has a query to get the recent launches: `launchesPast`.

You can make requests to this query like so:

```python
from qlient import Client

client = Client("https://api.spacex.land/graphql/")

response = client.query.launchesPast(
    limit=2,
    _fields=["mission_name", "mission_id"]
)
```

### Mutation

This operation makes requests to the graphql server to **change** data.

_(The example below is fictional and not working.)_

```python
from qlient import Client

client = Client("https://...")

response = client.mutation.createUser(
    first_name="John",
    last_name="Doe"
) 
```

### Subscription

_Not yet supported_