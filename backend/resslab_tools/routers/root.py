"""
Handle / requests
"""
from fastapi import APIRouter
from resslab_tools import __name__ as name
from resslab_tools import __version__
from resslab_tools.models import Info

router = APIRouter()


@router.get('/', response_model=Info)
async def root() -> Info:
    """
    Get Info
    """
    return Info(
        name=name,
        version=__version__
    )
