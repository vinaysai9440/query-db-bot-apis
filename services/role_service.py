from sqlalchemy.orm import Session
from typing import List
from models.role import RoleMaster
from schemas.role import RoleCreate, RoleUpdate, RoleOut
from repositories.role_repository import RoleRepository
from mappers.role_mapper import RoleMapper
from exceptions.exceptions import AppException
from decorators.transaction import transactional
from utils.logger import get_logger

logger = get_logger(__name__)


class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    @transactional
    def create_role(self, db: Session, role_in: RoleCreate) -> RoleOut:
        logger.info(f"Creating new role: {role_in.role_name}")
        existing: RoleMaster = self.role_repository.get_by_name(db, role_in.role_name)
        if existing:
            logger.warning(
                f"Role creation failed: Role already exists - {role_in.role_name}"
            )
            raise AppException(
                http_status=400,
                code="ROLE_ALREADY_EXISTS",
                message_key="role.already.exists",
                params={"role_name": role_in.role_name},
                details={"role_name": role_in.role_name},
            )
        db_role: RoleMaster = self.role_repository.create(
            db, RoleMapper.to_role_master_for_create(role_in)
        )
        logger.info(
            f"Role created successfully: {db_role.role_name}, ID: {db_role.role_id}"
        )
        return RoleMapper.to_role_out(db_role)

    @transactional
    def update_role(self, db: Session, role_id: str, payload: RoleUpdate) -> RoleOut:
        logger.info(f"Updating role: {role_id}")
        existing_role: RoleMaster = self.role_repository.get_by_id(db, role_id)
        if not existing_role:
            logger.warning(f"Role update failed: Role not found - {role_id}")
            raise AppException(
                http_status=404,
                code="ROLE_NOT_FOUND",
                message_key="role.not.found",
                params={"role_id": role_id},
                details={"role_id": role_id},
            )

        if payload.role_name and payload.role_name != existing_role.role_name:
            existing_name = self.role_repository.get_by_name(db, payload.role_name)
            if existing_name:
                logger.warning(
                    f"Role update failed: Role name already exists - {payload.role_name}"
                )
                raise AppException(
                    http_status=400,
                    code="ROLE_ALREADY_EXISTS",
                    message_key="role.already.exists",
                    params={"role_name": payload.role_name},
                    details={"role_name": payload.role_name},
                )

        RoleMapper.apply_update(existing_role, payload)
        db_role = self.role_repository.update(db, existing_role)
        logger.info(f"Role updated successfully: {db_role.role_name}, ID: {role_id}")
        return RoleMapper.to_role_out(db_role)

    @transactional
    def delete_role(self, db: Session, role_id: str) -> str:
        logger.info(f"Deleting role: {role_id}")
        db_role: RoleMaster = self.role_repository.get_by_id(db, role_id)
        if not db_role:
            logger.warning(f"Role deletion failed: Role not found - {role_id}")
            raise AppException(
                http_status=404,
                code="ROLE_NOT_FOUND",
                message_key="role.delete.not.found",
                params={"role_id": role_id},
                details={"role_id": role_id},
            )
        self.role_repository.delete(db, db_role)
        logger.info(f"Role deleted successfully: {db_role.role_name}, ID: {role_id}")
        return db_role.role_name

    def get_role_by_id(self, db: Session, role_id: str) -> RoleOut:
        logger.debug(f"Retrieving role by ID: {role_id}")
        role: RoleMaster = self.role_repository.get_by_id(db, role_id)
        if not role:
            logger.warning(f"Role not found: {role_id}")
            raise AppException(
                http_status=404,
                code="ROLE_NOT_FOUND",
                message_key="role.not.found",
                params={"role_id": role_id},
                details={"role_id": role_id},
            )
        logger.debug(f"Role retrieved: {role.role_name}")
        return RoleMapper.to_role_out(role)

    def list_roles(self, db: Session, skip: int = 0, limit: int = 100) -> List[RoleOut]:
        logger.debug(f"Listing roles with skip={skip}, limit={limit}")
        roles: List[RoleMaster] = self.role_repository.list(db, skip, limit)
        logger.info(f"Retrieved {len(roles)} roles")
        return RoleMapper.to_role_out_list(roles)

    def get_role_names(self, db: Session) -> List[str]:
        logger.debug("Retrieving all active role names")
        roles: List[RoleMaster] = self.role_repository.list_active(db)
        role_names: List[str] = [role.role_name for role in roles]
        logger.info(f"Retrieved {len(role_names)} active role names")
        return role_names
