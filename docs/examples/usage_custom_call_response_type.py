from typing import List

import pydantic  # must be installed additionally
import requests

from qlient import Client
from qlient.response import BaseResponse


class Person(pydantic.BaseModel):
    id: str
    name: str


class SWAPIAllPeopleResponse(BaseResponse):
    def __init__(self, response: requests.Response):
        super(SWAPIAllPeopleResponse, self).__init__(response)

        # parse the result
        # {
        #   "data": {
        #     "allPeople": {
        #       "people": [
        #         {
        #           "id": "cGVvcGxlOjE=",
        #           "name": "Luke Skywalker"
        #         },
        #         {
        #           "id": "cGVvcGxlOjI=",
        #           "name": "C-3PO"
        #         },
        #         {
        #           "id": "cGVvcGxlOjM=",
        #           "name": "R2-D2"
        #         }
        #       ]
        #     }
        #   }
        # }
        # to the pydantic model
        self.people: List[Person] = [
            Person(**raw_person)
            for raw_person in self.response.json()["data"]["allPeople"]["people"]
        ]


client = Client("https://swapi-graphql.netlify.app/.netlify/functions/index")

res = client.query.allPeople(
    first=3,
    _fields={"people": ["id", "name"]},
    _response_type=SWAPIAllPeopleResponse  # this is the important part
)

type(res)  # <class '__main__.SWAPIAllPeopleResponse'>
print(res.people)
# [
#   Person(id='cGVvcGxlOjE=', name='Luke Skywalker'),
#   Person(id='cGVvcGxlOjI=', name='C-3PO'),
#   Person(id='cGVvcGxlOjM=', name='R2-D2')
# ]

