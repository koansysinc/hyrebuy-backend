"""
Property API endpoints
Days 8-9: Property Search (P1-F05, P1-F06)

Endpoints:
- GET /properties - Search and filter properties with pagination
- GET /properties/{id} - Get single property detail (Day 10-11)
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import joinedload
from typing import Optional
import math

from app.database import get_db
from app.schemas.property import (
    PropertyResponse,
    PropertyListResponse,
    PropertySearchParams,
)
from app.models.property import Property
from app.models.builder import Builder

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("", response_model=PropertyListResponse)
async def search_properties(
    location: Optional[str] = Query(None, description="Filter by location"),
    min_price: Optional[int] = Query(None, ge=0, description="Minimum price in INR"),
    max_price: Optional[int] = Query(None, ge=0, description="Maximum price in INR"),
    configuration: Optional[str] = Query(None, description="Filter by configuration (e.g., '3BHK')"),
    min_carpet_area: Optional[int] = Query(None, ge=0, description="Minimum carpet area"),
    max_carpet_area: Optional[int] = Query(None, ge=0, description="Maximum carpet area"),
    status: str = Query("available", description="Filter by status"),
    group_buying_only: bool = Query(False, description="Show only group buying properties"),
    sort_by: str = Query("price", description="Sort field: price, smart_score, created_at"),
    sort_order: str = Query("asc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
):
    """
    Search and filter properties with pagination

    P1-F05: Property Search API

    Filters:
    - location: Exact match on location name
    - min_price/max_price: Price range filter
    - configuration: Exact match on configuration (2BHK, 3BHK, 4BHK)
    - min_carpet_area/max_carpet_area: Carpet area range
    - status: Property status (available, sold, upcoming)
    - group_buying_only: Only show properties with group buying support

    Sorting:
    - price: Sort by price (default)
    - smart_score: Sort by smart score
    - created_at: Sort by creation date

    Pagination:
    - page: Page number (default 1)
    - limit: Items per page (default 20, max 100)
    """
    try:
        # Build base query with builder join
        query = select(Property).options(joinedload(Property.builder))

        # Apply filters
        filters = []

        if location:
            filters.append(Property.location.ilike(f"%{location}%"))

        if min_price is not None:
            filters.append(Property.price >= min_price)

        if max_price is not None:
            filters.append(Property.price <= max_price)

        if configuration:
            filters.append(Property.configuration.ilike(f"%{configuration}%"))

        if min_carpet_area is not None:
            # carpet_area is stored as string, convert for comparison
            # Filter properties where carpet_area can be cast to int and is >= min_carpet_area
            # Note: This is a simplified approach for Phase 1 MVP
            filters.append(Property.carpet_area.cast(func.integer) >= min_carpet_area)

        if max_carpet_area is not None:
            filters.append(Property.carpet_area.cast(func.integer) <= max_carpet_area)

        if status:
            filters.append(Property.status == status)

        if group_buying_only:
            filters.append(Property.available_for_group_buying == "true")

        # Apply all filters
        if filters:
            query = query.where(and_(*filters))

        # Get total count (before pagination)
        count_query = select(func.count()).select_from(Property)
        if filters:
            count_query = count_query.where(and_(*filters))

        result = await db.execute(count_query)
        total = result.scalar() or 0

        # Apply sorting
        if sort_order.lower() == "desc":
            order_column = getattr(Property, sort_by).desc()
        else:
            order_column = getattr(Property, sort_by).asc()

        query = query.order_by(order_column)

        # Apply pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        # Execute query
        result = await db.execute(query)
        properties = result.scalars().unique().all()

        # Calculate total pages
        total_pages = math.ceil(total / limit) if total > 0 else 0

        return PropertyListResponse(
            properties=properties,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching properties: {str(e)}"
        )


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get single property by ID

    P1-F07: Property Detail Page (Days 10-11)
    """
    try:
        query = select(Property).options(joinedload(Property.builder)).where(Property.id == property_id)
        result = await db.execute(query)
        property_obj = result.scalar_one_or_none()

        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )

        return property_obj

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching property: {str(e)}"
        )
