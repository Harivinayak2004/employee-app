from pydantic import BaseModel, EmailStr

from models.employee import EmployeeRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    id: int
    email: str
    role: EmployeeRole