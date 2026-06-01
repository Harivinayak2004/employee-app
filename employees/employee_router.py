from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from auth.dependencies import get_current_user, require_role
from auth.schemas import TokenPayload
from models.employee import Employee, EmployeeRole
import employees.employee_service as employee_service
from database import get_db
import logging
from employees.schemas import EmployeeCreate, EmployeeResponseSchema, EmployeeResponseSchema2, EmployeeUpdate, UpdateAddress


router = APIRouter(prefix="/employee", tags=["Employees"])
@router.post("/{emp_id}/departments/{dep_id}",)
async def map(emp_id:int, dep_id:int,db: AsyncSession = Depends(get_db),current_user: TokenPayload = Depends(get_current_user)):

    return await employee_service.map(emp_id,dep_id,db)

@router.delete("/{emp_id}/departments/{dep_id}")
async def unmap(emp_id:int, dep_id:int,db: AsyncSession = Depends(get_db),current_user: TokenPayload = Depends(get_current_user)):
    return await employee_service.map(emp_id,dep_id,db)

@router.delete("/{emp_id}/addresses/{addr_id}")
async def removeaddress(emp_id: int, addr_id:int, db: AsyncSession = Depends(get_db),current_user: TokenPayload = Depends(get_current_user)):
    return await employee_service.removeaddress(emp_id,addr_id,db)

@router.put("/{emp_id}/addresses/{addr_id}")
async def updateaddress(emp_id: int, addr_id:int,body: UpdateAddress, db: AsyncSession = Depends(get_db)):
    return await employee_service.updateaddress(emp_id,addr_id,body,db)

@router.get("/{emp_id}/addresses")
async def getaddress(emp_id: int, db: AsyncSession = Depends(get_db)):
    return await employee_service.getaddress(emp_id,db)

@router.post("",status_code=status.HTTP_201_CREATED,response_model=EmployeeResponseSchema,dependencies=[Depends(require_role(EmployeeRole.HR))])
async def create(body: EmployeeCreate,db: AsyncSession = Depends(get_db)):
    employee = await employee_service.create(db,body)
    return employee

@router.get("", status_code=status.HTTP_200_OK,tags=["Employees"],response_model=list[EmployeeResponseSchema])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await employee_service.get_all(db)
    return result

@router.get("/search",status_code=status.HTTP_200_OK,tags=["Employees"],response_model=list[EmployeeResponseSchema])
async def search_by_name( db: AsyncSession = Depends(get_db),q:str | None = None):
    result = await employee_service.search_by_name(db,q)
    return result

@router.get("/{id}", tags=["Employees"],status_code=status.HTTP_200_OK,response_model=EmployeeResponseSchema2)
async def get_by_id(id:int,db: AsyncSession = Depends(get_db),current_user: TokenPayload = Depends(get_current_user)):
    result = await employee_service.get_by_id(id,db)
    return result

@router.put("/{id}",tags=["Employees"],status_code=status.HTTP_200_OK,response_model=EmployeeResponseSchema)
async def update(id:int,body: EmployeeUpdate,db: AsyncSession = Depends(get_db),current_user: TokenPayload = Depends(get_current_user)):
    name = body.name
    email = body.email
    employee = await employee_service.update(id,db, body)
    return employee

@router.delete("/{id}",tags=["Employees"],status_code=status.HTTP_200_OK,response_model=EmployeeResponseSchema)
async def delete(id:int,db: AsyncSession = Depends(get_db),current_user: TokenPayload = Depends(get_current_user)):
    result = await employee_service.delete(id,db)
    return result

@router.get("/email/{email}",tags=["Employees"],response_model=EmployeeResponseSchema)
async def get_by_email(email:str,db:AsyncSession= Depends(get_db)):
    employee=await employee_service.get_by_email(email=email,db=db)
    return employee


