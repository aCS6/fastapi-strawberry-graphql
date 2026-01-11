import strawberry
from typing import List
from tags.schemas import Tag
from tags.resolvers import resolve_tags

@strawberry.type
class TagQuery:
    tags: List[Tag] = strawberry.field(resolver=resolve_tags)
