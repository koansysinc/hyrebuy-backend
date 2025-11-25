"""
Referral model - Track user referrals for viral growth
Days 36-42: Viral Growth & Rewards System (Phase 3)
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Index, func, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class Referral(Base):
    __tablename__ = "referrals"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    referrer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    referred_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Referral Details
    referral_code = Column(String(20), nullable=False, index=True)
    source = Column(String(50), nullable=True)  # whatsapp, email, link, group_invite

    # Status Tracking
    status = Column(String(20), default="pending")  # pending, active, converted
    conversion_type = Column(String(50), nullable=True)  # property_view, group_join, property_purchase

    # Rewards
    points_awarded = Column(Integer, default=0)
    points_awarded_to_referrer = Column(Integer, default=0)
    points_awarded_to_referred = Column(Integer, default=0)

    # Timestamps
    referred_at = Column(DateTime(timezone=True), server_default=func.now())
    converted_at = Column(DateTime(timezone=True), nullable=True)

    # Indexes
    __table_args__ = (
        Index('idx_referrals_referrer', 'referrer_id'),
        Index('idx_referrals_referred', 'referred_id'),
        Index('idx_referrals_code', 'referral_code'),
        Index('idx_referrals_status', 'status'),
    )

    def __repr__(self):
        return f"<Referral {self.referrer_id} -> {self.referred_id}>"
