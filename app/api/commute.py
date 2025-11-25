"""
Commute API
Days 22-24: Commute Calculator

Calculate and cache commute times from work location to properties
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

from app.database import get_db
from app.models.commute import CommuteCache
from app.models.property import Property
from app.services.maps import get_maps_service

router = APIRouter(prefix="/commute", tags=["Commute"])


# Schemas

class CommuteRequest(BaseModel):
    """Request to calculate commute"""
    origin_lat: float = Field(..., description="Work location latitude")
    origin_lng: float = Field(..., description="Work location longitude")
    dest_lat: float = Field(..., description="Property latitude")
    dest_lng: float = Field(..., description="Property longitude")
    mode: str = Field(default="driving", description="Travel mode: driving, transit, walking, bicycling")


class CommuteResponse(BaseModel):
    """Commute calculation result"""
    distance_meters: int
    distance_text: str
    duration_seconds: int
    duration_text: str
    duration_in_traffic_seconds: Optional[int] = None
    duration_in_traffic_text: Optional[str] = None
    travel_mode: str
    from_cache: bool = Field(description="Whether result was retrieved from cache")


class PropertyCommuteRequest(BaseModel):
    """Request to calculate commute to a specific property"""
    property_id: str
    origin_lat: float
    origin_lng: float
    mode: str = "driving"


# API Endpoints

@router.post("/calculate", response_model=CommuteResponse)
async def calculate_commute(
    request: CommuteRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Calculate commute between two points

    Phase 2: Commute Calculator
    Uses mock data by default to avoid API costs during development
    """
    try:
        # Check cache first
        tolerance = 0.001  # ~111 meters tolerance
        cache_query = select(CommuteCache).where(
            CommuteCache.origin_lat.between(request.origin_lat - tolerance, request.origin_lat + tolerance),
            CommuteCache.origin_lng.between(request.origin_lng - tolerance, request.origin_lng + tolerance),
            CommuteCache.dest_lat.between(request.dest_lat - tolerance, request.dest_lat + tolerance),
            CommuteCache.dest_lng.between(request.dest_lng - tolerance, request.dest_lng + tolerance),
            CommuteCache.travel_mode == request.mode
        )

        result = await db.execute(cache_query)
        cached = result.scalar_one_or_none()

        if cached:
            # Return cached result
            return CommuteResponse(
                distance_meters=cached.distance_meters,
                distance_text=cached.distance_text,
                duration_seconds=cached.duration_seconds,
                duration_text=cached.duration_text,
                duration_in_traffic_seconds=cached.duration_in_traffic_seconds,
                duration_in_traffic_text=cached.duration_in_traffic_text,
                travel_mode=cached.travel_mode,
                from_cache=True
            )

        # Calculate new commute
        maps_service = get_maps_service(use_mock=True)  # Use mock for now
        commute_data = maps_service.calculate_commute(
            origin_lat=request.origin_lat,
            origin_lng=request.origin_lng,
            dest_lat=request.dest_lat,
            dest_lng=request.dest_lng,
            mode=request.mode
        )

        # Cache the result
        cache_entry = CommuteCache(
            origin_lat=request.origin_lat,
            origin_lng=request.origin_lng,
            dest_lat=request.dest_lat,
            dest_lng=request.dest_lng,
            travel_mode=request.mode,
            distance_meters=commute_data['distance_meters'],
            distance_text=commute_data['distance_text'],
            duration_seconds=commute_data['duration_seconds'],
            duration_text=commute_data['duration_text'],
            duration_in_traffic_seconds=commute_data.get('duration_in_traffic_seconds'),
            duration_in_traffic_text=commute_data.get('duration_in_traffic_text'),
        )

        db.add(cache_entry)
        await db.commit()

        return CommuteResponse(
            distance_meters=commute_data['distance_meters'],
            distance_text=commute_data['distance_text'],
            duration_seconds=commute_data['duration_seconds'],
            duration_text=commute_data['duration_text'],
            duration_in_traffic_seconds=commute_data.get('duration_in_traffic_seconds'),
            duration_in_traffic_text=commute_data.get('duration_in_traffic_text'),
            travel_mode=request.mode,
            from_cache=False
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Commute calculation failed: {str(e)}")


@router.post("/property", response_model=CommuteResponse)
async def calculate_property_commute(
    request: PropertyCommuteRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Calculate commute to a specific property

    Phase 2: Commute Calculator
    Convenience endpoint that looks up property coordinates
    """
    try:
        # Get property
        from uuid import UUID
        property_query = select(Property).where(Property.id == UUID(request.property_id))
        result = await db.execute(property_query)
        property_obj = result.scalar_one_or_none()

        if not property_obj:
            raise HTTPException(status_code=404, detail="Property not found")

        # Calculate commute
        commute_request = CommuteRequest(
            origin_lat=request.origin_lat,
            origin_lng=request.origin_lng,
            dest_lat=float(property_obj.latitude),
            dest_lng=float(property_obj.longitude),
            mode=request.mode
        )

        return await calculate_commute(commute_request, db)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate property commute: {str(e)}")


@router.get("/batch")
async def calculate_batch_commutes(
    origin_lat: float = Query(..., description="Work location latitude"),
    origin_lng: float = Query(..., description="Work location longitude"),
    property_ids: str = Query(..., description="Comma-separated property IDs"),
    mode: str = Query(default="driving", description="Travel mode"),
    db: AsyncSession = Depends(get_db),
):
    """
    Calculate commutes to multiple properties at once

    Phase 2: Commute Calculator
    Useful for showing commute times on property list pages
    """
    try:
        from uuid import UUID

        # Parse property IDs
        ids = [UUID(pid.strip()) for pid in property_ids.split(',')]

        # Get properties
        properties_query = select(Property).where(Property.id.in_(ids))
        result = await db.execute(properties_query)
        properties = result.scalars().all()

        if not properties:
            return []

        # Calculate commutes
        results = []
        for prop in properties:
            try:
                commute_request = CommuteRequest(
                    origin_lat=origin_lat,
                    origin_lng=origin_lng,
                    dest_lat=float(prop.latitude),
                    dest_lng=float(prop.longitude),
                    mode=mode
                )
                commute = await calculate_commute(commute_request, db)

                results.append({
                    "property_id": str(prop.id),
                    "property_name": prop.name,
                    "commute": commute
                })
            except Exception as e:
                # Skip failed calculations
                print(f"Failed to calculate commute for {prop.name}: {e}")
                continue

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch calculation failed: {str(e)}")
