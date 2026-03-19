from functools import lru_cache
from fastapi import Request, HTTPException, status
from repositories.query_repository import QueryRepository
from repositories.user_repository import UserRepository
from repositories.table_repository import TableRepository
from repositories.chat_repository import ChatRepository
from repositories.role_repository import RoleRepository
from services.auth_service import AuthService
from services.masters_service import MastersService
from services.user_service import UserService
from services.table_service import TableService
from services.chat_service import ChatService
from services.llm_service import LLMService
from services.role_service import RoleService
from models.user import UserMaster

# Repository dependencies
@lru_cache()
def get_user_repository() -> UserRepository:
    return UserRepository()

@lru_cache()
def get_table_repository() -> TableRepository:
    return TableRepository()

@lru_cache()
def get_role_repository() -> RoleRepository:
    return RoleRepository()

@lru_cache()
def get_query_repository() -> QueryRepository:
    return QueryRepository()

@lru_cache()
def get_chat_repository() -> ChatRepository:
    return ChatRepository()

# Service dependencies
@lru_cache()
def get_user_service() -> UserService:
    return UserService(user_repository=get_user_repository())

@lru_cache()
def get_auth_service() -> AuthService:
    return AuthService(user_repository=get_user_repository(), role_repository=get_role_repository())

@lru_cache()
def get_table_service() -> TableService:
    return TableService(table_repository=get_table_repository())

@lru_cache()
def get_llm_service() -> LLMService:
    return LLMService()

@lru_cache()
def get_chat_service() -> ChatService:
    return ChatService(
        table_repository=get_table_repository(),
        chat_repository=get_chat_repository(),
        query_repository=get_query_repository(),
        llm_service=get_llm_service()
    )

@lru_cache()
def get_role_service() -> RoleService:
    return RoleService(role_repository=get_role_repository())

@lru_cache()
def get_masters_service() -> MastersService:
    return MastersService(table_service=get_table_service())

def get_current_user(request: Request) -> UserMaster:
    if not hasattr(request.state, 'user'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return request.state.user

def get_current_user_id(request: Request) -> str:
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return request.state.user_id