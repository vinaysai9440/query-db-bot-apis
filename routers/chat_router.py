from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.error import ErrorResponse
from config.database import get_db, get_trans_db
from services.chat_service import ChatService
from schemas.chat import (
    ChatQueryRequest,
    ChatQueryResponse,
    ChatSessionInfo,
    ChatSessionRequest,
)
from utils.dependencies import get_chat_service
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/apis/chat", tags=["chat"])


@router.post(
    "/session",
    response_model=ChatSessionInfo,
    responses={400: {"model": ErrorResponse}},
)
def create_chat_session(
    request: ChatSessionRequest,
    db: Session = Depends(get_db),
    trans_db: Session = Depends(get_trans_db),
    chat_service: ChatService = Depends(get_chat_service),
):
    logger.info(f"POST /apis/chat/session - Creating chat session for user: {request.user_id}")
    result = chat_service.create_chat_session(db, trans_db, request)
    logger.info(f"POST /apis/chat/session - Chat session created: {result.session_id}")
    return result


@router.post(
    "/session/{session_id}/query",
    response_model=ChatQueryResponse,
    responses={400: {"model": ErrorResponse}},
)
def process_chat_session_query(
    session_id: str,
    request: ChatQueryRequest,
    db: Session = Depends(get_db),
    trans_db: Session = Depends(get_trans_db),
    chat_service: ChatService = Depends(get_chat_service),
):
    logger.info(f"POST /apis/chat/session/{session_id}/query - Processing query")
    result = chat_service.process_chat_query(db, trans_db, session_id, request)
    logger.info(f"POST /apis/chat/session/{session_id}/query - Query processed successfully")
    return result


@router.delete(
    "/session/{session_id}",
    responses={404: {"model": ErrorResponse}},
)
def delete_chat_session(
    session_id: str,
    db: Session = Depends(get_db),
    chat_service: ChatService = Depends(get_chat_service),
):
    logger.info(f"DELETE /apis/chat/session/{session_id} - Deleting chat session")
    session_title: str = chat_service.delete_chat_session(db, session_id)
    logger.info(f"DELETE /apis/chat/session/{session_id} - Chat session deleted: {session_title}")
    return {"message": "Session deleted successfully", "session_title": session_title}


@router.get(
    "/session/{session_id}",
    response_model=ChatSessionInfo,
    responses={400: {"model": ErrorResponse}},
)
def get_chat_session(
    session_id: str,
    db: Session = Depends(get_db),
    chat_service: ChatService = Depends(get_chat_service),
):
    logger.debug(f"GET /apis/chat/session/{session_id} - Retrieving chat session")
    result = chat_service.get_chat_session(db, session_id)
    logger.debug(f"GET /apis/chat/session/{session_id} - Chat session retrieved")
    return result


@router.get(
    "/sessions/{user_id}",
    response_model=List[ChatSessionInfo],
    responses={400: {"model": ErrorResponse}},
)
def get_user_chat_sessions(
    user_id: str,
    db: Session = Depends(get_db),
    chat_service: ChatService = Depends(get_chat_service),
):
    logger.debug(f"GET /apis/chat/sessions/{user_id} - Retrieving user chat sessions")
    result = chat_service.get_user_chat_sessions(db, user_id)
    logger.debug(f"GET /apis/chat/sessions/{user_id} - Retrieved {len(result)} chat sessions")
    return result
