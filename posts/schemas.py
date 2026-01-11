import strawberry
from typing import Optional, List, TYPE_CHECKING, Annotated
from datetime import datetime
import posts.resolvers as resolvers

if TYPE_CHECKING:
    from users.schemas import User
    from comments.schemas import Comment
    from likes.schemas import Like
    from tags.schemas import Tag

@strawberry.type
class Post:
    id: int
    author_id: int
    content: str
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    # Use class variable pattern with explicit resolver functions
    author: Optional[Annotated["User", strawberry.lazy("users.schemas")]] = strawberry.field(resolver=resolvers.get_author)
    comments: List[Annotated["Comment", strawberry.lazy("comments.schemas")]] = strawberry.field(resolver=resolvers.get_comments)
    likes: List[Annotated["Like", strawberry.lazy("likes.schemas")]] = strawberry.field(resolver=resolvers.get_likes)
    tags: List[Annotated["Tag", strawberry.lazy("tags.schemas")]] = strawberry.field(resolver=resolvers.get_tags)
    likes_count: int = strawberry.field(resolver=resolvers.get_likes_count)

    @staticmethod
    def from_db_model(post) -> "Post":
        return Post(
            id=post.id,
            author_id=post.author_id,
            content=post.content,
            image_url=post.image_url,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
