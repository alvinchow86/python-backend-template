
from graphene import ID, ObjectType, String


class User(ObjectType):
    id = ID()
    email = String()
