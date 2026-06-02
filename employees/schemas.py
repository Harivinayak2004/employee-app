from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    model_validator,
    EmailStr,
)
from datetime import datetime

from models.employee import EmployeeRole


class AddressCreate(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Postal code must contain only digits (0-9)")
        return v

    @model_validator(mode="after")
    def postal_code_length_for_country(self):

        country = self.country.strip().upper()

        n = len(self.postal_code)

        if country in ("US", "USA") and n != 5:
            raise ValueError("US ZIP codes must be exactly 5 digits")

        elif country == "IN" and n != 6:
            raise ValueError("Indian PIN codes must be exactly 6 digits")

        return self


class UpdateAddress(BaseModel):
    line1: str | None = None
    city: str | None = None
    postal_code: str | None = None
    country: str | None = None


class AddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    line1: str
    city: str
    postal_code: str
    country: str


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)
    email: EmailStr
    age: int | None = Field(default=None, ge=18, le=100)
    addresses: list[AddressCreate] | None = None
    password: str = Field(min_length=6)
    role: EmployeeRole


class EmployeeUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)
    email: EmailStr
    age: int | None = Field(default=None, ge=18, le=100)
    addresses: list[AddressCreate] | None = None
    role: EmployeeRole


class EmployeePatch(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str | None = Field(default=None, min_length=1)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=18, le=100)
    addresses: list[AddressCreate] | None = None
    role: EmployeeRole | None = None


class EmployeeResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    addresses: list[AddressResponse] = []
    age: int | None = None
    role: EmployeeRole


class EmployeeResponseSchema2(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int | None = Field(default=None, ge=18, le=100)
    addresses: list[AddressResponse] = []
    role: EmployeeRole
    created_at: datetime | None
    updated_at: datetime | None
