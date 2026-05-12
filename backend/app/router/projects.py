import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_current_user_id, get_project_service
from app.schemas.project import TravelProjectCreate, TravelProjectResponse, TravelProjectUpdate
from app.service.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=TravelProjectResponse, status_code=201)
async def create_project(
    data: TravelProjectCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    project_service: ProjectService = Depends(get_project_service),
):
    return await project_service.create(user_id, data)


@router.get("", response_model=list[TravelProjectResponse])
async def list_projects(
    user_id: uuid.UUID = Depends(get_current_user_id),
    project_service: ProjectService = Depends(get_project_service),
):
    return await project_service.list_by_user(user_id)


@router.get("/{project_id}", response_model=TravelProjectResponse)
async def get_project(
    project_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    project_service: ProjectService = Depends(get_project_service),
):
    try:
        return await project_service.get_by_id(project_id, user_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{project_id}", response_model=TravelProjectResponse)
async def update_project(
    project_id: uuid.UUID,
    data: TravelProjectUpdate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    project_service: ProjectService = Depends(get_project_service),
):
    try:
        return await project_service.update(project_id, user_id, data)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    project_service: ProjectService = Depends(get_project_service),
):
    try:
        await project_service.delete(project_id, user_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))