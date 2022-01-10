# Client

The **Client** is the main interface for interacting with the graphql server. It provides the `query`, `mutation`
and `subscription` attribute which references the different types of operations (via `ServiceProxy` class).

## Configuring a default client

The client takes one required argument (the `endpoint`) and several optional arguments which all have an impact on the
client behaviour.

```python
from qlient import Client

endpoint = "https://..."  # endpoint to your graphql api  
my_client = Client(endpoint) 
```

Initiating a client like so will make a request to the graphql server to inspect the schema. For more details on that,
have a look at the [schema documentation](./schema.md).

## Making a request

Let's say we already have our default client setup. Now how do we make requests?

Below is an example for the free spacex graphql api.

```python
from qlient import Client

client = Client("https://api.spacex.land/graphql/")

result = client.query.launchesPast(
    limit=3,
    _fields=["mission_id", "mission_name"]
)
```

```json
{
  "data": {
    "launchesPast": [
      {
        "mission_id": [],
        "mission_name": "Starlink-15 (v1.0)"
      },
      {
        "mission_id": [],
        "mission_name": "Sentinel-6 Michael Freilich"
      },
      {
        "mission_id": [
          "EE86F74"
        ],
        "mission_name": "Crew-1"
      }
    ]
  }
}
```

## Selecting nested fields

You can use the `Fields` class to make powerful selections.

Say for the example above, you'd also like to have information about the rocket.

```python
from qlient import Fields

nested_fields = Fields(
    "mission_id",
    "mission_name",
    rocket=Fields(
        fairings="ship"
    )
)

result = client.query.launchesPast(
    limit=3,
    _fields=nested_fields
)
```

For more details on the `Fields` class, have a look at the [fields documentation](./fields.md)