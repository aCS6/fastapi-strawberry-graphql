import strawberry
from typing import Optional, TYPE_CHECKING, Annotated
from datetime import datetime
import likes.resolvers as resolvers

if TYPE_CHECKING:
    from users.schemas import User
    from posts.schemas import Post
    from comments.schemas import Comment

@strawberry.type
class Like:
    id: int
    user_id: int
    post_id: Optional[int]
    comment_id: Optional[int]
    created_at: datetime

    # Use class variable pattern with explicit resolver functions
    user: Optional[Annotated["User", strawberry.lazy("users.schemas")]] = strawberry.field(resolver=resolvers.get_like_user)
    post: Optional[Annotated["Post", strawberry.lazy("posts.schemas")]] = strawberry.field(resolver=resolvers.get_like_post)
    comment: Optional[Annotated["Comment", strawberry.lazy("comments.schemas")]] = strawberry.field(resolver=resolvers.get_like_comment)

    @staticmethod
    def from_db_model(like) -> "Like":
        return Like(
            id=like.id,
            user_id=like.user_id,
            post_id=like.post_id,
            comment_id=like.comment_id,
            created_at=like.created_at,
        )
