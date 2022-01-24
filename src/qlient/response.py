import json
from typing import Optional, List, Dict, Any

import requests


class BaseResponse:

    def __init__(self, response: requests.Response):
        self.response: requests.Response = response


class GraphQLResponse(BaseResponse):

    def __init__(self, response: requests.Response):
        super(GraphQLResponse, self).__init__(response)
        self.request_content: Dict[str, Any] = json.loads(self.response.request.body)
        self.response_content: Dict[str, Any] = self.response.json()

        # request information parsing
        self.query: str = self.request_content["query"]
        self.variables: Dict[str, Any] = self.request_content["variables"]
        self.operation_name: str = self.request_content["operationName"]

        # response parsing
        self.data: Optional[Dict[str, Any]] = self.response_content.get("data")
        self.errors: Optional[List[Dict[str, Any]]] = self.response_content.get("errors")
        self.extensions: Optional[Dict[str, Any]] = self.response_content.get("extensions")
