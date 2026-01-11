import asyncio
import sys
import os

# Ensure app is in path
sys.path.append(os.getcwd())

from strawberry.types import Info
from posts.resolvers import get_likes
from posts.schemas import Post
from database import SessionLocal
from dataloaders import DataLoaders

async def main():
    print("Starting debug script")
    db = SessionLocal()
    loaders = DataLoaders(db)
    
    # Mock Info
    class MockContext:
        pass
    
    ctx = MockContext()
    ctx.loaders = loaders
    ctx.db = db
    
    class MockInfo:
        context = ctx
    
    # Mock Post (first post ID 1 usually exists from seed)
    post = Post(
        id=1, 
        author_id=1, 
        content="Test", 
        image_url=None, 
        created_at=None, 
        updated_at=None
    )
    
    print("Calling get_likes...")
    try:
        res = await get_likes(post, MockInfo())
        print(f"Result: {res}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
