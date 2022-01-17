# Qlient: Python GraphQL Client

[![qlient-org](https://circleci.com/gh/qlient-org/python-qlient.svg?style=svg)](https://circleci.com/gh/qlient-org/python-qlient)
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
from qlient import Client

client = Client("https://api.spacex.land/graphql/")

res = client.query.launchesPast(
    # spacex graphql input fields
    find={"mission_name": "Starlink"},
    limit=5,
    sort="mission_name",

    # qlient specific
    _fields=["mission_name", "launch_success", "launch_year"]
)
````

which sends the following query

```gql
query launchesPast($find: LaunchFind, $limit: Int, $sort: String) {
  launchesPast(find: $find, limit: $limit, sort: $sort) {
    mission_name
    launch_success
    launch_year
  }
}
```

to the server and return this body:

````json
{
  "data": {
    "launchesPast": [
      {
        "mission_name": "Paz / Starlink Demo",
        "launch_success": true,
        "launch_year": "2018"
      },
      {
        "mission_name": "Starlink 1",
        "launch_success": true,
        "launch_year": "2019"
      },
      {
        "mission_name": "Starlink 2",
        "launch_success": true,
        "launch_year": "2020"
      },
      {
        "mission_name": "Starlink 3",
        "launch_success": true,
        "launch_year": "2020"
      },
      {
        "mission_name": "Starlink 4",
        "launch_success": true,
        "launch_year": "2020"
      }
    ]
  }
}
````
