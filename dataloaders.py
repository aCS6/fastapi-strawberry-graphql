from typing import List, Optional
from strawberry.dataloader import DataLoader
from sqlalchemy.orm import Session
from users import models as user_models
from posts import models as post_models
from comments import models as comment_models
from likes import models as like_models
from tags import models as tag_models


async def load_users(keys: List[int], db: Session) -> List[Optional[user_models.User]]:
    users = db.query(user_models.User).filter(user_models.User.id.in_(keys)).all()
    user_map = {user.id: user for user in users}
    return [user_map.get(key) for key in keys]


async def load_posts(keys: List[int], db: Session) -> List[Optional[post_models.Post]]:
    posts = db.query(post_models.Post).filter(post_models.Post.id.in_(keys)).all()
    post_map = {post.id: post for post in posts}
    return [post_map.get(key) for key in keys]


async def load_comments(keys: List[int], db: Session) -> List[Optional[comment_models.Comment]]:
    comments = db.query(comment_models.Comment).filter(comment_models.Comment.id.in_(keys)).all()
    comment_map = {comment.id: comment for comment in comments}
    return [comment_map.get(key) for key in keys]


async def load_posts_by_author(keys: List[int], db: Session) -> List[List[post_models.Post]]:
    posts = db.query(post_models.Post).filter(post_models.Post.author_id.in_(keys)).all()
    posts_map = {}
    for post in posts:
        if post.author_id not in posts_map:
            posts_map[post.author_id] = []
        posts_map[post.author_id].append(post)
    return [posts_map.get(key, []) for key in keys]


async def load_comments_by_post(keys: List[int], db: Session) -> List[List[comment_models.Comment]]:
    comments = db.query(comment_models.Comment).filter(comment_models.Comment.post_id.in_(keys)).all()
    comments_map = {}
    for comment in comments:
        if comment.post_id not in comments_map:
            comments_map[comment.post_id] = []
        comments_map[comment.post_id].append(comment)
    return [comments_map.get(key, []) for key in keys]


async def load_likes_by_post(keys: List[int], db: Session) -> List[List[like_models.Like]]:
    likes = db.query(like_models.Like).filter(like_models.Like.post_id.in_(keys)).all()
    likes_map = {}
    for like in likes:
        if like.post_id not in likes_map:
            likes_map[like.post_id] = []
        likes_map[like.post_id].append(like)
    return [likes_map.get(key, []) for key in keys]


async def load_likes_by_comment(keys: List[int], db: Session) -> List[List[like_models.Like]]:
    likes = db.query(like_models.Like).filter(like_models.Like.comment_id.in_(keys)).all()
    likes_map = {}
    for like in likes:
        if like.comment_id not in likes_map:
            likes_map[like.comment_id] = []
        likes_map[like.comment_id].append(like)
    return [likes_map.get(key, []) for key in keys]


async def load_tags_by_post(keys: List[int], db: Session) -> List[List[tag_models.Tag]]:
    from sqlalchemy.orm import joinedload
    posts = db.query(post_models.Post).options(
        joinedload(post_models.Post.tags)
    ).filter(post_models.Post.id.in_(keys)).all()
    
    tags_map = {post.id: post.tags for post in posts}
    return [tags_map.get(key, []) for key in keys]


class DataLoaders:
    def __init__(self, db: Session):
        self.db = db
        self.user_loader = DataLoader(load_fn=lambda keys: load_users(keys, db))
        self.post_loader = DataLoader(load_fn=lambda keys: load_posts(keys, db))
        self.comment_loader = DataLoader(load_fn=lambda keys: load_comments(keys, db))
        self.posts_by_author_loader = DataLoader(load_fn=lambda keys: load_posts_by_author(keys, db))
        self.comments_by_post_loader = DataLoader(load_fn=lambda keys: load_comments_by_post(keys, db))
        self.likes_by_post_loader = DataLoader(load_fn=lambda keys: load_likes_by_post(keys, db))
        self.likes_by_comment_loader = DataLoader(load_fn=lambda keys: load_likes_by_comment(keys, db))
        self.tags_by_post_loader = DataLoader(load_fn=lambda keys: load_tags_by_post(keys, db))
