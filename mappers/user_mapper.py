from typing import List
from models.user import UserMaster
from schemas.user import UserCreate, UserOut, UserUpdate
from utils.security import hash_password


class UserMapper:

    @staticmethod
    def to_user_out(user: UserMaster) -> UserOut:
        return UserOut(
            id=user.id,
            name=user.name,
            email=user.email,
            provider=user.provider,
            is_active=user.is_active,
            role=user.role,
            created_by=user.created_by,
            created_date=user.created_date,
            updated_by=user.updated_by,
            updated_date=user.updated_date,
        )

    @staticmethod
    def to_user_out_list(users: List[UserMaster]) -> List[UserOut]:
        return [UserMapper.to_user_out(user) for user in users]

    @staticmethod
    def to_user_master_for_create(user: UserCreate) -> UserMaster:
        return UserMaster(
            name=user.name,
            email=user.email,
            password=hash_password(user.password),
            provider=user.provider,
            is_active=user.is_active,
            role=user.role,
            created_by=user.created_by,
        )

    @staticmethod
    def apply_update(db_user: UserMaster, user_in: UserUpdate) -> UserMaster:
        db_user.name = user_in.name or db_user.name
        db_user.email = user_in.email or db_user.email
        db_user.is_active = (
            user_in.is_active if user_in.is_active is not None else db_user.is_active
        )
        db_user.role = user_in.role or db_user.role
        db_user.provider = user_in.provider or db_user.provider
        db_user.updated_by = user_in.updated_by
        db_user.password = (
            hash_password(user_in.password) if user_in.password else db_user.password
        )
        return db_user
