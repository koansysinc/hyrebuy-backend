"""
BuyingGroup model - Group buying groups where employees coordinate bulk purchases
"""

from sqlalchemy import Column, String, BigInteger, Date, DateTime, ForeignKey, ARRAY, Index, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class BuyingGroup(Base):
    __tablename__ = "buying_groups"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Group Info
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)

    # Group Goals
    target_location = Column(String(100), nullable=False)
    target_configuration = Column(String(50), nullable=True)  # "3BHK", "4BHK", etc.
    budget_min = Column(BigInteger, nullable=True)
    budget_max = Column(BigInteger, nullable=False)
    preferred_builders = Column(ARRAY(UUID(as_uuid=True)), nullable=True)  # Array of builder IDs

    # Group Rules
    minimum_members = Column(String, default="5")  # Integer as string
    maximum_members = Column(String, default="20")
    close_by_date = Column(Date, nullable=True)  # Deadline to form group

    # Group Status
    status = Column(String(50), default="forming", index=True)  # forming, negotiating, closed, cancelled
    current_member_count = Column(String, default="1")  # Admin counts as 1 (integer as string)
    committed_member_count = Column(String, default="0")

    # Pricing
    expected_discount_percent = Column(String, nullable=True)  # Decimal as string (e.g., "15.00")
    current_discount_tier = Column(String(20), nullable=True)  # bronze, silver, gold, platinum

    # Negotiation
    selected_builder_id = Column(UUID(as_uuid=True), ForeignKey("builders.id"), nullable=True)
    final_discount_percent = Column(String, nullable=True)
    final_price_per_unit = Column(BigInteger, nullable=True)
    deal_closed_date = Column(Date, nullable=True)

    # Sharing
    invite_code = Column(String(20), unique=True, nullable=False, index=True)
    public_landing_page_url = Column(String, nullable=True)
    is_discoverable = Column(String, default="true")  # Boolean as string

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    # admin = relationship("User", back_populates="groups_as_admin")
    # members = relationship("GroupMember", back_populates="group")

    # Indexes
    __table_args__ = (
        Index('idx_groups_status', 'status'),
        Index('idx_groups_admin', 'admin_id'),
        Index('idx_groups_location', 'target_location'),
    )

    def __repr__(self):
        return f"<BuyingGroup {self.name} ({self.current_member_count}/{self.maximum_members})>"
