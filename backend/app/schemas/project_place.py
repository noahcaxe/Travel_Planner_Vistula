import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectPlaceCreate(BaseModel):
    name: str
    address: str | None = None
    latitude: float
    longitude: float
    notes: str | None = None


class ProjectPlaceUpdate(BaseModel):
    notes: str | None = None
    visited: bool | None = None


class ProjectPlaceResponse(BaseModel):
    id: uuid.UUID
    name: str
    address: str | None = None
    latitude: float
    longitude: float
    notes: str | None = None
    visited: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)