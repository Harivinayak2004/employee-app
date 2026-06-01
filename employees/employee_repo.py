from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from employees.schemas import EmployeeCreate, EmployeeUpdate, UpdateAddress
from models.address import Address
from models.departments import Departments
from models.emp_dep import EmpDep
from models.employee import Employee
from sqlalchemy import select
from datetime import datetime
from exceptions import NotFoundException, ConflictException
from sqlalchemy.orm import selectinload
async def create(db: AsyncSession,body: EmployeeCreate, hashed):
    db_employee = Employee(name=body.name.strip(), email=body.email.strip(),password_hash=hashed,role=body.role)
    if body.addresses:
        for addr in body.addresses:
            db_employee.addresses.append(Address(line1=addr.line1,city=addr.city,postal_code=addr.postal_code,country=addr.country))
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(detail=f"Email '{body.email.strip()}' is already in use")
    await db.refresh(db_employee)
    stmt = (select(Employee).where(Employee.id == db_employee.id).options(selectinload(Employee.addresses)))
    result = await db.scalars(stmt)
    return result.first()

async def get_all(db: AsyncSession):
    stmt = select(Employee).where(Employee.deleted_at.is_(None)).options(selectinload(Employee.addresses))
    result = await db.scalars(stmt)
    return result.all()

async def get_by_id(id:int,db: AsyncSession):
    stmt = select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.id == id).options(selectinload(Employee.addresses))
    result = await db.scalars(stmt)
    db_employee = result.first()
    return db_employee


async def update(id:int,db: AsyncSession,body:EmployeeUpdate):
    stmt = select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.id == id)
    result = await db.scalars(stmt)
    db_employee = result.first()
    db_employee.name = body.name.strip()
    db_employee.email = body.email.strip()
    if not db_employee:
        raise NotFoundException(detail="Employee not found")
    try:
        await db.commit()
    except:
        await db.rollback()
        raise ConflictException(detail=f"Email '{body.email.strip()}' is already in use")
    await db.refresh(db_employee)
    return db_employee

async def delete(id:int,db: AsyncSession):
    stmt = select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.id == id)
    result = await db.scalars(stmt)
    db_employee = result.first()
    if not db_employee:
        raise NotFoundException(detail="Employee not found")
    db_employee.deleted_at = datetime.now()
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

async def search_by_name( db: AsyncSession,q:str | None = None):
    stmt = select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.name.ilike(f"%{q}%")).options(selectinload(Employee.addresses))
    result = await db.scalars(stmt)
    return result.all()

async def get_by_email(email: str,db: AsyncSession) -> Employee | None:
    stmt = select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.email == email).options(selectinload(Employee.addresses))
    result = await db.scalars(stmt)
    db_employee = result.first()
    return db_employee

async def map(emp_id:int, dep_id:int,db: AsyncSession):
    stmt = (select(Employee).where(Employee.id == emp_id).options(selectinload(Employee.departments)))
    result = await db.execute(stmt)
    employee = result.scalar_one_or_none()
    if not employee:
        raise NotFoundException(detail="Employee not found")
    dept = await db.get(Departments, dep_id)
    if not dept:
        raise NotFoundException(detail="Department not found")
    employee.departments.append(dept)
    await db.commit()
    await db.refresh(employee)
    return {"message": "Department attached successfully"}


async def unmap(emp_id:int, dep_id:int,db: AsyncSession):
    employee = await db.get(Employee, emp_id).options(selectinload(Employee.departments))
    if not employee:
        raise NotFoundException(detail="Employee not found")
    dept = await db.get(Departments, dep_id)
    if not dept:
        raise NotFoundException(detail="Department not found")
    employee.departments.remove(dept)
    await db.commit()
    await db.refresh(employee)
    return {"message": "Department attached successfully"}

async def removeaddress(emp_id: int, addr_id:int, db: AsyncSession):
    stmt = (select(Employee).where(Employee.id == emp_id).options(selectinload(Employee.addresses)))
    result = await db.execute(stmt)
    employee = result.scalar_one_or_none()
    if not employee:
        raise NotFoundException(detail="Employee not found")
    address = next(
        (a for a in employee.addresses if a.id == addr_id),
        None
    )
    if not address:
        raise NotFoundException(detail="Address not found")
    employee.addresses.remove(address)

    await db.commit()

    return {"message": "Address removed successfully"}


async def updateaddress(emp_id: int, addr_id: int, body: UpdateAddress, db: AsyncSession):
    stmt = (select(Employee).where(Employee.id == emp_id).options(selectinload(Employee.addresses)))

    result = await db.execute(stmt)
    employee = result.scalar_one_or_none()
    if not employee:
        raise NotFoundException(detail="Employee not found")

    address = next((a for a in employee.addresses if a.id == addr_id),None)
    if not address:
        raise NotFoundException(detail="Address not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)

    await db.commit()
    await db.refresh(address)

    return address


    


