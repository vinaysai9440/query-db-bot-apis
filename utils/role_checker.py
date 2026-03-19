from fastapi import Request, HTTPException, status
from functools import wraps
from typing import List

class RoleChecker:
    """
    Dependency class for role-based access control.
    
    Usage:
        @router.get("/admin/users")
        def get_all_users(
            request: Request,
            role_checker: None = Depends(RoleChecker(["admin"]))
        ):
            ...
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, request: Request):
        if not hasattr(request.state, 'user_role'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        user_role = request.state.user_role
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(self.allowed_roles)}"
            )
