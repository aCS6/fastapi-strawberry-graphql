from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="likes", foreign_keys=[user_id])
    post = relationship("Post", back_populates="likes")
    comment = relationship("Comment", back_populates="likes")
