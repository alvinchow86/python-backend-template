from graphql import GraphQLError
from graphene import Boolean, Field, InputObjectType, String, Mutation

from alvinchow_backend.api.graphql.types import User
from alvinchow_backend.db.repository import user_repo
from alvinchow_backend.lib.web.user import (
    get_current_user,
    login_user_with_credentials,
    logout_current_user,
    AuthenticationError
)


def get_user_or_raise(user_id):
    user = user_repo.get_user(user_id, raise_exception=False)
    if not user:
        raise GraphQLError("Not found")
    return user


# -----------
# Input types
# -----------
class UserInput(InputObjectType):
    password = String()


# --------
# Queries
# --------
class UserQuery:
    my_user = Field(User)

    def resolve_my_user(root, info):
        user = get_current_user()
        return user


# ----------
# Mutations
# ----------
class Login(Mutation):
    class Arguments:
        email = String()
        password = String()

    Output = User

    def mutate(root, info, email, password):
        try:
            user = login_user_with_credentials(email, password)
        except AuthenticationError:
            raise GraphQLError('Invalid credentials')

        return user


class Logout(Mutation):
    Output = Boolean

    def mutate(root, info):
        logout_current_user()

        return True


class UserMutation:
    login = Login.Field()
    logout = Logout.Field()
