"""
Builder model - Real estate builders/developers
Examples: Aparna, My Home, Aliens, Mantri, Sobha, etc.
"""

from sqlalchemy import Column, String, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class Builder(Base):
    __tablename__ = "builders"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Builder Info
    name = Column(String(255), nullable=False, unique=True)  # e.g., "Aparna Constructions"
    full_name = Column(String(255), nullable=True)
    description = Column(String, nullable=True)

    # Ratings
    rating = Column(Numeric(3, 2), default=0.0)  # e.g., 4.5 out of 5
    on_time_delivery_percentage = Column(Numeric(5, 2), default=0.0)  # e.g., 92.00%

    # Contact Info
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)

    # Group Buying Settings (Phase 1)
    accepts_group_buying = Column(String, default="false")  # Boolean as string for Phase 1
    minimum_group_size = Column(String, default="5")
    maximum_discount_percent = Column(Numeric(5, 2), default=30.00)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    # properties = relationship("Property", back_populates="builder")

    def __repr__(self):
        return f"<Builder {self.name} (Rating: {self.rating})>"
