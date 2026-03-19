from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.error import ErrorResponse
from schemas.role import RoleCreate, RoleUpdate, RoleOut
from config.database import get_db
from services.role_service import RoleService
from utils.dependencies import get_role_service
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/apis/roles", tags=["roles"])


@router.post("/", response_model=RoleOut, responses={400: {"model": ErrorResponse}})
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db),
    role_service: RoleService = Depends(get_role_service),
):
    logger.info(f"POST /apis/roles - Creating role: {role_in.role_name}")
    result = role_service.create_role(db, role_in)
    logger.info(f"POST /apis/roles - Role created successfully: {result.role_name}")
    return result


@router.put(
    "/{role_id}", response_model=RoleOut, responses={400: {"model": ErrorResponse}}
)
def update_role(
    role_id: str,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    role_service: RoleService = Depends(get_role_service),
):
    logger.info(f"PUT /apis/roles/{role_id} - Updating role")
    result = role_service.update_role(db, role_id, payload)
    logger.info(f"PUT /apis/roles/{role_id} - Role updated successfully")
    return result


@router.delete(
    "/{role_id}",
    responses={404: {"model": ErrorResponse}},
)
def delete_role(
    role_id: str,
    db: Session = Depends(get_db),
    role_service: RoleService = Depends(get_role_service),
):
    logger.info(f"DELETE /apis/roles/{role_id} - Deleting role")
    role_name: str = role_service.delete_role(db, role_id)
    logger.info(f"DELETE /apis/roles/{role_id} - Role deleted successfully: {role_name}")
    return {"message": "Role deleted successfully", "role_name": role_name}


@router.get("/", response_model=List[RoleOut])
def list_roles(
    skip: int = 0,
    limit: int = 10000,
    db: Session = Depends(get_db),
    role_service: RoleService = Depends(get_role_service),
):
    logger.debug(f"GET /apis/roles - Listing roles (skip={skip}, limit={limit})")
    result = role_service.list_roles(db, skip, limit)
    logger.debug(f"GET /apis/roles - Returned {len(result)} roles")
    return result


@router.get("/names", response_model=List[str])
def get_role_names(
    db: Session = Depends(get_db),
    role_service: RoleService = Depends(get_role_service),
):
    logger.debug("GET /apis/roles/names - Retrieving role names")
    result = role_service.get_role_names(db)
    logger.debug(f"GET /apis/roles/names - Returned {len(result)} role names")
    return result


@router.get("/{role_id}", response_model=RoleOut)
def get_role(
    role_id: str,
    db: Session = Depends(get_db),
    role_service: RoleService = Depends(get_role_service),
):
    logger.debug(f"GET /apis/roles/{role_id} - Retrieving role")
    result = role_service.get_role_by_id(db, role_id)
    logger.debug(f"GET /apis/roles/{role_id} - Role retrieved: {result.role_name}")
    return result
