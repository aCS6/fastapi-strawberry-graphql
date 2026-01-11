import strawberry
from typing import Optional, List
from users.schemas import User
from users.resolvers import resolve_me, resolve_user, resolve_users

@strawberry.type
class UserQuery:
    me: Optional[User] = strawberry.field(resolver=resolve_me)
    user: Optional[User] = strawberry.field(resolver=resolve_user)
    users: List[User] = strawberry.field(resolver=resolve_users)
