"""
Entrypoint for FastAPI application
https://fastapi.tiangolo.com/tutorial/bigger-applications/
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from resslab_tools import __name__ as title
from resslab_tools import __version__
from resslab_tools.config import settings
from resslab_tools.routers import connections, root
from resslab_tools.services.database import upgrade_database
from resslab_tools.utils.fastapi import use_route_names_as_operation_ids

app = FastAPI(
    title=title,
    version=__version__,
    root_path=settings.root_path,  # type: ignore
)

if settings.cors_enabled:  # type: ignore
    print('cors enabled')
else:
    print('cors disabled')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

app.include_router(root.router)
app.include_router(connections.router)
add_pagination(app)
use_route_names_as_operation_ids(app)

upgrade_database()
