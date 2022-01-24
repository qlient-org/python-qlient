# Response

Previously you've had a look into how the operation proxies are configured and what they do. Now you'll learn what an
operation proxy will return when you call them.

## Default Response Type

By default, a `QlientResponse` is returned from an operation.

```python 
{% include "../examples/usage_default_response_type.py" %}
```

So what happens here?

* The client generates the query and sends it to the server
* The server responds with the data or possible errors
* This response is parsed to a `QlientResponse` object where the response can be easily accessed.

## Custom Response Types

But what if we want to do further processing with the response?

There are two possible ways to change the default return type.

### Configure Globally

First is by setting the custom response type globally. This can be done via the `Settings` instance.

```python 
{% include "../examples/usage_custom_global_response_type.py" %}
```

### Configure per call

Or you can configure the response type per call.

This is especially useful when you work with something like [pydantic](https://pydantic-docs.helpmanual.io/).

```python 
{% include "../examples/usage_custom_call_response_type.py" %}
```

