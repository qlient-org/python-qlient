# Proxy

The `OperationServiceProxy` object is a simple object which will check if an operation exists for attribute or item requested.
If the operation exists then it will return an `OperationProxy` object (callable) which is responsible for calling the
operation on the binding.

```python 
{% include "../examples/simple_proxy_example.py" %}
```

## Sending custom queries

If you want to send your own custom queries, say because you want to send multiple queries or have fragments, you can
use any proxy class.

**NOTE**: No validation is done to neither the query, nor the variables.

```python 
{% include "../examples/sending_custom_queries.py" %}
```