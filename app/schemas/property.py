"""
Property schemas for request/response validation
Days 8-9: Property Search (P1-F05, P1-F06)
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class BuilderInfo(BaseModel):
    """Builder information included in property response"""
    id: UUID
    name: str
    rating: Optional[str] = None
    on_time_delivery_percentage: Optional[str] = None

    class Config:
        from_attributes = True


class PropertyResponse(BaseModel):
    """Property response schema for list and detail views"""
    id: UUID
    builder_id: UUID
    name: str
    location: str
    description: Optional[str] = None
    latitude: Decimal
    longitude: Decimal
    configuration: str
    carpet_area: str
    price: int
    price_per_sqft: Optional[str] = None
    status: str
    amenities: Optional[List[str]] = []
    images: Optional[List[str]] = []
    smart_score: Decimal
    location_score: Decimal
    builder_score: Decimal
    price_score: Decimal
    commute_score: Decimal
    available_for_group_buying: str
    minimum_group_size: Optional[str] = None
    group_discount_tiers: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Nested builder info
    builder: Optional[BuilderInfo] = None

    class Config:
        from_attributes = True


class PropertySearchParams(BaseModel):
    """Query parameters for property search"""
    location: Optional[str] = Field(None, description="Filter by location (e.g., 'Gachibowli')")
    min_price: Optional[int] = Field(None, description="Minimum price in INR", ge=0)
    max_price: Optional[int] = Field(None, description="Maximum price in INR", ge=0)
    configuration: Optional[str] = Field(None, description="Filter by configuration (e.g., '3BHK')")
    min_carpet_area: Optional[int] = Field(None, description="Minimum carpet area in sqft", ge=0)
    max_carpet_area: Optional[int] = Field(None, description="Maximum carpet area in sqft", ge=0)
    status: Optional[str] = Field("available", description="Filter by status")
    group_buying_only: Optional[bool] = Field(False, description="Show only group buying properties")
    sort_by: Optional[str] = Field("price", description="Sort field: price, smart_score, created_at")
    sort_order: Optional[str] = Field("asc", description="Sort order: asc or desc")
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(20, ge=1, le=100, description="Items per page")


class PropertyListResponse(BaseModel):
    """Paginated property list response"""
    properties: List[PropertyResponse]
    total: int
    page: int
    limit: int
    total_pages: int
