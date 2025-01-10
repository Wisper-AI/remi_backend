from fastapi import FastAPI


def import_routes(app: FastAPI) -> None:
    """
    Import routes from different modules and add them to the main application
    """
    del app
