import strawberry
from users.schemas import LoginInput, LoginResponse
from users.resolvers import resolve_login

@strawberry.type
class UserMutation:
    login: LoginResponse = strawberry.mutation(resolver=resolve_login)
