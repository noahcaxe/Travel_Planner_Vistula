import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.project_place import ProjectPlaceResponse


class TravelProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    start_date: date | None = None


class TravelProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    start_date: date | None = None
    is_completed: bool | None = None


class TravelProjectResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID

    name: str
    description: str | None = None
    start_date: date | None = None
    is_completed: bool

    created_at: datetime
    updated_at: datetime

    places: list[ProjectPlaceResponse]

    model_config = ConfigDict(from_attributes=True)