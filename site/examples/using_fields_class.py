from qlient import Fields

nested_fields = Fields(
    "first_name",  # will be converted to Field("first_name")
    "last_name",  # will be converted to Field("first_name")
    # This will be converted to
    # Field(
    #   "hobby",
    #   _sub_fields=Fields(
    #       Field("name"),
    #       Field("club", _sub_fields=Fields(Field("name")))
    #   )
    # )
    hobby=Fields("name", club="name"),
)

# last_name first_name hobby { name club { name } }
