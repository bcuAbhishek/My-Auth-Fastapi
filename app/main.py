import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.core.exceptions import http_exception_handler, validation_exception_handler
from app.routers import routers

app = FastAPI(title=settings.app_name)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_middleware(SessionMiddleware, secret_key=settings.jwt_secret)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


for r in routers:
    app.include_router(r)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
