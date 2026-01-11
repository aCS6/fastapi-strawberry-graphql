import strawberry
from typing import Optional, TYPE_CHECKING
from likes import models
from sqlalchemy.orm import Session # type: ignore

import users.schemas
import posts.schemas
import comments.schemas

if TYPE_CHECKING:
    from users.schemas import User
    from posts.schemas import Post
    from comments.schemas import Comment

async def get_like_user(root: "Like", info: strawberry.Info) -> Optional["User"]:
    # from users.schemas import User # Removed
    loaders = info.context.loaders
    user = await loaders.user_loader.load(root.user_id)
    return users.schemas.User.from_db_model(user) if user else None

async def get_like_post(root: "Like", info: strawberry.Info) -> Optional["Post"]:
    # from posts.schemas import Post # Removed
    if not root.post_id:
        return None
    loaders = info.context.loaders
    post = await loaders.post_loader.load(root.post_id)
    return posts.schemas.Post.from_db_model(post) if post else None

async def get_like_comment(root: "Like", info: strawberry.Info) -> Optional["Comment"]:
    # from comments.schemas import Comment # Removed
    if not root.comment_id:
        return None
    loaders = info.context.loaders
    comment = await loaders.comment_loader.load(root.comment_id)
    return comments.schemas.Comment.from_db_model(comment) if comment else None
