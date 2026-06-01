from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from exceptions import BadRequestException
from models.departments import Departments
import departments.department_repo as department_repo

async def create(db: AsyncSession,name:str):
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException(detail="name must be a non-empty string")
    departments = await department_repo.create(db, name.strip())
    return departments

async def get_all(db: AsyncSession):
    result = await department_repo.get_all(db)
    return result

async def get_by_id(id:int,db: AsyncSession):
    result = await department_repo.get_by_id(id,db)
    return result

async def update(id:int,db: AsyncSession, name:str):
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException(detail="name must be a non-empty string")
    result = await department_repo.update(id,db,name)
    return result

async def delete(id:int,db: AsyncSession):
    result = await department_repo.delete(id,db)
    return result

async def search_by_name( db: AsyncSession,q:str | None = None):
    result = await department_repo.search_by_name(db,q)
    return result