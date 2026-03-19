from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate, UserOut
from schemas.error import ErrorResponse
from config.database import get_db
from services.user_service import UserService
from utils.dependencies import get_user_service
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/apis/users", tags=["users"])

@router.post(
    "/",
    response_model=UserOut,
    responses={400: {"model": ErrorResponse}},
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    logger.info(f"POST /apis/users - Creating user: {user_in.email}")
    result = user_service.create_user(db, user_in)
    logger.info(f"POST /apis/users - User created successfully: {result.email}")
    return result


@router.put(
    "/{user_id}",
    response_model=UserOut,
    responses={404: {"model": ErrorResponse}},
)
def update_user(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    logger.info(f"PUT /apis/users/{user_id} - Updating user")
    result = user_service.update_user(db, user_id, payload)
    logger.info(f"PUT /apis/users/{user_id} - User updated successfully")
    return result


@router.delete(
    "/{user_id}",
    responses={404: {"model": ErrorResponse}},
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    logger.info(f"DELETE /apis/users/{user_id} - Deleting user")
    email: str = user_service.delete(db, user_id)
    logger.info(f"DELETE /apis/users/{user_id} - User deleted successfully: {email}")
    return {"message": "User deleted successfully", "user_email": email}


@router.get("/", response_model=List[UserOut])
def list_users(
    skip: int = 0,
    limit: int = 10000,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    logger.debug(f"GET /apis/users - Listing users (skip={skip}, limit={limit})")
    result = user_service.list(db, skip, limit)
    logger.debug(f"GET /apis/users - Returned {len(result)} users")
    return result


@router.get(
    "/{user_id}",
    response_model=UserOut,
    responses={404: {"model": ErrorResponse}},
)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    logger.debug(f"GET /apis/users/{user_id} - Retrieving user")
    result = user_service.get_by_id(db, user_id)
    logger.debug(f"GET /apis/users/{user_id} - User retrieved: {result.email}")
    return result
