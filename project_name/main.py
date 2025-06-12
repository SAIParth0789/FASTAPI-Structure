import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.requests import Request

from project_name.database import database
from project_name.logging_conf import configure_logging

# ---------------- Routes Package Import --------------------
from project_name.routers.admin_user import router as admin_user_router


logger = logging.getLogger(__name__)

security = HTTPBasic()

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "admin"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


app = FastAPI(lifespan=lifespan,
              docs_url=None,
              redoc_url=None,
              title="CodeHub",
              description="CodeHub API",
              version="2.0",
              openapi_url="/api/v1/openapi.json",
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your specific allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


app.add_middleware(CorrelationIdMiddleware)


# ------------------ Declare your Routes ------------------------
app.include_router(admin_user_router, prefix="/admin", tags=["Admin"])
# app.include_router(categories_router, prefix="/categories")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)

@app.get("/api/v1/docs", include_in_schema=False)
async def get_swagger_documentation(request: Request, username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="docs")

@app.get("/api/v1/redoc", include_in_schema=False)
async def get_redoc_documentation(request: Request, username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url=app.openapi_url, title="redoc")


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Oops! The page you are looking for was not found."}
    )


# --------

import json

def get_config():
    """
    This function contains different hardcoded credentials that
    should be detected by Amazon CodeGuru.
    """
    # Using different patterns for fake credentials
    config = {
        "api_key": "zaCELgL.0imfnc8mVLWwsAawjYr4Rx-Af50DDqtlx",
        "api_secret": "26422219-4a7b-45b7-a365-802526543210",
        "db_connection_string": "mongodb+srv://user_test:MyTestPassword123@cluster-test.mongodb.net/test?retryWrites=true"
    }

    print("Using hardcoded API key and secret for connection.")
    return json.dumps(config)

if __name__ == "__main__":
    get_config()
