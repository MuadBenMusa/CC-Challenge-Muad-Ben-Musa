from typing import Literal

from fastapi import APIRouter,HTTPException, status as http_status

from .schemas import ProjectCreate, ProjectRead
from .service import create_project, get_projects, CustomerNotFoundError

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectRead])
async def get_all_projects(
    status: Literal["open", "in progress", "done"] | None = None,
) -> list[ProjectRead]:
    return await get_projects(status)


@router.post(
    "",
    response_model=ProjectRead,
    status_code=http_status.HTTP_201_CREATED,
)
async def post_project(project: ProjectCreate) -> ProjectRead:
    try:
        return await create_project(project)
    except CustomerNotFoundError as exc:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Customer does not exist.",
        ) from exc