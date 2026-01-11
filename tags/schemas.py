import strawberry
from typing import List, TYPE_CHECKING, Annotated
import tags.resolvers as resolvers

if TYPE_CHECKING:
    from posts.schemas import Post

@strawberry.type
class Tag:
    id: int
    name: str

    # Use class variable pattern with explicit resolver function
    posts: List[Annotated["Post", strawberry.lazy("posts.schemas")]] = strawberry.field(resolver=resolvers.get_tag_posts)

    @staticmethod
    def from_db_model(tag) -> "Tag":
        return Tag(
            id=tag.id,
            name=tag.name,
        )
