from typing import Union, Dict, List, Optional, Any

JSON = Union[
    str,
    int,
    float,
    bool,
    None,
    Dict[str, "JSON"],
    List["JSON"]
]

GraphQLQuery = str
GraphQLVariables = Optional[Dict[str, JSON]]
GraphQLOperation = Optional[str]
GraphQLReturnType = Dict[str, JSON]
GraphQLContext = Optional[Any]
GraphQLRoot = Optional[Any]

GraphQLData = Optional[Dict[str, JSON]]
GraphQLErrors = Optional[List[Dict[str, JSON]]]
GraphQLExtensions = Optional[List[Dict[str, JSON]]]
