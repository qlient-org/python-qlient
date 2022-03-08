# Qlient: Python GraphQL Client

[![qlient-org](https://circleci.com/gh/qlient-org/python-qlient.svg?style=svg)](https://circleci.com/gh/qlient-org/python-qlient)
[![DeepSource](https://deepsource.io/gh/qlient-org/python-qlient.svg/?label=resolved+issues&token=WQWScZui5Jy-cNg3fzvWxqhW)](https://deepsource.io/gh/qlient-org/python-qlient/?ref=repository-badge)
[![pypi](https://img.shields.io/pypi/v/qlient.svg)](https://pypi.python.org/pypi/qlient)
[![versions](https://img.shields.io/pypi/pyversions/qlient.svg)](https://github.com/qlient-org/python-qlient)
[![license](https://img.shields.io/github/license/qlient-org/python-qlient.svg)](https://github.com/qlient-org/python-qlient/blob/master/LICENSE)

A fast and modern graphql client designed with simplicity in mind.

## Help

See [documentation](https://qlient-org.github.io/python-qlient/) for more details

## Installation

```shell script
pip install qlient
```

## Quick Start

````python
from qlient import Client, GraphQLResponse

client = Client("https://swapi-graphql.netlify.app/.netlify/functions/index")

res: GraphQLResponse = client.query.film(
    # swapi graphql input fields
    id="ZmlsbXM6MQ==",

    # qlient specific
    _fields=["id", "title", "episodeID"]
)

print(res.query)  # query film($id: ID) { film(id: $id) { id title episodeID } }
print(res.variables)  # {'id': 'ZmlsbXM6MQ=='}
print(res.data)  # {'film': {'id': 'ZmlsbXM6MQ==', 'title': 'A New Hope', 'episodeID': 4}}
````
