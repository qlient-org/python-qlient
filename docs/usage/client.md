# Client

The **Client** is the main interface for interacting with the graphql server. It provides the `query`, `mutation`
and `subscription` attribute which references the different types of operations (via `ServiceProxy` class).

## Configuring a default client

The client takes one required argument (the `backend`) and several optional arguments which all have an impact on the
client behaviour.

```python 
{% include "../examples/simple_client_instantiation.py" %}
```

{% include "../examples/script_legend.md" %}

Initiating a client like so will make a request to the graphql server to inspect the schema. For more details on the
schema, have a look at the [schema documentation](./schema.md). If you want to get to know the backend, have a look at
the [backend documentation](./backend.md).

## Making a request

Let's say we already have our default client setup. Now how do we make requests?

Below is an example for the star wars api

```python 
{% include "../examples/index_quick_start.py" %}
```

{% include "../examples/script_legend.md" %}

## Selecting nested fields

You can use the `Fields` class to make powerful selections.

Say for the example above, you'd also like to have information about the rocket.

```python 
{% include "../examples/request_with_nested_fields.py" %}
```

{% include "../examples/script_legend.md" %}

For more details on the `Fields` class, have a look at the [fields documentation](./fields.md)