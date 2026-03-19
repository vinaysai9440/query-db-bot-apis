from sqlalchemy.orm import Session
from models.chat import ChatSession, ChatConversation
from repositories.chat_repository import ChatRepository
from repositories.table_repository import TableRepository
from repositories.query_repository import QueryRepository
from services.llm_service import LLMService
from schemas.chat import (
    ChatQueryRequest,
    ChatQueryResponse,
    ChatSessionInfo,
    ChatConversationInfo,
    ChatSessionRequest,
)
from decorators.transaction import transactional
from exceptions.exceptions import AppException
from typing import List
import time
import json
from utils.logger import get_logger

logger = get_logger(__name__)


class ChatService:

    def __init__(
        self,
        table_repository: TableRepository,
        chat_repository: ChatRepository,
        query_repository: QueryRepository,
        llm_service: LLMService,
    ):
        self.table_repository = table_repository
        self.chat_repository = chat_repository
        self.query_repository = query_repository
        self.llm_service = llm_service
        self.max_conversations = 10

    @transactional
    def create_chat_session(
        self, db: Session, trans_db: Session, request: ChatSessionRequest
    ) -> ChatSessionInfo:
        logger.info(f"Creating new chat session for user: {request.user_id}")
        session_title = self.llm_service.generate_session_title(request.query_text)
        logger.debug(f"Generated session title: {session_title}")
        db_session: ChatSession = self.chat_repository.create_chat_session(
            db, request.user_id, session_title
        )

        conversation = self.process_chat_query(db, trans_db, db_session.session_id, request)
    
        logger.info(f"Chat session created successfully: {db_session.session_id}")
        return ChatSessionInfo(
            session_id=db_session.session_id,
            user_id=db_session.user_id,
            title=db_session.title,
            is_active=db_session.is_active,
            created_date=db_session.created_date,
            conversations=[conversation],
        )

    def get_chat_session(self, db: Session, session_id: str) -> ChatSessionInfo:
        logger.debug(f"Retrieving chat session: {session_id}")
        db_session = self.chat_repository.get_chat_session(db, session_id)

        if not db_session:
            logger.warning(f"Chat session not found: {session_id}")
            raise AppException(
                http_status=404,
                code="SESSION_NOT_FOUND",
                message_key="session.not.found",
                params={"session_id": session_id},
                details={"session_id": session_id},
            )

        # Load conversations for the session
        conversations = self.chat_repository.get_chat_conversations(db, session_id)
        logger.debug(f"Retrieved {len(conversations)} conversations for session: {session_id}")

        # Convert conversations to ChatConversationInfo
        # Only include suggestions in the last conversation
        conversation_infos = []
        for i, conv in enumerate(conversations):
            conv_info = ChatConversationInfo.model_validate(conv)
            # Clear suggestions for all except the last conversation
            if i < len(conversations) - 1:
                conv_info.suggestions = None
            conversation_infos.append(conv_info)

        return ChatSessionInfo(
            session_id=db_session.session_id,
            user_id=db_session.user_id,
            title=db_session.title,
            is_active=db_session.is_active,
            created_date=db_session.created_date,
            conversations=conversation_infos,
        )

    def get_user_chat_sessions(
        self, db: Session, user_id: str
    ) -> List[ChatSessionInfo]:
        logger.debug(f"Retrieving chat sessions for user: {user_id}")
        db_sessions: List[ChatSession] = self.chat_repository.get_user_chat_sessions(
            db, user_id
        )

        session_infos: List[ChatSessionInfo] = []
        for session in db_sessions:
            session_info = ChatSessionInfo(
                session_id=session.session_id,
                user_id=session.user_id,
                title=session.title,
                is_active=session.is_active,
                created_date=session.created_date,
                conversations=[],
            )
            session_infos.append(session_info)

        logger.info(f"Retrieved {len(session_infos)} chat sessions for user: {user_id}")
        return session_infos

    @transactional
    def process_chat_query(
        self, db: Session, trans_db: Session, session_id: str, request: ChatQueryRequest
    ) -> ChatQueryResponse:
        start_time = time.time()
        sql_query = None
        logger.info(f"Processing chat query for session: {session_id}, query: {request.query_text[:100]}")
        try:
            # Step 1: Check for existing session or create new one
            session = self.chat_repository.get_chat_session(db, session_id)
            if not session:
                logger.warning(f"Chat session not found: {session_id}")
                raise AppException(
                    http_status=404,
                    code="SESSION_NOT_FOUND",
                    message_key="session.not.found",
                    params={"session_id": session_id},
                    details={"session_id": session_id},
                )

            # Step 2: Fetch context for LLM
            conversations = self.chat_repository.get_chat_conversations(
                db, session_id, self.max_conversations
            )
            logger.info(f"Loaded {len(conversations)} previous conversations for context")

            # Step 3a: Get table definitions
            available_tables = self.table_repository.list_active(db, skip=0, limit=1000)
            logger.info(f"Retrieved {len(available_tables)} available tables")

            # Step 3b: First pass - Identify relevant tables using LLM service
            relevant_tables = self.llm_service.identify_relevant_tables(
                request.query_text, conversations, available_tables
            )
            logger.info(f"LLM identified {len(relevant_tables)} relevant tables")

            # Step 3c: If LLM couldn't identify tables, provide intelligent guidance
            if not relevant_tables:
                logger.warning("No relevant tables identified, providing context help")
                suggestion_message = self.llm_service.create_context_help_message(
                    request.query_text, available_tables
                )
                execution_time_ms = (time.time() - start_time) * 1000
                error_conversation = ChatConversation(
                    session_id=session.session_id,
                    query_text=request.query_text,
                    content=suggestion_message,
                    content_type="text/plain",
                    sql_generated=None,
                    execution_time_ms=str(execution_time_ms),
                    error_message="LLM couldn't identify tables",
                )
                db_error_conversation = self.chat_repository.save_conversation(
                    db, error_conversation
                )
                return ChatQueryResponse.model_validate(db_error_conversation)

            # Step 3d: Generate SQL using LLM service with filtered tables metadata
            sql_query = self.llm_service.generate_sql_query(
                request.query_text, conversations, relevant_tables
            )
            logger.info(f"Generated SQL query: {sql_query}")

            # Step 4: Validate and execute SQL
            if not self.query_repository.validate_sql_query(sql_query):
                logger.warning(f"Generated SQL query is not allowed: {sql_query}")
                execution_time_ms = (time.time() - start_time) * 1000
                error_message = f"The generated SQL query is not allowed: {sql_query}"
                db_error_conversation = ChatConversation(
                    session_id=session.session_id,
                    query_text=request.query_text,
                    content=error_message,
                    content_type="text/plain",
                    sql_generated=sql_query,
                    execution_time_ms=str(execution_time_ms),
                    error_message=None,
                )
                db_error_conversation = self.chat_repository.save_conversation(
                    db, db_error_conversation
                )
                return ChatQueryResponse.model_validate(db_error_conversation)

            query_results = self.query_repository.execute_sql_query(trans_db, sql_query, 50)
            logger.info(f"Query executed successfully, returned {len(query_results) if query_results else 0} rows")

            # Generate intelligent suggestions for next questions (only metadata, no actual data)
            suggestions = []
            if query_results:
                try:
                    result_count = len(query_results)
                    result_columns = list(query_results[0].keys()) if query_results else []
                    suggestions = self.llm_service.generate_query_suggestions(
                        request.query_text,
                        sql_query,
                        result_count,
                        result_columns,
                        conversations,
                        relevant_tables
                    )
                    logger.info(f"Generated {len(suggestions)} suggestions for next queries")
                except Exception as e:
                    logger.warning(f"Failed to generate suggestions: {str(e)}")
                    suggestions = []

            # Serialize query results to JSON
            content = json.dumps(query_results) if query_results else None
            content_type = "application/json" if query_results else None
            
            # Serialize suggestions to JSON (only for current/last conversation)
            suggestions_json = json.dumps(suggestions) if suggestions else None
            
            # Calculate execution time
            execution_time_ms = (time.time() - start_time) * 1000
            
            conversation = ChatConversation(
                session_id=session.session_id,
                query_text=request.query_text,
                content=content,
                content_type=content_type,
                sql_generated=sql_query,
                execution_time_ms=str(execution_time_ms),
                suggestions=suggestions_json,
                error_message=None,
            )

            # Step 6: Save conversation record
            db_conversation = self.chat_repository.save_conversation(db, conversation)
            logger.info(f"Conversation saved successfully, execution time: {execution_time_ms:.2f}ms")

            # Step 7: Build response
            return ChatQueryResponse.model_validate(db_conversation)

        except Exception as e:
            logger.error(f"Error processing chat query: {str(e)}", exc_info=True)
            # Calculate execution time even for errors
            execution_time_ms = (time.time() - start_time) * 1000

            # Save error conversation
            db_error_conversation = ChatConversation(
                session_id=session.session_id if session else None,
                query_text=request.query_text,
                content=None,
                content_type=None,
                sql_generated=sql_query,
                execution_time_ms=str(execution_time_ms),
                error_message=str(e),
            )

            if session:
                db_error_conversation = self.chat_repository.save_conversation(
                    db, db_error_conversation
                )
                # Return error response with saved conversation
                return ChatQueryResponse.model_validate(db_error_conversation)

            raise e

    @transactional
    def delete_chat_session(self, db: Session, session_id: str) -> str:
        logger.info(f"Deleting chat session: {session_id}")
        session = self.chat_repository.get_chat_session(db, session_id)

        if not session:
            logger.warning(f"Chat session deletion failed: Session not found - {session_id}")
            raise AppException(
                http_status=404,
                code="SESSION_NOT_FOUND",
                message_key="session.not.found",
                params={"session_id": session_id},
                details={"session_id": session_id},
            )

        self.chat_repository.delete_chat_session(db, session_id)
        logger.info(f"Chat session deleted successfully: {session.title}, ID: {session_id}")
        return session.title
