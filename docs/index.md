# Overview

[![qlient-org](https://circleci.com/gh/qlient-org/python-qlient.svg?style=svg)](https://circleci.com/gh/qlient-org/python-qlient)
[![pypi](https://img.shields.io/pypi/v/python-qlient.svg)](https://pypi.python.org/pypi/python-qlient)
[![versions](https://img.shields.io/pypi/pyversions/python-qlient.svg)](https://github.com/qlient-org/python-qlient)
[![license](https://img.shields.io/github/license/qlient-org/python-qlient.svg)](https://github.com/qlient-org/python-qlient/blob/master/LICENSE)

A fast and modern graphql client designed with simplicity in mind.

## Quick introduction

## Quick Start

```python
from qlient import Client, Fields

client = Client("https://api.spacex.land/graphql/")

mission_fields = Fields("mission_id", "mission_name")
rocket_fields = Fields("rocket_name", fairings="ship")

result = client.query.launchesPast(
    limit=3,
    _fields=Fields(mission_fields, rocket=rocket_fields)
)
print(result)
```

```json
{
  "data": {
    "launchesPast": [
      {
        "mission_name": "Starlink-15 (v1.0)",
        "rocket": {
          "rocket_name": "Falcon 9",
          "fairings": {
            "ship": "GOMSCHIEF"
          }
        }
      },
      {
        "mission_name": "Sentinel-6 Michael Freilich",
        "rocket": {
          "rocket_name": "Falcon 9",
          "fairings": {
            "ship": null
          }
        }
      },
      {
        "mission_name": "Crew-1",
        "rocket": {
          "rocket_name": "Falcon 9",
          "fairings": null
        }
      }
    ]
  }
}
```