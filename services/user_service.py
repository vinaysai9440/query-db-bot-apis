from sqlalchemy.orm import Session
from models.user import UserMaster
from schemas.user import UserCreate, UserUpdate, UserOut
from repositories.user_repository import UserRepository
from mappers.user_mapper import UserMapper
from decorators.transaction import transactional
from typing import List
from exceptions.exceptions import AppException
from utils.logger import get_logger

logger = get_logger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @transactional
    def create_user(self, db: Session, payload: UserCreate) -> UserOut:
        logger.info(f"Creating new user with email: {payload.email}")
        existing = self.user_repository.get_by_email(db, payload.email)
        if existing:
            logger.warning(f"User creation failed: Email already exists - {payload.email}")
            raise AppException(
                http_status=400,
                code="USER_ALREADY_EXISTS",
                message_key="user.already.exists",
                params={"email": payload.email},
                details={"email": payload.email},
            )
        userMaster: UserMaster = UserMapper.to_user_master_for_create(payload)
        user = self.user_repository.create(db, userMaster)
        logger.info(f"User created successfully: {user.email}, ID: {user.id}")
        return UserMapper.to_user_out(user)

    @transactional
    def update_user(self, db: Session, user_id: str, payload: UserUpdate) -> UserOut:
        logger.info(f"Updating user: {user_id}")
        existing = self.user_repository.get_by_id(db, user_id)
        if not existing:
            logger.warning(f"User update failed: User not found - {user_id}")
            raise AppException(
                http_status=400,
                code="USER_NOT_FOUND",
                message_key="user.not.found",
                params={"user_id": user_id},
                details={"user_id": user_id},
            )
        UserMapper.apply_update(existing, payload)
        user = self.user_repository.update(db, existing)
        logger.info(f"User updated successfully: {user.email}, ID: {user.id}")
        return UserMapper.to_user_out(user)

    @transactional
    def delete(self, db: Session, user_id: str) -> str:
        logger.info(f"Deleting user: {user_id}")
        existing: UserMaster = self.user_repository.get_by_id(db, user_id)
        if not existing:
            logger.warning(f"User deletion failed: User not found - {user_id}")
            raise AppException(
                http_status=400,
                code="USER_NOT_FOUND",
                message_key="user.delete.not.found",
                params={"user_id": user_id},
                details={"user_id": user_id},
            )

        self.user_repository.delete(db, existing)
        logger.info(f"User deleted successfully: {existing.email}, ID: {user_id}")
        return existing.email

    def list(self, db: Session, skip: int, limit: int) -> List[UserOut]:
        logger.debug(f"Listing users with skip={skip}, limit={limit}")
        users: List[UserMaster] = self.user_repository.list(db, skip=skip, limit=limit)
        logger.info(f"Retrieved {len(users)} users")
        return UserMapper.to_user_out_list(users)

    def get_by_id(self, db: Session, user_id: str) -> UserOut:
        logger.debug(f"Retrieving user by ID: {user_id}")
        user: UserMaster = self.user_repository.get_by_id(db, user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise AppException(
                http_status=404,
                code="USER_NOT_FOUND",
                message_key="user.not.found",
                params={"user_id": user_id},
                details={"user_id": user_id},
            )
        logger.debug(f"User retrieved: {user.email}")
        return UserMapper.to_user_out(user)
