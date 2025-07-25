from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import create_user
from app.schemas.user_schema import UserLogin
from app.services.auth_service import login_user
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await create_user(user, db)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        # Puedes usar el email como identificador para buscar por email o username
        logged_user = await login_user(user.email, user.password, db)
        return logged_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))