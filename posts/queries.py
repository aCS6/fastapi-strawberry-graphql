import strawberry
from typing import Optional, List
from posts.schemas import Post
from posts.resolvers import resolve_post, resolve_posts, resolve_feed

@strawberry.type
class PostQuery:
    post: Optional[Post] = strawberry.field(resolver=resolve_post)
    posts: List[Post] = strawberry.field(resolver=resolve_posts)
    feed: List[Post] = strawberry.field(resolver=resolve_feed)
