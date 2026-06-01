"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.employee import Employee
from models.entity import Entity


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class Address(Entity):
    __abstract__ = False
    __tablename__ = "addresses"
    line1: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String[100], nullable=True)
    postal_code: Mapped[str] = mapped_column(String(255), nullable=True)
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="addresses",
    )

    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "line1": self.line1,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
        }
