from fastapi import APIRouter

from . import endpoints

router = APIRouter()
router.include_router(endpoints.router, prefix="/fingerprints", tags=["fingerprints"])
