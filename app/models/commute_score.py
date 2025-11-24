"""
CommuteScore model - Pre-calculated commute times between properties and GCC offices
"""

from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class CommuteScore(Base):
    __tablename__ = "commute_scores"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("gcc_companies.id"), nullable=False)

    # Commute Data (from OSRM API)
    distance_km = Column(Numeric(8, 2), nullable=False)  # Distance in kilometers
    duration_seconds = Column(String, nullable=False)  # Base duration from OSRM (as string)

    # Time-of-Day Estimates
    normal_minutes = Column(String, nullable=False)  # Normal traffic
    peak_morning_minutes = Column(String, nullable=False)  # 8-10 AM (1.5x multiplier)
    peak_evening_minutes = Column(String, nullable=False)  # 6-8 PM (1.6x multiplier)

    # Current estimate (used for display)
    current_minutes = Column(String, nullable=False)

    # Traffic Level (for UI indicators)
    traffic_level = Column(String(20), default="normal")  # normal, moderate, heavy

    # Calculation Metadata
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    osrm_response = Column(String, nullable=True)  # Store raw OSRM response (JSON as string)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    # property = relationship("Property", back_populates="commute_scores")
    # company = relationship("GCCCompany")

    # Index for fast lookups
    __table_args__ = (
        Index('idx_commute_scores_property', 'property_id'),
        Index('idx_commute_scores_company', 'company_id'),
        Index('idx_commute_scores_property_company', 'property_id', 'company_id', unique=True),
    )

    def __repr__(self):
        return f"<CommuteScore Property:{self.property_id} -> Company:{self.company_id} = {self.current_minutes} min>"
