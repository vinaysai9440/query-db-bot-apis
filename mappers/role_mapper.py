from typing import List
from datetime import datetime
from models.role import RoleMaster, RolePermission
from schemas.auth import AuthPermission
from schemas.role import (
    RoleOut,
    RoleCreate,
    RoleUpdate,
    RolePermissionInfo,
)


class RoleMapper:

    @staticmethod
    def to_role_out(role: RoleMaster) -> RoleOut:
        role_permissions: List[RolePermissionInfo] = [
            RolePermissionInfo(ref_id=perm.ref_id, granted=perm.granted)
            for perm in (role.role_permissions or [])
        ]
        return RoleOut(
            role_id=role.role_id,
            role_name=role.role_name,
            description=role.description,
            is_active=role.is_active,
            role_permissions=role_permissions,
            created_by=role.created_by,
            created_date=role.created_date,
            updated_by=role.updated_by,
            updated_date=role.updated_date,
        )

    @staticmethod
    def to_role_out_list(roles: List[RoleMaster]) -> List[RoleOut]:
        return [RoleMapper.to_role_out(r) for r in roles]

    @staticmethod
    def to_role_master_for_create(role_in: RoleCreate) -> RoleMaster:
        role = RoleMaster(
            role_name=role_in.role_name,
            description=role_in.description,
            is_active=role_in.is_active if role_in.is_active is not None else True,
            created_by=role_in.created_by,
        )
        # map incoming permissions
        role.role_permissions = [
            RolePermission(
                ref_id=perm.ref_id,
                granted=perm.granted,
                created_date=datetime.utcnow(),
            )
            for perm in (role_in.role_permissions or [])
        ]
        return role

    @staticmethod
    def apply_update(existing: RoleMaster, role_in: RoleUpdate) -> RoleMaster:
        existing.role_name = role_in.role_name or existing.role_name
        existing.description = role_in.description or existing.description
        existing.is_active = (
            role_in.is_active if role_in.is_active is not None else existing.is_active
        )
        existing.updated_by = role_in.updated_by
        existing.role_permissions = [
            RolePermission(
                ref_id=perm.ref_id,
                granted=perm.granted,
                created_date=datetime.utcnow(),
            )
            for perm in (role_in.role_permissions or [])
        ]
        return existing

    @staticmethod
    def to_auth_permissions(role: RoleMaster) -> list[AuthPermission]:
        if not role:
            return []

        return [
            AuthPermission(ref_id=perm.ref_id, granted=perm.granted)
            for perm in (role.role_permissions or [])
            if perm.ref_id is not None
        ]
