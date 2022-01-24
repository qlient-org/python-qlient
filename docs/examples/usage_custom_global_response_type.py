import requests

from qlient import Client, Settings
from qlient.response import BaseResponse


class MyCustomResponse(BaseResponse):
    def __init__(self, response: requests.Response):
        super(MyCustomResponse, self).__init__(response)

        # do something with the response here
        self.response_code = self.response.status_code


client = Client("https://...", settings=Settings(response_type=MyCustomResponse))

res = client.query.myQuery("foo")

type(res)  # <class '__main__.MyCustomResponse'>
print(res.response_code)  # 200
