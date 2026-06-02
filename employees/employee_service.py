from sqlalchemy.ext.asyncio import AsyncSession

import employees.employee_repo as employee_repo
from auth.utils import hash_password
from employees.schemas import EmployeeCreate, EmployeeUpdate, UpdateAddress
from exceptions import BadRequestException
from models.employee import Employee


async def create(db: AsyncSession, body: EmployeeCreate):
    if not isinstance(body.name, str) or not body.name.strip():
        raise BadRequestException(detail="name must be a non-empty string")
    if not isinstance(body.email, str) or not body.email.strip():
        raise BadRequestException(detail="email must be a non-empty string")
    hashed = hash_password(body.password)
    employee = await employee_repo.create(db, body, hashed)
    return employee


async def get_all(db: AsyncSession):
    result = await employee_repo.get_all(db)
    return result


async def get_by_id(id: int, db: AsyncSession):
    result = await employee_repo.get_by_id(id, db)
    return result


async def update(id: int, db: AsyncSession, body: EmployeeUpdate):
    if not isinstance(body.name, str) or not body.name.strip():
        raise BadRequestException(detail="name must be a non-empty string")
    if not isinstance(body.email, str) or not body.email.strip():
        raise BadRequestException(detail="email must be a non-empty string")
    result = await employee_repo.update(id, db, body)
    return result


async def patchemployee(id: int, body: EmployeeUpdate, db: AsyncSession):
    result = await employee_repo.patchemployee(id, body, db)
    return result


async def delete(id: int, db: AsyncSession):
    result = await employee_repo.delete(id, db)
    return result


async def search_by_name(db: AsyncSession, q: str | None = None):
    result = await employee_repo.search_by_name(db, q)
    return result


async def map(emp_id: int, dep_id: int, db: AsyncSession):
    return await employee_repo.map(emp_id, dep_id, db)


async def unmap(emp_id: int, dep_id: int, db: AsyncSession):
    return await employee_repo.unmap(emp_id, dep_id, db)


async def removeaddress(emp_id: int, addr_id: int, db: AsyncSession):
    return await employee_repo.removeaddress(emp_id, addr_id, db)


async def updateaddress(
    emp_id: int, addr_id: int, body: UpdateAddress, db: AsyncSession
):
    return await employee_repo.updateaddress(emp_id, addr_id, body, db)


async def get_by_email(email: str, db: AsyncSession) -> Employee | None:
    employee = await employee_repo.get_by_email(email=email, db=db)
    return employee
