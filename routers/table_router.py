from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.error import ErrorResponse
from schemas.table import TableDefCreate, TableDefUpdate, TableDefOut
from config.database import get_db
from services.table_service import TableService
from utils.dependencies import get_table_service
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/apis/tabledef", tags=["tabledef"])

@router.post(
    "/",
    response_model=TableDefOut,
    responses={400: {"model": ErrorResponse}},
)
def create_table_def(
    payload: TableDefCreate,
    db: Session = Depends(get_db),
    table_service: TableService = Depends(get_table_service),
):
    logger.info(f"POST /apis/tabledef - Creating table definition: {payload.table_name}")
    result = table_service.create_table(db, payload)
    logger.info(f"POST /apis/tabledef - Table definition created successfully: {result.table_name}")
    return result

@router.put(
    "/{td_id}",
    response_model=TableDefOut,
    responses={404: {"model": ErrorResponse}},
)
def update_table_def(
    td_id: str,
    payload: TableDefUpdate,
    db: Session = Depends(get_db),
    table_service: TableService = Depends(get_table_service),
):
    logger.info(f"PUT /apis/tabledef/{td_id} - Updating table definition")
    result = table_service.update_table(db, td_id, payload)
    logger.info(f"PUT /apis/tabledef/{td_id} - Table definition updated successfully")
    return result

@router.delete(
    "/{td_id}",
    responses={404: {"model": ErrorResponse}},
)
def delete_table_def(
    td_id: str,
    db: Session = Depends(get_db),
    table_service: TableService = Depends(get_table_service)
):
    logger.info(f"DELETE /apis/tabledef/{td_id} - Deleting table definition")
    table_name: str = table_service.delete(db, td_id)
    logger.info(f"DELETE /apis/tabledef/{td_id} - Table definition deleted successfully: {table_name}")
    return {"message": "TableDef deleted successfully", "table_name": table_name}

@router.get("/", response_model=List[TableDefOut])
def list_table_defs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    table_service: TableService = Depends(get_table_service)
):
    logger.debug(f"GET /apis/tabledef - Listing table definitions (skip={skip}, limit={limit})")
    result = table_service.list(db, skip, limit)
    logger.debug(f"GET /apis/tabledef - Returned {len(result)} table definitions")
    return result

@router.get(
    "/{td_id}",
    response_model=TableDefOut,
    responses={404: {"model": ErrorResponse}},
)
def get_table_def(
    td_id: str,
    db: Session = Depends(get_db),
    table_service: TableService = Depends(get_table_service)
):
    logger.debug(f"GET /apis/tabledef/{td_id} - Retrieving table definition")
    result = table_service.get_by_id(db, td_id)
    logger.debug(f"GET /apis/tabledef/{td_id} - Table definition retrieved: {result.table_name}")
    return result
