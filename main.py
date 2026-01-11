from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter, BaseContext
from sqlalchemy.orm import Session
from typing import Optional
import strawberry

from database import engine, get_db, Base
from auth import get_current_user
from dataloaders import DataLoaders

# Import models to ensure registration with Base.metadata
from users import models as user_models
from posts import models as post_models
from comments import models as comment_models
from likes import models as like_models
from tags import models as tag_models

# Import Domain Queries and Mutations
from users.queries import UserQuery
from users.mutations import UserMutation
from posts.queries import PostQuery
from comments.queries import CommentQuery
from tags.queries import TagQuery

# Create tables
Base.metadata.create_all(bind=engine)

class Context(BaseContext):
    db: Session
    user: Optional[user_models.User]
    loaders: DataLoaders

    def __init__(self, db: Session, user: Optional[user_models.User] = None):
        self.db = db
        self.user = user
        self.loaders = DataLoaders(db)

async def get_context(
    request: Request,
    db: Session = Depends(get_db)
) -> Context:
    authorization = request.headers.get("authorization")
    user = await get_current_user(authorization, db)
    return Context(db=db, user=user)

@strawberry.type
class Query(UserQuery, PostQuery, CommentQuery, TagQuery):
    pass

@strawberry.type
class Mutation(UserMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI(title="Social Media GraphQL API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphql_ide="graphiql",
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {
        "message": "Social Media GraphQL API",
        "graphql_endpoint": "/graphql",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)