"""
Referrals API
Days 36-42: Viral Growth & Rewards System (Phase 3)

Endpoints for referral tracking and conversion
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
import string
import random

from app.database import get_db
from app.models.referral import Referral
from app.models.user import User
from app.services.rewards import RewardsService
from app.core.deps import get_current_user

router = APIRouter(prefix="/referrals", tags=["Referrals"])


# Utility function
def generate_referral_code(length: int = 8) -> str:
    """Generate a unique referral code"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# Schemas

class CreateReferralRequest(BaseModel):
    """Request to create a referral"""
    referred_email: str
    source: Optional[str] = "link"  # whatsapp, email, link, group_invite


class ReferralResponse(BaseModel):
    """Referral data response"""
    id: str
    referrer_id: str
    referred_id: Optional[str]
    referral_code: str
    source: Optional[str]
    status: str
    conversion_type: Optional[str]
    points_awarded_to_referrer: int
    points_awarded_to_referred: int
    referred_at: datetime
    converted_at: Optional[datetime]


class ReferralStatsResponse(BaseModel):
    """User referral statistics"""
    user_id: str
    total_referrals: int
    pending_referrals: int
    active_referrals: int
    converted_referrals: int
    total_points_earned: int
    referral_code: str
    referral_link: str


# API Endpoints

@router.get("/my-code")
async def get_my_referral_code(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get current user's referral code

    Phase 3: Viral Growth
    Returns unique referral code for sharing
    Requires Authentication: Yes (Bearer token)
    """
    # Generate referral code based on user ID
    # For simplicity, using user_id[:8] as code
    referral_code = str(current_user.id)[:8].upper()

    return {
        "user_id": str(current_user.id),
        "referral_code": referral_code,
        "referral_link": f"https://hyrebuy.com/signup?ref={referral_code}",
        "whatsapp_share": f"https://wa.me/?text=Join%20HyreBuy%20using%20my%20referral%20code%20{referral_code}%20-%20https://hyrebuy.com/signup?ref={referral_code}",
    }


@router.post("/create", response_model=ReferralResponse)
async def create_referral(
    request: CreateReferralRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new referral

    Phase 3: Viral Growth
    Track when a user refers someone
    Requires Authentication: Yes (Bearer token)
    """
    try:

        # Generate unique referral code
        referral_code = generate_referral_code()

        # Ensure uniqueness
        while True:
            existing = await db.execute(
                select(Referral).where(Referral.referral_code == referral_code)
            )
            if not existing.scalar_one_or_none():
                break
            referral_code = generate_referral_code()

        # Create referral record (referred_id will be set when they sign up)
        new_referral = Referral(
            referrer_id=current_user.id,
            referral_code=referral_code,
            source=request.source,
            status="pending",
        )

        db.add(new_referral)
        await db.commit()
        await db.refresh(new_referral)

        return ReferralResponse(
            id=str(new_referral.id),
            referrer_id=str(new_referral.referrer_id),
            referred_id=str(new_referral.referred_id) if new_referral.referred_id else None,
            referral_code=new_referral.referral_code,
            source=new_referral.source,
            status=new_referral.status,
            conversion_type=new_referral.conversion_type,
            points_awarded_to_referrer=new_referral.points_awarded_to_referrer,
            points_awarded_to_referred=new_referral.points_awarded_to_referred,
            referred_at=new_referral.referred_at,
            converted_at=new_referral.converted_at,
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create referral: {str(e)}")


@router.post("/apply/{referral_code}")
async def apply_referral_code(
    referral_code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Apply a referral code (when new user signs up)

    Phase 3: Viral Growth
    Awards points to both referrer and referred user
    Requires Authentication: Yes (Bearer token)
    """
    try:

        # Find referral by code
        referral_query = select(Referral).where(
            and_(
                Referral.referral_code == referral_code.upper(),
                Referral.status == "pending"
            )
        )
        result = await db.execute(referral_query)
        referral = result.scalar_one_or_none()

        if not referral:
            raise HTTPException(status_code=404, detail="Invalid or expired referral code")

        # Update referral with referred user
        referral.referred_id = current_user.id
        referral.status = "active"

        # Award points to referrer
        rewards_service = RewardsService(db)
        referrer_result = await rewards_service.award_points(
            user_id=referral.referrer_id,
            action_type="referral_signup",
            description=f"Referred a new user",
            related_referral_id=referral.id,
        )

        # Award welcome bonus to referred user
        referred_result = await rewards_service.award_points(
            user_id=current_user.id,
            action_type="welcome_bonus",
            description="Welcome to HyreBuy!",
            related_referral_id=referral.id,
        )

        referral.points_awarded_to_referrer = referrer_result["points_awarded"]
        referral.points_awarded_to_referred = referred_result["points_awarded"]

        await db.commit()

        return {
            "message": "Referral code applied successfully",
            "referral_id": str(referral.id),
            "points_earned_referrer": referrer_result["points_awarded"],
            "points_earned_referred": referred_result["points_awarded"],
        }

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to apply referral: {str(e)}")


@router.post("/convert/{referral_id}")
async def convert_referral(
    referral_id: str,
    conversion_type: str = Query(..., description="property_view, group_join, property_purchase"),
    db: AsyncSession = Depends(get_db),
):
    """
    Mark referral as converted

    Phase 3: Viral Growth
    Awards bonus points when referred user takes action
    """
    try:
        # Find referral
        referral_query = select(Referral).where(Referral.id == UUID(referral_id))
        result = await db.execute(referral_query)
        referral = result.scalar_one_or_none()

        if not referral:
            raise HTTPException(status_code=404, detail="Referral not found")

        if referral.status == "converted":
            raise HTTPException(status_code=400, detail="Referral already converted")

        # Update referral status
        referral.status = "converted"
        referral.conversion_type = conversion_type
        referral.converted_at = datetime.utcnow()

        # Award conversion bonus to referrer
        rewards_service = RewardsService(db)
        conversion_result = await rewards_service.award_points(
            user_id=referral.referrer_id,
            action_type="referral_conversion",
            description=f"Referred user completed: {conversion_type}",
            related_referral_id=referral.id,
        )

        referral.points_awarded += conversion_result["points_awarded"]
        referral.points_awarded_to_referrer += conversion_result["points_awarded"]

        await db.commit()

        return {
            "message": "Referral converted successfully",
            "referral_id": str(referral.id),
            "conversion_type": conversion_type,
            "bonus_points": conversion_result["points_awarded"],
        }

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to convert referral: {str(e)}")


@router.get("/my-stats", response_model=ReferralStatsResponse)
async def get_my_referral_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get current user's referral statistics

    Phase 3: Viral Growth
    Shows referral performance metrics
    Requires Authentication: Yes (Bearer token)
    """
    try:

        # Get referral stats
        referrals_query = select(Referral).where(Referral.referrer_id == current_user.id)
        result = await db.execute(referrals_query)
        referrals = result.scalars().all()

        total_referrals = len(referrals)
        pending_referrals = sum(1 for r in referrals if r.status == "pending")
        active_referrals = sum(1 for r in referrals if r.status == "active")
        converted_referrals = sum(1 for r in referrals if r.status == "converted")
        total_points_earned = sum(r.points_awarded_to_referrer for r in referrals)

        # Generate referral code
        referral_code = str(current_user.id)[:8].upper()

        return ReferralStatsResponse(
            user_id=str(current_user.id),
            total_referrals=total_referrals,
            pending_referrals=pending_referrals,
            active_referrals=active_referrals,
            converted_referrals=converted_referrals,
            total_points_earned=total_points_earned,
            referral_code=referral_code,
            referral_link=f"https://hyrebuy.com/signup?ref={referral_code}",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.get("/list", response_model=List[ReferralResponse])
async def list_my_referrals(
    current_user: User = Depends(get_current_user),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """
    List current user's referrals

    Phase 3: Viral Growth
    Shows all referrals made by user
    Requires Authentication: Yes (Bearer token)
    """
    try:

        # Build query
        query = select(Referral).where(Referral.referrer_id == current_user.id)

        if status:
            query = query.where(Referral.status == status)

        query = query.order_by(Referral.referred_at.desc()).limit(limit)

        result = await db.execute(query)
        referrals = result.scalars().all()

        return [
            ReferralResponse(
                id=str(r.id),
                referrer_id=str(r.referrer_id),
                referred_id=str(r.referred_id) if r.referred_id else None,
                referral_code=r.referral_code,
                source=r.source,
                status=r.status,
                conversion_type=r.conversion_type,
                points_awarded_to_referrer=r.points_awarded_to_referrer,
                points_awarded_to_referred=r.points_awarded_to_referred,
                referred_at=r.referred_at,
                converted_at=r.converted_at,
            )
            for r in referrals
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list referrals: {str(e)}")
