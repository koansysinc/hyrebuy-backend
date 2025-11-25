"""
GroupInvite model - Invitation tracking for group buying
Days 29-35: Group Buying Backend (Phase 2)
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.database import Base


class GroupInvite(Base):
    __tablename__ = "group_invites"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    group_id = Column(UUID(as_uuid=True), ForeignKey("buying_groups.id", ondelete="CASCADE"), nullable=False)
    inviter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    invitee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Null if invite code shared

    # Invite Details
    invite_code = Column(String(20), unique=True, nullable=False, index=True)  # Unique code per invite
    status = Column(String(20), default="pending", index=True)  # pending, accepted, declined, expired

    # Sharing Method
    sharing_method = Column(String(20), nullable=True)  # whatsapp, email, link

    # Response
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    declined_at = Column(DateTime(timezone=True), nullable=True)

    # Expiry
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_invites_group', 'group_id'),
        Index('idx_invites_inviter', 'inviter_id'),
        Index('idx_invites_code', 'invite_code'),
        Index('idx_invites_status', 'status'),
    )

    def __repr__(self):
        return f"<GroupInvite {self.invite_code} ({self.status})>"
