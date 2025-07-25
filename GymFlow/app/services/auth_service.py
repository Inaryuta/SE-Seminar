from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password
from app.core.security import verify_password

async def login_user(identifier: str, password: str, db: AsyncSession):
    # Buscar por email o username
    result = await db.execute(
        select(User).where((User.email == identifier) | (User.username == identifier))
    )
    user = result.scalars().first()

    if not user:
        raise ValueError("Usuario no encontrado.")

    if not verify_password(password, user.password):
        raise ValueError("Contraseña incorrecta.")

    return user

async def create_user(user_data: UserCreate, db: AsyncSession):
    # Verificar si ya existe ese correo
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise ValueError("El correo ya está registrado.")

    # Hashear la contraseña
    hashed_password = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
