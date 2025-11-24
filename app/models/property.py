"""
Property model - Real estate listings
"""

from sqlalchemy import Column, String, BigInteger, Numeric, DateTime, ForeignKey, Text, ARRAY, func, Index
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Property(Base):
    __tablename__ = "properties"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    builder_id = Column(UUID(as_uuid=True), ForeignKey("builders.id"), nullable=False)

    # Basic Info
    name = Column(String(255), nullable=False)
    location = Column(String(100), nullable=False, index=True)  # e.g., "Gachibowli"
    description = Column(Text, nullable=True)

    # Geolocation
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)

    # Configuration
    configuration = Column(String(50), nullable=False)  # e.g., "3BHK", "4BHK"
    carpet_area = Column(String, nullable=False)  # Square feet (as string for Phase 1)
    total_floors = Column(String, nullable=True)
    tower_name = Column(String(100), nullable=True)

    # Pricing
    price = Column(BigInteger, nullable=False, index=True)  # In INR
    price_per_sqft = Column(String, nullable=True)

    # Status
    status = Column(String(20), default="available", index=True)  # available, sold, upcoming

    # Amenities
    amenities = Column(ARRAY(String), nullable=True)  # ["Swimming Pool", "Gym", "Park"]

    # Images
    images = Column(ARRAY(String), nullable=True)  # Array of image URLs

    # Smart Scoring (Phase 1)
    smart_score = Column(Numeric(5, 2), default=0.0)  # 0-100
    location_score = Column(Numeric(5, 2), default=0.0)
    builder_score = Column(Numeric(5, 2), default=0.0)
    price_score = Column(Numeric(5, 2), default=0.0)
    commute_score = Column(Numeric(5, 2), default=0.0)

    # Full-Text Search
    search_vector = Column(TSVECTOR, nullable=True)

    # Group Buying
    available_for_group_buying = Column(String, default="false")  # Boolean as string
    minimum_group_size = Column(String, nullable=True)
    group_discount_tiers = Column(String, nullable=True)  # JSON as string for Phase 1

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    builder = relationship("Builder", back_populates="properties")
    # commute_scores = relationship("CommuteScore", back_populates="property")
    # saved_by = relationship("SavedProperty", back_populates="property")

    # Indexes for fast querying
    __table_args__ = (
        Index('idx_properties_location_price', 'location', 'price'),
        Index('idx_properties_search_vector', 'search_vector', postgresql_using='gin'),
    )

    def __repr__(self):
        return f"<Property {self.name} - {self.location} - ₹{self.price}>"
