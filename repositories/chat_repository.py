from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.chat import ChatSession, ChatConversation
from typing import List, Optional


class ChatRepository:

    def __init__(self):
        pass

    def create_chat_session(self, db: Session, user_id: str, title: str) -> ChatSession:
        if len(title) > 50:
            title = title[:47] + "..."
        session = ChatSession(
            user_id=user_id,
            title=title,
        )
        db.add(session)
        db.flush()
        db.refresh(session)
        return session

    def save_conversation(
        self, db: Session, conversation: ChatConversation
    ) -> ChatConversation:
        db.add(conversation)
        db.flush()
        db.refresh(conversation)
        return conversation

    def get_chat_session(self, db: Session, session_id: str) -> Optional[ChatSession]:
        return (
            db.query(ChatSession)
            .filter(
                and_(
                    ChatSession.session_id == session_id,
                    ChatSession.is_active == True,
                )
            )
            .first()
        )

    def get_user_chat_sessions(self, db: Session, user_id: str) -> List[ChatSession]:
        return (
            db.query(ChatSession)
            .filter(and_(ChatSession.user_id == user_id, ChatSession.is_active == True))
            .order_by(ChatSession.created_date.desc())
            .all()
        )

    def get_chat_conversations(
        self, db: Session, session_id: str, limit: int = 10
    ) -> List[ChatConversation]:
        return (
            db.query(ChatConversation)
            .filter(ChatConversation.session_id == session_id)
            .order_by(ChatConversation.created_date.desc())
            .limit(limit)
            .all()
        )

    def delete_chat_session(self, db: Session, session_id: str) -> Optional[str]:
        session = (
            db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        )
        if session:
            session.is_active = False
            db.commit()
            return session.title
        return None
