"""
Rewards API
Days 36-42: Viral Growth & Rewards System (Phase 3)

Endpoints for points, levels, leaderboard, and gamification
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.database import get_db
from app.services.rewards import RewardsService, POINTS_CONFIG, LEVEL_THRESHOLDS
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(prefix="/rewards", tags=["Rewards"])


# Schemas

class AwardPointsRequest(BaseModel):
    """Request to manually award points (admin)"""
    user_id: str
    action_type: str
    description: Optional[str] = None


class RedeemPointsRequest(BaseModel):
    """Request to redeem points"""
    points: int = Field(..., gt=0)
    description: str


class UserStatsResponse(BaseModel):
    """User reward statistics"""
    user_id: str
    current_level: str
    current_points: int
    lifetime_points: int
    level_achieved_at: str
    next_level_points: Optional[int]
    progress_percent: int
    statistics: dict
    leaderboard_rank: Optional[int]


class LeaderboardEntry(BaseModel):
    """Leaderboard entry"""
    rank: int
    user_id: str
    current_level: str
    lifetime_points: int
    successful_referrals: int
    groups_created: int


class TransactionResponse(BaseModel):
    """Reward transaction"""
    id: str
    action_type: str
    points: int
    description: Optional[str]
    balance_after: int
    created_at: str


# API Endpoints

@router.get("/config")
async def get_rewards_config():
    """
    Get rewards configuration

    Returns points values for different actions and level thresholds
    """
    return {
        "points_config": POINTS_CONFIG,
        "level_thresholds": LEVEL_THRESHOLDS,
        "levels": ["bronze", "silver", "gold", "platinum", "diamond"],
    }


@router.get("/stats/{user_id}", response_model=UserStatsResponse)
async def get_user_stats(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get comprehensive user reward stats

    Phase 3: Gamification
    Shows points, level, progress, and statistics
    """
    try:
        rewards_service = RewardsService(db)
        stats = await rewards_service.get_user_stats(UUID(user_id))

        return UserStatsResponse(**stats)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    Get top users leaderboard

    Phase 3: Gamification
    Shows top users by lifetime points
    """
    try:
        rewards_service = RewardsService(db)
        leaderboard = await rewards_service.get_leaderboard(limit=limit)

        return [LeaderboardEntry(**entry) for entry in leaderboard]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get leaderboard: {str(e)}")


@router.get("/transactions/{user_id}", response_model=List[TransactionResponse])
async def get_transaction_history(
    user_id: str,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """
    Get user's reward transaction history

    Phase 3: Gamification
    Shows all points earned and redeemed
    """
    try:
        rewards_service = RewardsService(db)
        history = await rewards_service.get_transaction_history(UUID(user_id), limit=limit)

        return [TransactionResponse(**txn) for txn in history]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@router.post("/award")
async def award_points(
    request: AwardPointsRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Award points to a user (admin endpoint)

    Phase 3: Gamification
    Manually award points for various actions
    """
    try:
        rewards_service = RewardsService(db)
        result = await rewards_service.award_points(
            user_id=UUID(request.user_id),
            action_type=request.action_type,
            description=request.description,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to award points: {str(e)}")


@router.post("/redeem/{user_id}")
async def redeem_points(
    user_id: str,
    request: RedeemPointsRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Redeem points for rewards

    Phase 3: Gamification
    Convert points to discounts or cashback
    """
    try:
        rewards_service = RewardsService(db)
        result = await rewards_service.redeem_points(
            user_id=UUID(user_id),
            points=request.points,
            description=request.description,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to redeem points: {str(e)}")


@router.get("/my-stats")
async def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get current user's reward stats

    Phase 3: Gamification
    Requires Authentication: Yes (Bearer token)
    """
    try:
        rewards_service = RewardsService(db)
        stats = await rewards_service.get_user_stats(current_user.id)

        return UserStatsResponse(**stats)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.get("/my-transactions")
async def get_my_transactions(
    current_user: User = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """
    Get current user's transaction history

    Phase 3: Gamification
    Requires Authentication: Yes (Bearer token)
    """
    try:
        rewards_service = RewardsService(db)
        history = await rewards_service.get_transaction_history(current_user.id, limit=limit)

        return [TransactionResponse(**txn) for txn in history]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")
