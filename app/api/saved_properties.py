"""
Saved Properties API
Days 15-17: Saved Properties (P1-F08)

Note: Phase 1 MVP - Using temporary user session without full auth
"""

from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload
from typing import List
from uuid import UUID
import uuid

from app.database import get_db
from app.models.saved_property import SavedProperty
from app.models.property import Property
from app.models.user import User
from app.schemas.property import PropertyResponse
from app.core.deps import get_current_user

router = APIRouter(prefix="/saved-properties", tags=["saved-properties"])


@router.post("/{property_id}")
async def save_property(
    property_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Save a property to user's favorites

    P1-F08: Saved Properties
    Requires Authentication: Yes (Bearer token)
    """
    try:
        # Convert to UUID
        prop_uuid = UUID(property_id)
        user_uuid = current_user.id

        # Check if property exists
        prop_query = select(Property).where(Property.id == prop_uuid)
        result = await db.execute(prop_query)
        property_obj = result.scalar_one_or_none()

        if not property_obj:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )

        # Check if already saved
        existing_query = select(SavedProperty).where(
            and_(
                SavedProperty.user_id == user_uuid,
                SavedProperty.property_id == prop_uuid
            )
        )
        result = await db.execute(existing_query)
        existing = result.scalar_one_or_none()

        if existing:
            return {
                "message": "Property already saved",
                "property_id": property_id,
                "saved": True
            }

        # Create new saved property
        saved_property = SavedProperty(
            user_id=user_uuid,
            property_id=prop_uuid
        )

        db.add(saved_property)
        await db.commit()

        return {
            "message": "Property saved successfully",
            "property_id": property_id,
            "saved": True
        }

    except ValueError:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Invalid property ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving property: {str(e)}"
        )


@router.delete("/{property_id}")
async def unsave_property(
    property_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Remove a property from user's favorites

    P1-F08: Saved Properties
    Requires Authentication: Yes (Bearer token)
    """
    try:
        # Convert to UUID
        prop_uuid = UUID(property_id)
        user_uuid = current_user.id

        # Find saved property
        query = select(SavedProperty).where(
            and_(
                SavedProperty.user_id == user_uuid,
                SavedProperty.property_id == prop_uuid
            )
        )
        result = await db.execute(query)
        saved_property = result.scalar_one_or_none()

        if not saved_property:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Saved property not found"
            )

        await db.delete(saved_property)
        await db.commit()

        return {
            "message": "Property removed from saved list",
            "property_id": property_id,
            "saved": False
        }

    except ValueError:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Invalid property ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing saved property: {str(e)}"
        )


@router.get("", response_model=List[PropertyResponse])
async def get_saved_properties(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all saved properties for user

    P1-F08: Saved Properties
    Requires Authentication: Yes (Bearer token)
    """
    try:
        user_uuid = current_user.id

        # Get saved property IDs
        saved_query = select(SavedProperty.property_id).where(
            SavedProperty.user_id == user_uuid
        )
        result = await db.execute(saved_query)
        saved_property_ids = [row[0] for row in result.fetchall()]

        if not saved_property_ids:
            return []

        # Get full property details with builder info
        properties_query = (
            select(Property)
            .options(joinedload(Property.builder))
            .where(Property.id.in_(saved_property_ids))
            .order_by(Property.created_at.desc())
        )

        result = await db.execute(properties_query)
        properties = result.scalars().unique().all()

        return properties

    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching saved properties: {str(e)}"
        )


@router.get("/check/{property_id}")
async def check_if_saved(
    property_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Check if a property is saved by the user

    P1-F08: Saved Properties
    Requires Authentication: Yes (Bearer token)
    """
    try:
        prop_uuid = UUID(property_id)
        user_uuid = current_user.id

        query = select(SavedProperty).where(
            and_(
                SavedProperty.user_id == user_uuid,
                SavedProperty.property_id == prop_uuid
            )
        )
        result = await db.execute(query)
        saved_property = result.scalar_one_or_none()

        return {
            "property_id": property_id,
            "is_saved": saved_property is not None
        }

    except ValueError:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Invalid property ID format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking saved status: {str(e)}"
        )
