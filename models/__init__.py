"""ORM entities."""

from models.employee import Employee
from models.entity import Entity
from models.address import Address
from models.departments import Departments
from models.emp_dep import EmpDep

__all__ = ["Employee", "Entity", "Address", "Departments", "EmpDep"]
