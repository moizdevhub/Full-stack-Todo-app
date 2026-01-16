from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from pydantic import BaseModel, EmailStr

from ..models.user import User, UserCreate, UserRead, UserLogin
from ..services.auth import auth_service
from ..database.session import get_session

router = APIRouter(prefix="/auth", tags=["Authentication"])


class AuthResponse(BaseModel):
    """Response schema for authentication endpoints."""
    access_token: str
    token_type: str = "bearer"
    user: UserRead


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """Register a new user account.

    Args:
        user_data: User registration data (email and password)
        session: Database session

    Returns:
        Authentication response with JWT token and user data

    Raises:
        HTTPException: If email already exists or password is weak
    """
    # Validate password strength
    is_valid, error_message = auth_service.validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )

    # Check if email already exists
    result = await session.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password and create user
    hashed_password = auth_service.hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Generate JWT token
    access_token = auth_service.create_access_token(
        user_id=new_user.id,
        email=new_user.email
    )

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserRead(
            id=new_user.id,
            email=new_user.email,
            created_at=new_user.created_at
        )
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session)
):
    """Authenticate user and return JWT token.

    Args:
        credentials: User login credentials (email and password)
        session: Database session

    Returns:
        Authentication response with JWT token and user data

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    result = await session.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not user or not auth_service.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    access_token = auth_service.create_access_token(
        user_id=user.id,
        email=user.email
    )

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserRead(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )
    )
