"""
GroupMessage model - Simple messaging within buying groups
Days 29-35: Group Buying Backend (Phase 2)
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Index, func, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class GroupMessage(Base):
    __tablename__ = "group_messages"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    group_id = Column(UUID(as_uuid=True), ForeignKey("buying_groups.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Message Content
    message = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, announcement, system

    # Status
    is_pinned = Column(String, default="false")  # Boolean as string

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_messages_group', 'group_id'),
        Index('idx_messages_sender', 'sender_id'),
        Index('idx_messages_created', 'group_id', 'created_at'),
    )

    def __repr__(self):
        return f"<GroupMessage in Group:{self.group_id} by User:{self.sender_id}>"
