# Overview

[![DeepSource](https://deepsource.io/gh/qlient-org/python-qlient.svg/?label=active+issues&token=2ZJ0b1dinekjVtwgJHSy286C)](https://deepsource.io/gh/qlient-org/python-qlient/?ref=repository-badge)
[![DeepSource](https://deepsource.io/gh/qlient-org/python-qlient.svg/?label=resolved+issues&token=2ZJ0b1dinekjVtwgJHSy286C)](https://deepsource.io/gh/qlient-org/python-qlient/?ref=repository-badge)
[![pypi](https://img.shields.io/pypi/v/qlient.svg)](https://pypi.python.org/pypi/qlient)
[![versions](https://img.shields.io/pypi/pyversions/qlient.svg)](https://github.com/qlient-org/python-qlient)
[![license](https://img.shields.io/github/license/qlient-org/python-qlient.svg)](https://github.com/qlient-org/python-qlient/blob/master/LICENSE)
[![codestyle](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

A fast and modern graphql client designed with simplicity in mind.

## Key Features

* Compatible with Python 3.7 and above
* Build on top of
  [qlient-core](https://github.com/qlient-org/python-qlient-core),
  [requests](https://github.com/psf/requests)
  and [websocket-client](https://github.com/websocket-client/websocket-client/)
* support for subscriptions

## Help

See [documentation](https://qlient-org.github.io/python-qlient/) for more details.

If you want more information about the internals,
I kindly refer you to the [qlient-core documentation](https://qlient-org.github.io/python-qlient-core/).

If you are looking for an asynchronous implementation,
I kindly refer you to the [qlient-aiohttp](https://github.com/qlient-org/python-qlient-aiohttp) sister project.

## Installation

```shell
pip install qlient
```

## Quick Start

````python
from qlient.http import HTTPClient, GraphQLResponse

client = HTTPClient("https://swapi-graphql.netlify.app/.netlify/functions/index")

res: GraphQLResponse = client.query.film(
    # swapi graphql input fields
    id="ZmlsbXM6MQ==",

    # qlient specific
    _fields=["id", "title", "episodeID"]
)

print(res.request.query)  # query film($id: ID) { film(id: $id) { id title episodeID } }
print(res.request.variables)  # {'id': 'ZmlsbXM6MQ=='}
print(res.data)  # {'film': {'id': 'ZmlsbXM6MQ==', 'title': 'A New Hope', 'episodeID': 4}}
````
