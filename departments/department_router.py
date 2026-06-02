from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import departments.department_service as department_service
from auth.dependencies import get_current_user
from auth.schemas import TokenPayload
from database import get_db
from departments.schemas import DepartmentCreate, DepartmentResponse, DepartmentUpdate

router = APIRouter(prefix="/departments", tags=["departments"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=DepartmentResponse)
async def create(
    body: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    name = body.name
    departments = await department_service.create(db, name)
    return departments


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    tags=["departments"],
    response_model=list[DepartmentResponse],
)
async def get_all(
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    result = await department_service.get_all(db)
    return result


@router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    tags=["departments"],
    response_model=list[DepartmentResponse],
)
async def search_by_name(
    db: AsyncSession = Depends(get_db),
    q: str | None = None,
    current_user: TokenPayload = Depends(get_current_user),
):
    result = await department_service.search_by_name(db, q)
    return result


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    tags=["departments"],
    response_model=DepartmentResponse,
)
async def get_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    result = await department_service.get_by_id(id, db)
    return result


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    tags=["departments"],
    response_model=DepartmentResponse,
)
async def update(
    id: int,
    body: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    name = body.name
    departments = await department_service.update(id, db, name)
    return departments


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    tags=["departments"],
    response_model=DepartmentResponse,
)
async def delete(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    result = await department_service.delete(id, db)
    return result
