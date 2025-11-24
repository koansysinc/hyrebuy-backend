"""
GCC Company model - Major tech company offices in Hyderabad
Examples: Amazon, Google, Microsoft, Apple, Meta, etc.
"""

from sqlalchemy import Column, String, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class GCCCompany(Base):
    __tablename__ = "gcc_companies"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Company Info
    name = Column(String(255), nullable=False, unique=True)  # e.g., "Amazon"
    full_name = Column(String(255), nullable=True)  # e.g., "Amazon Development Centre India"
    location = Column(String(255), nullable=False)  # e.g., "Gachibowli, Hyderabad"

    # Geolocation (for commute calculation)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)

    # Additional Info
    office_address = Column(String(500), nullable=True)
    employee_count = Column(String, nullable=True)  # Approximate count

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    def __repr__(self):
        return f"<GCCCompany {self.name} - {self.location}>"
