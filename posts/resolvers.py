import sys
import strawberry
from typing import List, Optional, TYPE_CHECKING
from posts import models
from sqlalchemy.orm import Session # type: ignore

import users.schemas as user_schemas
import comments.schemas as comment_schemas
import likes.schemas as like_schemas
import tags.schemas as tag_schemas
import posts.schemas as post_schemas
from tags import models as tag_models
from users import models as user_models

if TYPE_CHECKING:
    from users.schemas import User
    from comments.schemas import Comment
    from likes.schemas import Like
    from tags.schemas import Tag
    from posts.schemas import Post

# Field Resolvers
async def get_author(root: "Post", info: strawberry.Info) -> Optional["User"]:
    loaders = info.context.loaders
    user = await loaders.user_loader.load(root.author_id)
    return user_schemas.User.from_db_model(user) if user else None

async def get_comments(root: "Post", info: strawberry.Info) -> List["Comment"]:
    loaders = info.context.loaders
    comments = await loaders.comments_by_post_loader.load(root.id)
    return [comment_schemas.Comment.from_db_model(comment) for comment in comments]

async def get_likes(root: "Post", info: strawberry.Info) -> List["Like"]:
    loaders = info.context.loaders
    likes = await loaders.likes_by_post_loader.load(root.id)
    return [like_schemas.Like.from_db_model(like) for like in likes]

async def get_tags(root: "Post", info: strawberry.Info) -> List["Tag"]:
    loaders = info.context.loaders
    tags = await loaders.tags_by_post_loader.load(root.id)
    return [tag_schemas.Tag.from_db_model(tag) for tag in tags]

async def get_likes_count(root: "Post", info: strawberry.Info) -> int:
    loaders = info.context.loaders
    likes = await loaders.likes_by_post_loader.load(root.id)
    return len(likes)

# Query Resolvers
def resolve_post(id: int, info: strawberry.Info) -> Optional["Post"]:
    if not info.context.user:
        raise Exception("Not authenticated")
    
    db = info.context.db
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise Exception(f"Post with id {id} not found")
    return post_schemas.Post.from_db_model(post)

def resolve_posts(
    info: strawberry.Info,
    author_id: Optional[int] = None,
    tag_id: Optional[int] = None
) -> List["Post"]:
    if not info.context.user:
        raise Exception("Not authenticated")
    
    db = info.context.db
    query = db.query(models.Post)
    
    if author_id:
        query = query.filter(models.Post.author_id == author_id)
    
    if tag_id:
        query = query.join(models.Post.tags).filter(tag_models.Tag.id == tag_id)
    
    all_posts = query.order_by(models.Post.created_at.desc()).all()
    res = [post_schemas.Post.from_db_model(post) for post in all_posts]
    if res:
        import sys
        sys.stderr.write(f"DEBUG resolve_posts[0]: {res[0]}\n")
        sys.stderr.write(f"DEBUG resolve_posts[0] dict: {res[0].__dict__}\n")
    return res

def resolve_feed(info: strawberry.Info) -> List["Post"]:
    current_user = info.context.user
    if not current_user:
        raise Exception("Not authenticated")
    
    db = info.context.db
    user = db.query(user_models.User).filter(
        user_models.User.id == current_user.id
    ).first()
    
    following_ids = [u.id for u in user.following]
    
    all_posts = db.query(models.Post).filter(
        models.Post.author_id.in_(following_ids)
    ).order_by(models.Post.created_at.desc()).all()
    
    return [post_schemas.Post.from_db_model(post) for post in all_posts]
