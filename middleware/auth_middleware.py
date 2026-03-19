from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List, Dict, Any
from utils.security import decode_access_token
from config.database import SessionLocal
from repositories.user_repository import UserRepository


class JWTAuthMiddleware(BaseHTTPMiddleware):

    # List of paths that don't require authentication
    EXEMPT_PATHS: List[tuple[str, str]] = [
        ("POST", "/apis/auth/login"),
        ("POST", "/apis/users"),
        ("GET", "/docs"),
        ("GET", "/openapi.json"),
        ("GET", "/redoc"),
        ("*", "/docs/"),  # allow subpaths
        ("*", "/redoc/"),  # allow subpaths
    ]

    def __init__(self, app):
        super().__init__(app)
        self.user_repository = UserRepository()

    def _create_cors_json_response(
        self, status_code: int, content: Dict[str, Any]
    ) -> JSONResponse:
        response = JSONResponse(status_code=status_code, content=content)
        # Add CORS headers to error responses
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

    async def dispatch(self, request: Request, call_next):
        # Check if the path is exempt from authentication
        if self._is_exempt_path(request.method, request.url.path):
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return self._create_cors_json_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "Authentication required",
                    "message": "Authorization header is missing",
                },
            )

        # Validate Bearer token format
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return self._create_cors_json_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "Invalid authentication",
                    "message": "Authorization header must be in format: Bearer <token>",
                },
            )

        token = parts[1]

        try:
            # Decode and validate the JWT token
            payload = decode_access_token(token)

            # Extract user information from token payload
            user_id = payload.get("sub")
            if not user_id:
                return self._create_cors_json_response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "error": "Invalid token",
                        "message": "Token payload is missing user identifier",
                    },
                )

            # Verify user exists in database
            db = SessionLocal()
            try:
                user = self.user_repository.get_by_id(db, user_id)
                if not user:
                    return self._create_cors_json_response(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "error": "User not found",
                            "message": "The user associated with this token no longer exists",
                        },
                    )

                if not user.is_active:
                    return self._create_cors_json_response(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={
                            "error": "Account inactive",
                            "message": "This user account has been deactivated",
                        },
                    )

                # Attach user info to request state for use in endpoints
                request.state.user_id = user_id
                request.state.user_email = payload.get("email")
                request.state.user_role = user.role
                request.state.user = user

            finally:
                db.close()

        except ValueError as e:
            # Handle token validation errors from decode_access_token
            return self._create_cors_json_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Token validation failed", "message": str(e)},
            )
        except Exception as e:
            # Handle unexpected errors
            return self._create_cors_json_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Authentication error",
                    "message": "An error occurred while processing authentication",
                },
            )

        # Proceed to the endpoint
        response = await call_next(request)
        return response

    def _is_exempt_path(self, method: str, path: str) -> bool:
        method = method.upper()
        
        if method.upper() == "OPTIONS":
            return True
        
        for exempt_method, exempt_path in self.EXEMPT_PATHS:

            # method match (supports "*")
            if exempt_method != "*" and exempt_method.upper() != method:
                continue

            # exact path match
            if path == exempt_path:
                return True

            # prefix match only for paths ending with "/"
            if exempt_path.endswith("/") and path.startswith(exempt_path):
                return True

        return False
