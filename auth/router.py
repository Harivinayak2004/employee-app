from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import get_current_user
from auth.schemas import LoginRequest, TokenPayload, TokenResponse
from auth import service as auth_service
from auth.utils import create_access_token, decode_access_token
from database.connection import get_db
from exceptions import UnAuthorizedException

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model = TokenResponse )
async def login( form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    token = await auth_service.login( email=form.username, password=form.password, db= db)
    return TokenResponse(access_token=token)



@router.post("/refresh", response_model=TokenResponse)
async def refresh(token: str):
    payload = decode_access_token(token)
    if not payload:
        raise UnAuthorizedException(status_code=401, detail="Invalid or expired token")
    new_token = create_access_token({
        "id": payload["id"],
        "email": payload["email"]
    })

    return TokenResponse(access_token=new_token)



