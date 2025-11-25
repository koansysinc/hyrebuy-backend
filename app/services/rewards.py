"""
Rewards Service - Business logic for points and gamification
Days 36-42: Viral Growth & Rewards System (Phase 3)
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict

from app.models.reward import RewardTransaction, UserRewardLevel
from app.models.referral import Referral


# Points configuration
POINTS_CONFIG = {
    "referral_signup": 100,  # When referred user signs up
    "referral_conversion": 500,  # When referred user completes an action
    "group_created": 50,
    "group_joined": 20,
    "property_viewed": 5,
    "property_saved": 10,
    "deal_closed": 1000,
    "welcome_bonus": 50,  # New user welcome bonus
}

# Level thresholds
LEVEL_THRESHOLDS = {
    "bronze": 0,
    "silver": 500,
    "gold": 2000,
    "platinum": 5000,
    "diamond": 10000,
}


class RewardsService:
    """Service for managing rewards and points"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_user_level(self, user_id: UUID) -> UserRewardLevel:
        """Get or create user reward level record"""
        query = select(UserRewardLevel).where(UserRewardLevel.user_id == user_id)
        result = await self.db.execute(query)
        user_level = result.scalar_one_or_none()

        if not user_level:
            # Create new level record
            user_level = UserRewardLevel(
                user_id=user_id,
                current_level="bronze",
                current_points=0,
                lifetime_points=0,
            )
            self.db.add(user_level)
            await self.db.flush()

        return user_level

    async def award_points(
        self,
        user_id: UUID,
        action_type: str,
        description: Optional[str] = None,
        related_referral_id: Optional[UUID] = None,
        related_group_id: Optional[UUID] = None,
        related_property_id: Optional[UUID] = None,
    ) -> Dict:
        """
        Award points to a user for an action
        Returns the transaction details and new balance
        """
        # Get points for action
        points = POINTS_CONFIG.get(action_type, 0)
        if points == 0:
            return {"error": f"Unknown action type: {action_type}"}

        # Get or create user level
        user_level = await self.get_or_create_user_level(user_id)

        # Calculate new balance
        new_balance = user_level.current_points + points
        new_lifetime = user_level.lifetime_points + points

        # Create transaction
        transaction = RewardTransaction(
            user_id=user_id,
            action_type=action_type,
            points=points,
            description=description or f"Earned {points} points for {action_type}",
            related_referral_id=related_referral_id,
            related_group_id=related_group_id,
            related_property_id=related_property_id,
            balance_after=new_balance,
        )
        self.db.add(transaction)

        # Update user level
        user_level.current_points = new_balance
        user_level.lifetime_points = new_lifetime

        # Update stats based on action type
        if action_type == "group_created":
            user_level.groups_created += 1
        elif action_type == "group_joined":
            user_level.groups_joined += 1
        elif action_type == "property_viewed":
            user_level.properties_viewed += 1
        elif action_type == "property_saved":
            user_level.properties_saved += 1

        # Check for level up
        new_level = self._calculate_level(new_lifetime)
        if new_level != user_level.current_level:
            user_level.current_level = new_level
            user_level.level_achieved_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(transaction)
        await self.db.refresh(user_level)

        return {
            "transaction_id": str(transaction.id),
            "points_awarded": points,
            "new_balance": new_balance,
            "new_level": user_level.current_level,
            "level_changed": new_level != user_level.current_level,
        }

    async def redeem_points(
        self, user_id: UUID, points: int, description: str
    ) -> Dict:
        """
        Redeem/deduct points from user account
        Returns the transaction details
        """
        user_level = await self.get_or_create_user_level(user_id)

        if user_level.current_points < points:
            return {"error": "Insufficient points", "available": user_level.current_points}

        # Calculate new balance
        new_balance = user_level.current_points - points

        # Create transaction (negative points)
        transaction = RewardTransaction(
            user_id=user_id,
            action_type="redemption",
            points=-points,
            description=description,
            balance_after=new_balance,
        )
        self.db.add(transaction)

        # Update user balance
        user_level.current_points = new_balance

        await self.db.commit()
        await self.db.refresh(transaction)

        return {
            "transaction_id": str(transaction.id),
            "points_redeemed": points,
            "new_balance": new_balance,
        }

    def _calculate_level(self, lifetime_points: int) -> str:
        """Calculate user level based on lifetime points"""
        if lifetime_points >= LEVEL_THRESHOLDS["diamond"]:
            return "diamond"
        elif lifetime_points >= LEVEL_THRESHOLDS["platinum"]:
            return "platinum"
        elif lifetime_points >= LEVEL_THRESHOLDS["gold"]:
            return "gold"
        elif lifetime_points >= LEVEL_THRESHOLDS["silver"]:
            return "silver"
        else:
            return "bronze"

    async def get_user_stats(self, user_id: UUID) -> Dict:
        """Get comprehensive user reward stats"""
        user_level = await self.get_or_create_user_level(user_id)

        # Get transaction count
        txn_query = select(func.count(RewardTransaction.id)).where(
            RewardTransaction.user_id == user_id
        )
        txn_result = await self.db.execute(txn_query)
        transaction_count = txn_result.scalar()

        # Get referral stats
        ref_query = select(func.count(Referral.id)).where(Referral.referrer_id == user_id)
        ref_result = await self.db.execute(ref_query)
        total_referrals = ref_result.scalar()

        ref_converted_query = select(func.count(Referral.id)).where(
            Referral.referrer_id == user_id, Referral.status == "converted"
        )
        ref_converted_result = await self.db.execute(ref_converted_query)
        successful_referrals = ref_converted_result.scalar()

        # Update user level with referral stats
        user_level.total_referrals = total_referrals
        user_level.successful_referrals = successful_referrals

        await self.db.commit()

        # Calculate progress to next level
        current_level_points = LEVEL_THRESHOLDS[user_level.current_level]
        next_level_points = self._get_next_level_threshold(user_level.current_level)
        progress_percent = 0

        if next_level_points:
            points_needed = next_level_points - current_level_points
            points_earned = user_level.lifetime_points - current_level_points
            progress_percent = int((points_earned / points_needed) * 100)

        return {
            "user_id": str(user_id),
            "current_level": user_level.current_level,
            "current_points": user_level.current_points,
            "lifetime_points": user_level.lifetime_points,
            "level_achieved_at": user_level.level_achieved_at.isoformat(),
            "next_level_points": next_level_points,
            "progress_percent": min(progress_percent, 100),
            "statistics": {
                "total_referrals": total_referrals,
                "successful_referrals": successful_referrals,
                "groups_created": user_level.groups_created,
                "groups_joined": user_level.groups_joined,
                "properties_viewed": user_level.properties_viewed,
                "properties_saved": user_level.properties_saved,
                "total_transactions": transaction_count,
            },
            "leaderboard_rank": user_level.leaderboard_rank,
        }

    def _get_next_level_threshold(self, current_level: str) -> Optional[int]:
        """Get points needed for next level"""
        levels = ["bronze", "silver", "gold", "platinum", "diamond"]
        current_index = levels.index(current_level)

        if current_index < len(levels) - 1:
            next_level = levels[current_index + 1]
            return LEVEL_THRESHOLDS[next_level]

        return None  # Already at max level

    async def get_leaderboard(self, limit: int = 10) -> list:
        """Get top users by lifetime points"""
        query = (
            select(UserRewardLevel)
            .order_by(UserRewardLevel.lifetime_points.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        top_users = result.scalars().all()

        leaderboard = []
        for rank, user_level in enumerate(top_users, start=1):
            # Update rank
            user_level.leaderboard_rank = rank

            leaderboard.append({
                "rank": rank,
                "user_id": str(user_level.user_id),
                "current_level": user_level.current_level,
                "lifetime_points": user_level.lifetime_points,
                "successful_referrals": user_level.successful_referrals,
                "groups_created": user_level.groups_created,
            })

        await self.db.commit()

        return leaderboard

    async def get_transaction_history(
        self, user_id: UUID, limit: int = 50
    ) -> list:
        """Get user's reward transaction history"""
        query = (
            select(RewardTransaction)
            .where(RewardTransaction.user_id == user_id)
            .order_by(RewardTransaction.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        transactions = result.scalars().all()

        history = []
        for txn in transactions:
            history.append({
                "id": str(txn.id),
                "action_type": txn.action_type,
                "points": txn.points,
                "description": txn.description,
                "balance_after": txn.balance_after,
                "created_at": txn.created_at.isoformat(),
            })

        return history
