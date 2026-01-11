import strawberry
from typing import List, Optional, TYPE_CHECKING
from comments import models
from sqlalchemy.orm import Session # type: ignore

import users.schemas
import posts.schemas
import comments.schemas
import likes.schemas 

if TYPE_CHECKING:
    from users.schemas import User
    from posts.schemas import Post
    from comments.schemas import Comment
    from likes.schemas import Like

# Field Resolvers
async def get_comment_author(root: "Comment", info: strawberry.Info) -> Optional["User"]:
    # from users.schemas import User # Removed
    loaders = info.context.loaders
    user = await loaders.user_loader.load(root.author_id)
    return users.schemas.User.from_db_model(user) if user else None

async def get_comment_post(root: "Comment", info: strawberry.Info) -> Optional["Post"]:
    # from posts.schemas import Post # Removed
    loaders = info.context.loaders
    post = await loaders.post_loader.load(root.post_id)
    return posts.schemas.Post.from_db_model(post) if post else None

async def get_parent_comment(root: "Comment", info: strawberry.Info) -> Optional["Comment"]:
    # from comments.schemas import Comment # Removed
    if not root.parent_comment_id:
        return None
    loaders = info.context.loaders
    comment = await loaders.comment_loader.load(root.parent_comment_id)
    return comments.schemas.Comment.from_db_model(comment) if comment else None

def get_replies(root: "Comment", info: strawberry.Info) -> List["Comment"]:
    # from comments.schemas import Comment # Removed
    db = info.context.db
    replies = db.query(models.Comment).filter(
        models.Comment.parent_comment_id == root.id
    ).all()
    return [comments.schemas.Comment.from_db_model(reply) for reply in replies]

async def get_comment_likes(root: "Comment", info: strawberry.Info) -> List["Like"]:
    # from likes.schemas import Like # Removed
    loaders = info.context.loaders
    comment_likes = await loaders.likes_by_comment_loader.load(root.id)
    return [like_schemas.Like.from_db_model(like) for like in comment_likes]

# Query Resolvers
def resolve_comment(id: int, info: strawberry.Info) -> Optional["Comment"]:
    # from comments.schemas import Comment # Removed
    if not info.context.user:
        raise Exception("Not authenticated")
    
    db = info.context.db
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise Exception(f"Comment with id {id} not found")
    return comments.schemas.Comment.from_db_model(comment)

def resolve_comments(
    info: strawberry.Info,
    post_id: Optional[int] = None
) -> List["Comment"]:
    # from comments.schemas import Comment # Removed
    if not info.context.user:
        raise Exception("Not authenticated")
    
    db = info.context.db
    query = db.query(models.Comment)
    
    if post_id:
        query = query.filter(models.Comment.post_id == post_id)
    
    all_comments = query.order_by(models.Comment.created_at.desc()).all()
    return [comments.schemas.Comment.from_db_model(comment) for comment in all_comments]
