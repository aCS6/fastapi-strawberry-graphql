import strawberry
from typing import Optional, List, TYPE_CHECKING, Annotated
from datetime import datetime
import users.resolvers as resolvers

if TYPE_CHECKING:
    from posts.schemas import Post
    from users.schemas import LoginInput, LoginResponse

@strawberry.type
class User:
    id: int
    username: str
    email: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime
    
    # Use class variable pattern with explicit resolver functions
    posts: List[Annotated["Post", strawberry.lazy("posts.schemas")]] = strawberry.field(resolver=resolvers.get_posts_for_user)
    followers: List["User"] = strawberry.field(resolver=resolvers.get_followers)
    following: List["User"] = strawberry.field(resolver=resolvers.get_following)

    @staticmethod
    def from_db_model(user) -> "User":
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            bio=user.bio,
            avatar_url=user.avatar_url,
            created_at=user.created_at,
        )

@strawberry.input
class LoginInput:
    username: str
    password: str

@strawberry.type
class LoginResponse:
    access_token: str
    token_type: str
    user: "User"
