from fastapi import Cookie, Depends, HTTPException
from sqlmodel import Session, select

from app.core.security import verify_token
from app.db.models.user_model import User
from app.db.session import get_session


def get_current_user(access_token: str = Cookie(), db: Session = Depends(get_session)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        print(f"access_token: {access_token}")
        payload = verify_token(access_token)
        print(f"payload: {payload}")
        user = db.exec(select(User).where(User.id == payload.get("id"))).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found or not active")

        return user
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid token")
