# Cache

When the client is initialized, it will automatically retrieve the schema using the given provider. By default, qlient
does not cache these files, but it is however advised to enable this for performance reasons. This library comes with
two built in Caching Backends.

## InMemoryCache

The `InMemoryCache` caches, as the name suggests, everything in memory.

This is useful when you create a lot of clients in a short period of time.

```python 
{% include "../examples/using_in_memory_cache.py" %}
```

{% include "../examples/script_legend.md" %}

## SqliteCache

The `SqliteCache` uses pythons built in `sqlite3` package to cache the schema in a `.sqlite` file. By default, this file
is stored in the application cache folder of your operating system.

* Linux: `/home/{USER}/.cache/qlient/schemas.sqlite`
* Windows: `C:/Users/{USER}/AppData/Local/qlient/Cache/schemas.sqlite`
* Mac: `/Users/{USER}/Library/Caches/qlient/schemas.sqlite`

However, the path can be adjusted to your liking.

```python 
{% include "../examples/using_sqlite_cache.py" %}
```

{% include "../examples/script_legend.md" %}
