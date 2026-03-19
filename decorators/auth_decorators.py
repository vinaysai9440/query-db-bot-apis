from fastapi import Request, HTTPException, status
from functools import wraps
from typing import List


def require_roles(allowed_roles: List[str]):
    """
    Decorator to enforce role-based access control on endpoints.
    
    Usage:
        @router.get("/admin/users")
        @require_roles(["admin"])
        def get_all_users(request: Request):
            ...
    
    Args:
        allowed_roles: List of role names that are allowed to access the endpoint
    
    Raises:
        HTTPException: 403 if user's role is not in allowed_roles
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            request = kwargs.get('request')
            if not request:
                # Try to find request in args
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request or not hasattr(request.state, 'user_role'):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_role = request.state.user_role
            if user_role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
                )
            
            return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            request = kwargs.get('request')
            if not request:
                # Try to find request in args
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request or not hasattr(request.state, 'user_role'):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_role = request.state.user_role
            if user_role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
                )
            
            return func(*args, **kwargs)
        
        # Return appropriate wrapper based on whether function is async
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator
