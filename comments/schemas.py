import strawberry
from typing import Optional, List, TYPE_CHECKING, Annotated
from datetime import datetime
import comments.resolvers as resolvers

if TYPE_CHECKING:
    from users.schemas import User
    from posts.schemas import Post
    from likes.schemas import Like

@strawberry.type
class Comment:
    id: int
    author_id: int
    post_id: Optional[int]
    parent_comment_id: Optional[int]
    content: str
    created_at: datetime
    updated_at: datetime

    # Use class variable pattern with explicit resolver functions
    author: Optional[Annotated["User", strawberry.lazy("users.schemas")]] = strawberry.field(resolver=resolvers.get_comment_author)
    post: Optional[Annotated["Post", strawberry.lazy("posts.schemas")]] = strawberry.field(resolver=resolvers.get_comment_post)
    parent_comment: Optional["Comment"] = strawberry.field(resolver=resolvers.get_parent_comment)
    replies: List["Comment"] = strawberry.field(resolver=resolvers.get_replies)
    likes: List[Annotated["Like", strawberry.lazy("likes.schemas")]] = strawberry.field(resolver=resolvers.get_comment_likes)

    @staticmethod
    def from_db_model(comment) -> "Comment":
        return Comment(
            id=comment.id,
            author_id=comment.author_id,
            post_id=comment.post_id,
            parent_comment_id=comment.parent_comment_id,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
