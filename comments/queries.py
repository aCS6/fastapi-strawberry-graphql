import strawberry
from typing import Optional, List
from comments.schemas import Comment
from comments.resolvers import resolve_comment, resolve_comments

@strawberry.type
class CommentQuery:
    comment: Optional[Comment] = strawberry.field(resolver=resolve_comment)
    comments: List[Comment] = strawberry.field(resolver=resolve_comments)
