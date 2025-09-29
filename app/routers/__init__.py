from .auth_router import router as auth_router
from .google_oauth import router as google_oauth_router

routers = [auth_router, google_oauth_router]

__all__ = ["auth_router", "google_oauth_router", "routers"]
