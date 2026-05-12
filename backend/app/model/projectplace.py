import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, UniqueConstraint, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class ProjectPlace(Base):
    __tablename__ = "project_places"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("travel_projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    external_id = Column(Integer, nullable=False)

    title = Column(String(255), nullable=False)
    artist = Column(String(255))
    image_url = Column(String(500))

    notes = Column(Text)
    visited = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    project = relationship(
        "TravelProject",
        back_populates="places",
    )

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "external_id",
            name="uq_project_external_place",
        ),
    )