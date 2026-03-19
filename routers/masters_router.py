from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from services.masters_service import MastersService
from typing import List

from utils.dependencies import get_masters_service
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/apis/masters", tags=["masters"])

@router.get("/permissions", response_model=List[str])
def get_master_permissions(
    db: Session = Depends(get_db),
    masters_service: MastersService = Depends(get_masters_service),
):
    logger.debug("GET /apis/masters/permissions - Retrieving permissions")
    result = masters_service.get_permissions(db)
    logger.debug(f"GET /apis/masters/permissions - Returned {len(result)} permissions")
    return result
