# Overview

{% include "./examples/project_batches.md" %}

A fast and modern graphql client designed with simplicity in mind.

**Highlights**:

* Automatic graphql query generation.
* Offline query validation
* Build on top of [requests](https://docs.python-requests.org).
* Tested with [hypothesis](https://hypothesis.readthedocs.io).

## Quick Introduction

`qlient` inspects the GraphQL schema and generates the corresponding code to use the operations and types in the schema.
This provides an easy to use programmatic interface to a GraphQL API.

## Example

```python 
{% include "./examples/index_quick_start.py" %}
```

_(This script is complete and should run "as is")_

What's going on here:

* When instantiating a new Client, the schema will be automatically resolved from the server and introspected to build
  the operation proxies.
* Then a query will be constructed using the given `kwargs` for variables and special variable `_fields` for field
  selection.
* Now, the query combined with the given variables is sent to the server and a response is returned.
