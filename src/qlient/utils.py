def gql(a) -> str:
    if type(a) == type:
        raise ValueError(f"Can not call __gql__ on type {a}.")

    if not hasattr(a, "__gql__"):
        raise NotImplementedError(f"{type(a).__name__} does not support __gql__.")

    if not callable(a.__gql__):
        raise ValueError(f"__gql__ on {a} is not callable.")

    return a.__gql__()
