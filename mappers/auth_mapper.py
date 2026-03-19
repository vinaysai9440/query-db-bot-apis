from models.user import UserMaster
from schemas.auth import AuthPermission, AuthResponse


class AuthMapper:

    @staticmethod
    def to_auth_response(
        user: UserMaster, permissions: list[AuthPermission], token: str
    ) -> AuthResponse:
        return AuthResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            provider=user.provider,
            role=user.role,
            permissions=permissions,
            token=token,
        )
