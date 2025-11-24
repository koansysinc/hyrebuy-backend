"""
User model - Authentication and user management
"""

from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class User(Base):
    __tablename__ = "users"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Profile
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    company_id = Column(UUID(as_uuid=True), nullable=True)  # GCC company (optional)

    # Group Admin
    is_group_admin = Column(Boolean, default=False)
    total_rewards_earned = Column(String, default="0")  # Stored as string for large numbers

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships (will be defined when other models are created)
    # saved_properties = relationship("SavedProperty", back_populates="user")
    # groups_as_admin = relationship("BuyingGroup", back_populates="admin")
    # group_memberships = relationship("GroupMember", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"
