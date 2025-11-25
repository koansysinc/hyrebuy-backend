"""
Commute Cache Model
Days 22-24: Commute Calculator Backend

Caches commute calculations to avoid repeated API calls
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.database import Base


class CommuteCache(Base):
    """
    Cache for commute time calculations

    Stores results from Google Maps Distance Matrix API
    to avoid repeated API calls and reduce costs
    """
    __tablename__ = "commute_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Origin (work location)
    origin_lat = Column(Float, nullable=False, comment="Work location latitude")
    origin_lng = Column(Float, nullable=False, comment="Work location longitude")

    # Destination (property location)
    dest_lat = Column(Float, nullable=False, comment="Property latitude")
    dest_lng = Column(Float, nullable=False, comment="Property longitude")

    # Travel mode (driving, transit, walking, bicycling)
    travel_mode = Column(String(20), nullable=False, default="driving")

    # Commute details
    distance_meters = Column(Integer, nullable=False, comment="Distance in meters")
    distance_text = Column(String(50), nullable=False, comment="Human-readable distance")

    duration_seconds = Column(Integer, nullable=False, comment="Duration in seconds")
    duration_text = Column(String(50), nullable=False, comment="Human-readable duration")

    # Duration in traffic (for driving mode)
    duration_in_traffic_seconds = Column(Integer, nullable=True, comment="Duration with traffic")
    duration_in_traffic_text = Column(String(50), nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Indexes for fast lookups
    __table_args__ = (
        Index(
            'idx_commute_lookup',
            'origin_lat', 'origin_lng',
            'dest_lat', 'dest_lng',
            'travel_mode'
        ),
    )

    def __repr__(self):
        return f"<CommuteCache {self.origin_lat},{self.origin_lng} -> {self.dest_lat},{self.dest_lng}: {self.duration_text}>"
