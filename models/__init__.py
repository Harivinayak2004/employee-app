"""ORM entities."""

from models.address import Address
from models.departments import Departments
from models.emp_dep import EmpDep
from models.employee import Employee
from models.entity import Entity

__all__ = ["Employee", "Entity", "Address", "Departments", "EmpDep"]
