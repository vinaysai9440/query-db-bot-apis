from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.auth_service import AuthService
from schemas.auth import AuthRequest, AuthResponse
from schemas.error import ErrorResponse
from config.database import get_db
from utils.dependencies import get_auth_service
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/apis/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=AuthResponse,
    responses={401: {"model": ErrorResponse}},
)
def authenticate_user(
    login_data: AuthRequest,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
):
    logger.info(f"Login request received for email: {login_data.email}")
    response = auth_service.authenticate_user(db, login_data)
    logger.info(f"Login successful for email: {login_data.email}")
    return response
