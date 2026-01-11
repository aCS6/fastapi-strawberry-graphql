from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

follows_table = Table(
    'follows',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('following_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    bio = Column(Text)
    avatar_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    posts = relationship("Post", back_populates="author", foreign_keys="Post.author_id")
    comments = relationship("Comment", back_populates="author", foreign_keys="Comment.author_id")
    likes = relationship("Like", back_populates="user", foreign_keys="Like.user_id")
    
    followers = relationship(
        "User",
        secondary=follows_table,
        primaryjoin=id == follows_table.c.following_id,
        secondaryjoin=id == follows_table.c.follower_id,
        backref="following"
    )
