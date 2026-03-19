from typing import List
from sqlalchemy.orm import Session
from schemas.table import TableDefOut
from services.table_service import TableService
from utils.logger import get_logger

logger = get_logger(__name__)


class MastersService:
    def __init__(self, table_service: TableService):
        self.table_service = table_service

    def get_permissions(self, db: Session) -> List[str]:
        logger.debug("Retrieving all permissions")
        permissions = [
            "modules.roles",
            "modules.users",
            "modules.schemas",
            "modules.analytics",
        ]
        tables: List[TableDefOut] = self.table_service.list(db, 0, 10000)
        for table in tables:
            permissions.append(f"tables.{table.table_name}")
        logger.info(f"Retrieved {len(permissions)} total permissions ({len(tables)} table-based)")
        return permissions
