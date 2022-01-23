from typing import Optional, List, Dict, Any

import requests


class QlientResponse:

    def __init__(self, response: requests.Response):
        self.response: requests.Response = response
        self.response_content: Dict[str, Any] = self.response.json()

        self.data: Optional[Dict[str, Any]] = self.response_content.get("data")
        self.errors: Optional[List[Dict[str, Any]]] = self.response_content.get("errors")
        self.extensions: Optional[Dict[str, Any]] = self.response_content.get("extensions")
