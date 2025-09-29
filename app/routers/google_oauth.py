from authlib.integrations.starlette_client import OAuth  # type: ignore[import]
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session, select

from app.core.config import settings
from app.core.security import create_token
from app.db.models.user_model import User
from app.db.session import get_session
from app.schemas.envelope import Envelope

router = APIRouter(prefix="/auth/google", tags=["google"])

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def login(request: Request) -> Response:
    redirect_url = settings.google_redirect_url
    return await oauth.google.authorize_redirect(request, redirect_url)


@router.get("/callback")
async def callback(
    request: Request, response: Response, db: Session = Depends(get_session)
) -> Envelope:
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo")
    print(f"userinfo: {userinfo}")
    if not userinfo or not userinfo.get("sub"):
        raise HTTPException(status_code=400, detail="Google authentication failed")

    # First, try to find user by oauth_sub (most reliable)
    user = db.exec(select(User).where(User.oauth_sub == userinfo["sub"])).first()
    print(f"user: {user}")
    if not user:
        # Fallback: find by email if verified
        if userinfo.get("email_verified") and userinfo.get("email"):
            user = db.exec(select(User).where(User.email == userinfo["email"])).first()

        if not user:
            # Create new user
            user = User(
                full_name=userinfo.get("name", userinfo["sub"]),
                email=userinfo.get("email", ""),
                password_hash="",  # OAuth users don't need password
                oauth_provider="google",
                oauth_sub=userinfo["sub"],
                is_verified=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Link existing user to Google
            user.oauth_provider = "google"
            user.oauth_sub = userinfo["sub"]
            db.commit()

    # Create session token and set cookie (like your existing login)

    token_data = {
        "id": str(user.id),
        "full_name": str(user.full_name),
        "email": str(user.email),
        "role": str(user.role) if user.role else None,
        "is_active": bool(user.is_active),
        "is_verified": bool(user.is_verified),
        "provider": "google",
    }

    access_token = create_token(token_data)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )

    return Envelope(
        detail="Google login successful",
        message="Google login successful",
        status_code=200,
    )
