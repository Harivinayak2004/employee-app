from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import verify_password, create_access_token
from employees import employee_repo
from exceptions import UnAuthorizedException
from models.employee import Employee

async def login(db: AsyncSession, email: str, password: str) -> Employee | None:
    employee = await employee_repo.get_by_email(email=email, db=db)
    if employee is None:
        raise UnAuthorizedException("Invalid email or password")
    
    if not verify_password(password, employee.password_hash):
        raise UnAuthorizedException("Inavid email or password")
    
    return create_access_token({"id": employee.id, "email" : employee.email, "role" : employee.role.value})