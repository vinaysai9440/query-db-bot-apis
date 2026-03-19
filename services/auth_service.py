from sqlalchemy.orm import Session
from mappers.auth_mapper import AuthMapper
from mappers.role_mapper import RoleMapper
from models.user import UserMaster
from repositories.role_repository import RoleRepository
from schemas.auth import AuthRequest, AuthResponse
from repositories.user_repository import UserRepository
from utils.security import verify_password, create_access_token
from exceptions.exceptions import AppException
from utils.logger import get_logger

logger = get_logger(__name__)


class AuthService:

    def __init__(
        self, user_repository: UserRepository, role_repository: RoleRepository
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def authenticate_user(self, db: Session, login_data: AuthRequest) -> AuthResponse:
        logger.info(f"Authentication attempt for user: {login_data.email}")
        user: UserMaster = self.user_repository.get_by_email(db, login_data.email)

        flag: bool = True
        if not user:
            logger.warning(f"Authentication failed: User not found - {login_data.email}")
            flag = False
        if not user.is_active:
            logger.warning(f"Authentication failed: User inactive - {login_data.email}")
            flag = False
        if not verify_password(login_data.password, user.password):
            logger.warning(f"Authentication failed: Invalid password - {login_data.email}")
            flag = False

        if flag == False:
            raise AppException(
                http_status=401,
                code="AUTHENTICATION_FAILED",
                message_key="auth.invalid.credentials",
                details={"email": login_data.email},
            )

        role = self.role_repository.get_by_name(db, user.role)
        if not role:
            logger.warning(f"Role '{user.role}' not found for user {login_data.email}, using default 'user' role")
            role = self.role_repository.get_by_name(db, "user")
        permissions = RoleMapper.to_auth_permissions(role)

        token_data = {
            "id": user.id,
            "sub": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "permissions": [
                {"ref_id": perm.ref_id, "granted": perm.granted} for perm in permissions
            ],
        }
        token = create_access_token(token_data)

        logger.info(f"Authentication successful for user: {login_data.email}, role: {user.role}")
        return AuthMapper.to_auth_response(user, permissions, token)
