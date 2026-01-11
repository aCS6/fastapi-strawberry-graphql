from datetime import datetime
from database import SessionLocal, engine
from users import models as user_models
from posts import models as post_models
from comments import models as comment_models
from likes import models as like_models
from tags import models as tag_models
from database import Base
from auth import get_password_hash
from faker import Faker
import random

fake = Faker()

# Create database tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ----------------------------
# Create Users
# ----------------------------
users = []
for i in range(3):
    user = user_models.User(
        username=fake.user_name(),
        email=fake.email(),
        password_hash=get_password_hash("12345"),
        bio=fake.sentence(),
        avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={i}"
    )
    users.append(user)
    db.add(user)
db.commit()

# Refresh users to get IDs
for i, user in enumerate(users):
    db.refresh(user)

# ----------------------------
# Create Tags
# ----------------------------
tag_names = ["technology", "programming", "graphql", "python", "javascript", "ai"]
tags = []
for name in tag_names:
    tag = tag_models.Tag(name=name)
    tags.append(tag)
    db.add(tag)
db.commit()

# Refresh tags
for tag in tags:
    db.refresh(tag)

# ----------------------------
# Create Posts
# ----------------------------
posts = []
for user in users:
    for _ in range(20):
        post = post_models.Post(
            author_id=user.id,
            content=fake.paragraph(nb_sentences=3),
            image_url=f"https://picsum.photos/800/600?random={random.randint(1,1000)}"
        )
        # Randomly assign 1-3 tags
        post.tags.extend(random.sample(tags, random.randint(1, 3)))
        posts.append(post)
        db.add(post)
db.commit()

# Refresh posts
for post in posts:
    db.refresh(post)

# ----------------------------
# Create Comments and Replies
# ----------------------------
comments = []
for post in posts:
    # Create min 2 top-level comments
    for _ in range(2):
        comment = comment_models.Comment(
            post_id=post.id,
            author_id=random.choice(users).id,
            content=fake.sentence(),
            parent_comment_id=None
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        comments.append(comment)

        # Create 5 replies for each comment
        for _ in range(5):
            reply = comment_models.Comment(
                post_id=post.id,
                author_id=random.choice(users).id,
                content=fake.sentence(),
                parent_comment_id=comment.id
            )
            comments.append(reply)
            db.add(reply)
db.commit()

# Refresh comments
for comment in comments:
    db.refresh(comment)

# ----------------------------
# Create Likes
# ----------------------------
likes = []
for post in posts:
    # Random number of likes per post (0 to 3 users)
    likers = random.sample(users, random.randint(0, len(users)))
    for liker in likers:
        like = like_models.Like(user_id=liker.id, post_id=post.id)
        likes.append(like)
        db.add(like)
db.commit()

# ----------------------------
# Create Follows
# ----------------------------
# Each user follows 1-2 others
for user in users:
    others = [u for u in users if u.id != user.id]
    following = random.sample(others, random.randint(1, len(others)))
    for f in following:
        user.followers.append(f)
db.commit()

print("Database seeded successfully with users, posts, likes, and follows!")
db.close()
