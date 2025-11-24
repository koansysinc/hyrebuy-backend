"""
GroupMember model - Members in buying groups
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class GroupMember(Base):
    __tablename__ = "group_members"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    group_id = Column(UUID(as_uuid=True), ForeignKey("buying_groups.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Member Status
    status = Column(String(50), default="invited", index=True)  # invited, interested, committed, deposit_paid, closed
    commitment_level = Column(String, default="0")  # 0-100 score (integer as string)

    # Joining
    invited_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    invited_at = Column(DateTime(timezone=True), nullable=True)
    joined_at = Column(DateTime(timezone=True), nullable=True)

    # Commitment
    committed_at = Column(DateTime(timezone=True), nullable=True)
    deposit_paid_at = Column(DateTime(timezone=True), nullable=True)
    deposit_amount = Column(BigInteger, nullable=True)

    # Property Selection
    selected_property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=True)

    # Tracking
    last_active_at = Column(DateTime(timezone=True), default=func.now())
    engagement_score = Column(String, default="0")  # Activity score (integer as string)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    # group = relationship("BuyingGroup", back_populates="members")
    # user = relationship("User", back_populates="group_memberships")

    # Indexes
    __table_args__ = (
        Index('idx_members_group', 'group_id'),
        Index('idx_members_user', 'user_id'),
        Index('idx_members_status', 'group_id', 'status'),
        Index('idx_members_unique', 'group_id', 'user_id', unique=True),
    )

    def __repr__(self):
        return f"<GroupMember User:{self.user_id} in Group:{self.group_id} ({self.status})>"
