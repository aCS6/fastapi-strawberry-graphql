import strawberry
from typing import List, Optional, Annotated, TYPE_CHECKING
from users import models
from sqlalchemy.orm import Session # type: ignore
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password
from datetime import timedelta

# Import schemas for runtime usage?
# The user wants NO import inside function.
# If I import schemas here, I risk cycle.
# BUT, users/schemas.py imports this file.
# If I use `import users.schemas` instead of `from users.schemas import User`, does it help?
# `users.schemas.User` might work if not accessed at module level.
import users.schemas 
import posts.schemas

if TYPE_CHECKING:
    from posts.schemas import Post
    from users.schemas import User, LoginInput, LoginResponse

# Field Resolvers
async def get_posts_for_user(root: "User", info: strawberry.Info) -> List["Post"]:
    loaders = info.context.loaders
    user_posts = await loaders.posts_by_author_loader.load(root.id)
    return [posts.schemas.Post.from_db_model(post) for post in user_posts]

def get_followers(root: "User", info: strawberry.Info) -> List["User"]:
    # from users.schemas import User # Removed
    db = info.context.db
    user = db.query(models.User).filter(models.User.id == root.id).first()
    return [users.schemas.User.from_db_model(follower) for follower in user.followers]

def get_following(root: "User", info: strawberry.Info) -> List["User"]:
    # from users.schemas import User # Removed
    db = info.context.db
    user = db.query(models.User).filter(models.User.id == root.id).first()
    return [users.schemas.User.from_db_model(following) for following in user.following]

# Query Resolvers
def resolve_me(info: strawberry.Info) -> Optional["User"]:
    # from users.schemas import User # Removed
    user = info.context.user
    if not user:
        raise Exception("Not authenticated")
    return users.schemas.User.from_db_model(user)

def resolve_user(id: int, info: strawberry.Info) -> Optional["User"]:
    # from users.schemas import User # Removed
    if not info.context.user:
        raise Exception("Not authenticated")
    
    db = info.context.db
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise Exception(f"User with id {id} not found")
    return users.schemas.User.from_db_model(user)

def resolve_users(info: strawberry.Info) -> List["User"]:
    # from users.schemas import User # Removed
    if not info.context.user:
        raise Exception("Not authenticated")
    
    db = info.context.db
    all_users = db.query(models.User).all()
    return [users.schemas.User.from_db_model(u) for u in all_users]

# Mutation Resolvers
def resolve_login(
    input: Annotated["LoginInput", strawberry.lazy("users.schemas")],
    info: strawberry.Info
) -> Annotated["LoginResponse", strawberry.lazy("users.schemas")]:
    # from users.schemas import LoginResponse, User # Removed
    
    db = info.context.db
    user = db.query(models.User).filter(
        models.User.username == input.username
    ).first()
    
    if not user:
        raise Exception("Invalid username or password")
    
    if not verify_password(input.password, user.password_hash):
        raise Exception("Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return users.schemas.LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=users.schemas.User.from_db_model(user)
    )
