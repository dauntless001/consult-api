from router import api_router
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from database import init_db


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="Consult Service API",
        description="A consultation platform where patient can get solutions from doctors",
        version="1.0",
        docs_url="/api/docs/",
        redoc_url="/api/redoc/",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    app.include_router(router=api_router, prefix="/api")
    @app.on_event("startup")
    def on_startup():
        init_db()
    return app
