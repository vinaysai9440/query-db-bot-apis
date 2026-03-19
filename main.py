
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import Base, engine
from routers.masters_router import router as masters_router
from routers.user_router import router as user_router
from routers.table_router import router as table_router
from routers.chat_router import router as chat_router
from routers.role_router import router as role_router
from routers.auth_router import router as auth_router
from messages.message_source import MessageSource
from exceptions.error_handlers import register_exception_handlers
from middleware.auth_middleware import JWTAuthMiddleware
from utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(log_level="INFO", log_file="logs/app.log")
logger = get_logger(__name__)

logger.info("Starting Query DB Bot APIs application")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Query DB Bot APIs - Conversational SQL Engine",
    description="Query DB Bot APIs - Conversational SQL Engine",
    version="1.0.0"
)

logger.info("FastAPI application initialized")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_message_source = MessageSource(path="messages/messages.properties")
register_exception_handlers(app, _message_source)

app.include_router(user_router)
app.include_router(table_router)
app.include_router(chat_router)
app.include_router(role_router)
app.include_router(auth_router)
app.include_router(masters_router)

logger.info("All routers registered successfully")
logger.info("Query DB Bot APIs application ready to accept requests")