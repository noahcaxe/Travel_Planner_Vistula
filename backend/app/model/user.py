from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
 
from app.db.database import Base
 
 
class User(Base):
    __tablename__ = "users"
 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
 
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
 
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
 
    projects = relationship(
        "TravelProject",
        back_populates="user",
        cascade="all, delete-orphan",
    )