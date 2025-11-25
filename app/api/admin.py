"""
Admin API
Days 18-21: Basic Admin Panel (P1-F09)

Note: Phase 1 MVP - No authentication, simple CRUD operations
"""

from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from sqlalchemy.orm import joinedload
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from app.database import get_db
from app.models.property import Property
from app.models.builder import Builder
from app.schemas.property import PropertyResponse

router = APIRouter(prefix="/admin", tags=["admin"])


# Schemas for Admin Operations

class PropertyCreateUpdate(BaseModel):
    """Schema for creating/updating properties"""
    builder_id: str
    name: str
    location: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    configuration: str
    carpet_area: str
    price: int
    price_per_sqft: Optional[str] = None
    amenities: Optional[List[str]] = []
    images: Optional[List[str]] = []
    supports_group_buying: str = "false"
    group_discount_percentage: Optional[str] = None


class AdminStats(BaseModel):
    """Basic admin statistics"""
    total_properties: int
    total_builders: int
    total_saved_properties: int


# Properties Management

@router.get("/properties", response_model=List[PropertyResponse])
async def admin_list_properties(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """
    Get all properties for admin management

    P1-F09: Admin Panel - List Properties
    """
    try:
        query = (
            select(Property)
            .options(joinedload(Property.builder))
            .order_by(Property.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await db.execute(query)
        properties = result.scalars().unique().all()

        return properties

    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching properties: {str(e)}"
        )


@router.post("/properties", response_model=PropertyResponse)
async def admin_create_property(
    property_data: PropertyCreateUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new property

    P1-F09: Admin Panel - Create Property
    """
    try:
        # Verify builder exists
        builder_query = select(Builder).where(Builder.id == UUID(property_data.builder_id))
        result = await db.execute(builder_query)
        builder = result.scalar_one_or_none()

        if not builder:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Builder not found"
            )

        # Create property
        new_property = Property(
            builder_id=UUID(property_data.builder_id),
            name=property_data.name,
            location=property_data.location,
            description=property_data.description,
            latitude=Decimal(str(property_data.latitude)),
            longitude=Decimal(str(property_data.longitude)),
            configuration=property_data.configuration,
            carpet_area=property_data.carpet_area,
            price=property_data.price,
            price_per_sqft=property_data.price_per_sqft,
            amenities=property_data.amenities,
            images=property_data.images,
            supports_group_buying=property_data.supports_group_buying,
            group_discount_percentage=property_data.group_discount_percentage,
            smart_score=Decimal("0.0"),
            location_score=Decimal("0.0"),
            builder_score=Decimal("0.0"),
            price_score=Decimal("0.0"),
            commute_score=Decimal("0.0"),
        )

        db.add(new_property)
        await db.commit()
        await db.refresh(new_property)

        # Load builder relationship
        await db.refresh(new_property, ["builder"])

        return new_property

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating property: {str(e)}"
        )


@router.put("/properties/{property_id}", response_model=PropertyResponse)
async def admin_update_property(
    property_id: str,
    property_data: PropertyCreateUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing property

    P1-F09: Admin Panel - Update Property
    """
    try:
        # Find property
        query = select(Property).where(Property.id == UUID(property_id))
        result = await db.execute(query)
        property_obj = result.scalar_one_or_none()

        if not property_obj:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )

        # Verify builder exists if changed
        if str(property_obj.builder_id) != property_data.builder_id:
            builder_query = select(Builder).where(Builder.id == UUID(property_data.builder_id))
            result = await db.execute(builder_query)
            builder = result.scalar_one_or_none()

            if not builder:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail="Builder not found"
                )

        # Update property fields
        property_obj.builder_id = UUID(property_data.builder_id)
        property_obj.name = property_data.name
        property_obj.location = property_data.location
        property_obj.description = property_data.description
        property_obj.latitude = Decimal(str(property_data.latitude))
        property_obj.longitude = Decimal(str(property_data.longitude))
        property_obj.configuration = property_data.configuration
        property_obj.carpet_area = property_data.carpet_area
        property_obj.price = property_data.price
        property_obj.price_per_sqft = property_data.price_per_sqft
        property_obj.amenities = property_data.amenities
        property_obj.images = property_data.images
        property_obj.supports_group_buying = property_data.supports_group_buying
        property_obj.group_discount_percentage = property_data.group_discount_percentage

        await db.commit()
        await db.refresh(property_obj)

        # Load builder relationship
        await db.refresh(property_obj, ["builder"])

        return property_obj

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating property: {str(e)}"
        )


@router.delete("/properties/{property_id}")
async def admin_delete_property(
    property_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a property

    P1-F09: Admin Panel - Delete Property
    """
    try:
        # Find property
        query = select(Property).where(Property.id == UUID(property_id))
        result = await db.execute(query)
        property_obj = result.scalar_one_or_none()

        if not property_obj:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )

        await db.delete(property_obj)
        await db.commit()

        return {"message": "Property deleted successfully", "property_id": property_id}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting property: {str(e)}"
        )


# Statistics

@router.get("/stats", response_model=AdminStats)
async def admin_get_stats(
    db: AsyncSession = Depends(get_db),
):
    """
    Get basic admin statistics

    P1-F09: Admin Panel - Statistics
    """
    try:
        # Count properties
        properties_result = await db.execute(select(func.count()).select_from(Property))
        total_properties = properties_result.scalar() or 0

        # Count builders
        builders_result = await db.execute(select(func.count(Builder.id)))
        total_builders = builders_result.scalar() or 0

        # Count saved properties
        from app.models.saved_property import SavedProperty
        saved_result = await db.execute(select(func.count(SavedProperty.id)))
        total_saved = saved_result.scalar() or 0

        return AdminStats(
            total_properties=total_properties,
            total_builders=total_builders,
            total_saved_properties=total_saved,
        )

    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching statistics: {str(e)}"
        )


# Builders Management (read-only for Phase 1)

@router.get("/builders")
async def admin_list_builders(
    db: AsyncSession = Depends(get_db),
):
    """
    Get all builders for dropdown/selection

    P1-F09: Admin Panel - List Builders
    """
    try:
        query = select(Builder).order_by(Builder.name)
        result = await db.execute(query)
        builders = result.scalars().all()

        return [
            {
                "id": str(builder.id),
                "name": builder.name,
                "rating": builder.rating,
            }
            for builder in builders
        ]

    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching builders: {str(e)}"
        )
