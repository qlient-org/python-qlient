# Proxy

The `OperationProxy` object is a simple object which will check if an operation exists for attribute or item requested.
If the operation exists then it will return an `Operation` object (callable) which is responsible for calling the
operation on the binding.

```python 
{% include "../examples/simple_proxy_example.py" %}
```