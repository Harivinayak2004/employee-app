from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from exceptions import NotFoundException
from models.departments import Departments
from sqlalchemy import select
from datetime import datetime

async def create(db: AsyncSession,name:str):
    db_Departments = Departments(name=name.strip())
    db.add(db_Departments)
    await db.commit()
    await db.rollback()
    await db.refresh(db_Departments)
    return db_Departments

async def get_all(db: AsyncSession):
    stmt = select(Departments).where(Departments.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result

async def get_by_id(id:int,db: AsyncSession):
    stmt = select(Departments).where(Departments.deleted_at.is_(None)).where(Departments.id == id)
    result = await db.scalars(stmt)
    db_Departments = result.first()
    return db_Departments


async def update(id:int,db: AsyncSession,name:str):
    stmt = select(Departments).where(Departments.deleted_at.is_(None)).where(Departments.id == id)
    result = await db.scalars(stmt)
    db_Departments = result.first()
    db_Departments.name = name.strip()
    await db.commit()
    await db.rollback()
    await db.refresh(db_Departments)
    return db_Departments

async def delete(id:int,db: AsyncSession):
    stmt = select(Departments).where(Departments.deleted_at.is_(None)).where(Departments.id == id)
    result = await db.scalars(stmt)
    db_Departments = result.first()
    if not db_Departments:
        raise NotFoundException(detail="Departments not found")
    db_Departments.deleted_at = datetime.now()
    await db.commit()
    await db.refresh(db_Departments)
    return db_Departments

async def search_by_name( db: AsyncSession,q:str | None = None):
    stmt = select(Departments).where(Departments.deleted_at.is_(None)).where(Departments.name.ilike(f"%{q}%"))
    result = await db.scalars(stmt)
    return result