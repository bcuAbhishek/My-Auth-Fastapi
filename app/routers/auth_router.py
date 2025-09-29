from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, or_, select

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.security import create_token, hash_password, verify_password
from app.db.models.user_model import User
from app.db.session import get_session
from app.schemas.envelope import Envelope
from app.schemas.user_schema import (
    ChangePasswordSchema,
    UserLoginSchema,
    UserRegisterSchema,
    UserResponseSchema,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(
    payload: UserRegisterSchema, db: Session = Depends(get_session)
) -> Envelope:
    existing_user = db.exec(select(User).where(User.email == payload.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(payload.password)
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hashed_password,
    )

    user.is_verified = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return Envelope(
        detail="User registered successfully",
        message=f"User {user.full_name} registered successfully",
        status_code=201,
    )


@router.post("/login")
async def login(
    payload: UserLoginSchema, response: Response, db: Session = Depends(get_session)
) -> Envelope:
    print(f"payload: {payload}")
    user = db.exec(select(User).where(User.email == payload.email)).first()
    print(f"user: {user}")
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid password")

    token_data = {
        "id": str(user.id),
        "full_name": str(user.full_name),
        "email": str(user.email),
        "role": str(user.role) if user.role else None,
        "is_active": bool(user.is_active),
        "is_verified": bool(user.is_verified),
    }

    access_token = create_token(token_data)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        max_age=settings.access_token_expire_minutes * 60,
        samesite="lax",
        path="/",
    )
    return Envelope(
        detail="User logged in successfully",
        message="User logged in successfully",
        status_code=200,
    )


@router.get("/profile")
async def profile(user: User = Depends(get_current_user)) -> Envelope:
    return Envelope(
        data=UserResponseSchema(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            role=user.role,
        ),
        detail="User profile",
        message=f"Logged in as {user.full_name}",
        status_code=200,
    )


@router.post("/logout")
async def logout(response: Response) -> Envelope:
    response.delete_cookie(key="access_token")
    return Envelope(
        detail="User logged out successfully",
        message="User logged out successfully",
        status_code=200,
    )


@router.post("/change-password")
async def change_password(
    payload: ChangePasswordSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> Envelope:
    if not verify_password(payload.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid password")
    user.password_hash = hash_password(payload.new_password)
    db.commit()
    db.refresh(user)
    return Envelope(
        detail="Password changed successfully",
        message="Password changed successfully",
        status_code=200,
    )
