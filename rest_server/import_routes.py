from fastapi import FastAPI

from rest_server.api.email import router as email_router


def import_routes(app: FastAPI) -> None:
    """
    Import routes from different modules and add them to the main application

    Args:
        app: FastAPI application
    """
    app.include_router(email_router)
    # Add other routers here as needed
