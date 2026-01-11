import strawberry
from typing import List, TYPE_CHECKING
from tags import models
from sqlalchemy.orm import Session # type: ignore

import posts.schemas
import tags.schemas

if TYPE_CHECKING:
    from posts.schemas import Post
    from tags.schemas import Tag

# Field Resolvers
def get_tag_posts(root: "Tag", info: strawberry.Info) -> List["Post"]:
    # from posts.schemas import Post # Removed
    db = info.context.db
    tag = db.query(models.Tag).filter(models.Tag.id == root.id).first()
    return [posts.schemas.Post.from_db_model(post) for post in tag.posts]

# Query Resolvers
def resolve_tags(info: strawberry.Info) -> List["Tag"]:
    # from tags.schemas import Tag # Removed
    if not info.context.user:
        raise Exception("Not authenticated")
    
    db = info.context.db
    all_tags = db.query(models.Tag).all()
    return [tags.schemas.Tag.from_db_model(tag) for tag in all_tags]
