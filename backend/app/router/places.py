import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_current_user_id, get_place_service
from app.schemas.project_place import ProjectPlaceCreate, ProjectPlaceResponse, ProjectPlaceUpdate
from app.service.project_place_service import ProjectPlaceService

router = APIRouter(prefix="/projects/{project_id}/places", tags=["places"])


@router.post("", response_model=ProjectPlaceResponse, status_code=201)
async def add_place(
    project_id: uuid.UUID,
    data: ProjectPlaceCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    place_service: ProjectPlaceService = Depends(get_place_service),
):
    try:
        return await place_service.add_place(project_id, user_id, data.external_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        msg = str(e)
        if "not found in Art Institute" in msg:
            raise HTTPException(status_code=422, detail=msg)
        if "already exists" in msg or "more than 10" in msg:
            raise HTTPException(status_code=409, detail=msg)
        raise HTTPException(status_code=404, detail=msg)


@router.get("", response_model=list[ProjectPlaceResponse])
async def list_places(
    project_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    place_service: ProjectPlaceService = Depends(get_place_service),
):
    try:
        return await place_service.list_places(project_id, user_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{place_id}", response_model=ProjectPlaceResponse)
async def update_place(
    project_id: uuid.UUID,
    place_id: uuid.UUID,
    data: ProjectPlaceUpdate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    place_service: ProjectPlaceService = Depends(get_place_service),
):
    try:
        return await place_service.update_place(place_id, user_id, data)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{place_id}", status_code=204)
async def delete_place(
    project_id: uuid.UUID,
    place_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    place_service: ProjectPlaceService = Depends(get_place_service),
):
    try:
        await place_service.delete_place(place_id, user_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))