import logging

from fastapi import FastAPI

from auth.router import router as auth_router
from config import settings
from departments.department_router import router as department_router
from employees.employee_router import router as employee_router
from exceptions.handlers import register_exception_handlers
from middleware import configure_middleware

app = FastAPI(
    title="Employee app", description="This is a employee application", version="1.3.0"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


configure_middleware(app)
register_exception_handlers(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "env": settings.app_env}


app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(department_router)

# @app.get("/employees/{id}", tags=["Employees"])
# async def get_by_id(id:int,db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.id == id)
#     result = await db.scalars(stmt)
#     db_employee = result.first()
#     return db_employee.to_api_dict()

# @app.put("/employees/{id}",status_code=200, tags=["Employees"])
# async def update_employee(id:int,body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.id == id)
#     result = await db.scalars(stmt)
#     name = body.get("name")
#     email = body.get("email")
#     db_employee = result.first()
#     if not db_employee:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     if not isinstance(name, str) or not name.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#     if not isinstance(email, str) or not email.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
#     db_employee.name = name.strip()
#     db_employee.email = email.strip()
#     try:
#         await db.commit()
#     except:
#         await db.rollback(db_employee)
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()


# ----Patch----
# @app.patch("/employees/{id}",status_code=200, tags=["Employees"])
# async def update_employee(id:int,body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.id == id)
#     allowed_fields = ["name","email"]
#     result = await db.scalars(stmt)
#     db_employee = result.first()
#     if not db_employee:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     for x,y in body.items():
#         if x not in allowed_fields:
#             raise HTTPException(status_code=404, detail="Employee not found")
#         setattr(db_employee, x, y)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.refresh(db_employee)
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{db_employee.email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()

# @app.delete("/employees/{id}",tags=["Employees"])
# async def delete_employee(id:int, db:AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.id == id)
#     result = await db.scalars(stmt)
#     db_employee = result.first()
#     if not db_employee:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     db_employee.deleted_at = datetime.now()
#     await db.commit()
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()
