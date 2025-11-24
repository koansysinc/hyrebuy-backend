"""
SavedProperty model - User's saved/favorited properties
"""

from sqlalchemy import Column, DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class SavedProperty(Base):
    __tablename__ = "saved_properties"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False)

    # Timestamps
    saved_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    # user = relationship("User", back_populates="saved_properties")
    # property = relationship("Property", back_populates="saved_by")

    # Indexes
    __table_args__ = (
        Index('idx_saved_properties_user', 'user_id'),
        Index('idx_saved_properties_property', 'property_id'),
        Index('idx_saved_properties_unique', 'user_id', 'property_id', unique=True),
    )

    def __repr__(self):
        return f"<SavedProperty User:{self.user_id} -> Property:{self.property_id}>"
