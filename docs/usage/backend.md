# Backends

A backend is a service that can take a query, variables and an operation name to create a response. The most common
backend is probably going to be some sort of web server, which is why I've made it the default.

## The default HTTP Backend

Below you find an example on instantiating a simple client with an `HTTPBackend`.

```python 
{% include "../examples/simple_client_instantiation.py" %}
```

{% include "../examples/script_legend.md" %}

### Customizing the HTTP Backend Session

For example let's say you have to do session based authentication.

Since the http backend is based on requests, this can be quite easily achieved.

```python 
{% include "../examples/using_custom_requests_sessions.py" %}
```

So what's going on here:

* A new `requests.Session` instance is created
* The session authentication is set
* A new `HTTPBackend` with the custom session is created
* The client with the customized `HTTPBackend` is created

## Custom Backends

But although a GraphQL API is mostly used in combination with a http backend, it's not solely bound serve over http.

For example when using [strawberry](https://strawberry.rocks/) you can generally just execute queries locally.

```python 
{% include "../examples/using_custom_backends.py" %}
```

{% include "../examples/script_legend.md" %}

So what's going on here:

* After all imports are done the strawberry schema is created
* Once we have the schema, it's time to create our backend. For that we must import the base `Backend` class
  from `qlient.backend`. Then we implement the required abstract methods `execute_query` and add the `cache_key`
  property. (Later is used for using the client with a cache. But this is not necessary in this case.)
* Once we have our custom backend, all we have to do now is to create our client.
* Now we can use the client just like any other http client