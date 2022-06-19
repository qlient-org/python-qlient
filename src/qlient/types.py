"""This file contains all the types definitions that can be used for type hinting"""
import multiprocessing
from queue import Empty
from typing import Union, Dict, List, Optional, Any

JSON = Union[str, int, float, bool, None, Dict[str, "JSON"], List["JSON"]]

GraphQLQuery = str
GraphQLVariables = Optional[Dict[str, JSON]]
GraphQLOperation = Optional[str]
GraphQLReturnType = Dict[str, JSON]
GraphQLContext = Optional[Any]
GraphQLRoot = Optional[Any]

GraphQLData = Optional[Dict[str, JSON]]
GraphQLErrors = Optional[List[Dict[str, JSON]]]
GraphQLExtensions = Optional[List[Dict[str, JSON]]]


class GraphQLReturnTypeIterator:

    def __init__(self, queue: multiprocessing.Queue):
        self.queue = queue

    def __iter__(self):
        return self

    def __next__(self) -> GraphQLReturnType:
        while True:
            try:
                return self.queue.get()
            except Empty:
                pass
