from qlient import Fields, Field

name_fields = Fields("first_name", "last_name")
age_field = Field("age")

person_fields = name_fields + age_field

# { first_name last_name age }
