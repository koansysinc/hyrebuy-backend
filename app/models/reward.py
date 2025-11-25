"""
Reward and RewardTransaction models - Gamification and points system
Days 36-42: Viral Growth & Rewards System (Phase 3)
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Index, func, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class RewardTransaction(Base):
    __tablename__ = "reward_transactions"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Transaction Details
    action_type = Column(String(50), nullable=False)  # referral, group_created, group_joined, property_saved, property_viewed, deal_closed
    points = Column(Integer, nullable=False)  # Can be positive (earn) or negative (redeem)
    description = Column(Text, nullable=True)

    # Related Entities (optional)
    related_referral_id = Column(UUID(as_uuid=True), ForeignKey("referrals.id"), nullable=True)
    related_group_id = Column(UUID(as_uuid=True), ForeignKey("buying_groups.id"), nullable=True)
    related_property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=True)

    # Balance after transaction
    balance_after = Column(Integer, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_reward_txn_user', 'user_id'),
        Index('idx_reward_txn_action', 'action_type'),
        Index('idx_reward_txn_created', 'created_at'),
    )

    def __repr__(self):
        return f"<RewardTransaction user={self.user_id} points={self.points}>"


class UserRewardLevel(Base):
    __tablename__ = "user_reward_levels"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Key
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)

    # Level Information
    current_level = Column(String(20), default="bronze")  # bronze, silver, gold, platinum, diamond
    current_points = Column(Integer, default=0)
    lifetime_points = Column(Integer, default=0)

    # Statistics
    total_referrals = Column(Integer, default=0)
    successful_referrals = Column(Integer, default=0)
    groups_created = Column(Integer, default=0)
    groups_joined = Column(Integer, default=0)
    properties_viewed = Column(Integer, default=0)
    properties_saved = Column(Integer, default=0)

    # Leaderboard Position
    leaderboard_rank = Column(Integer, nullable=True)

    # Timestamps
    level_achieved_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_user_reward_user', 'user_id'),
        Index('idx_user_reward_level', 'current_level'),
        Index('idx_user_reward_points', 'current_points'),
        Index('idx_user_reward_rank', 'leaderboard_rank'),
    )

    def __repr__(self):
        return f"<UserRewardLevel user={self.user_id} level={self.current_level} points={self.current_points}>"
