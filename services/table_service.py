from sqlalchemy.orm import Session
from schemas.table import TableDefCreate, TableDefUpdate, TableDefOut
from repositories.table_repository import TableRepository
from mappers.table_mapper import TableMapper
from models.table import TableDef
from decorators.transaction import transactional
from exceptions.exceptions import AppException
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)


class TableService:
    def __init__(self, table_repository: TableRepository):
        self.table_repository = table_repository

    @transactional
    def create_table(self, db: Session, payload: TableDefCreate) -> TableDefOut:
        logger.info(f"Creating new table definition: {payload.table_name}")
        existing = self.table_repository.get_by_name(db, payload.table_name)
        if existing:
            logger.warning(f"Table creation failed: Table already exists - {payload.table_name}")
            raise AppException(
                http_status=400,
                code="TABLE_ALREADY_EXISTS",
                message_key="table.already.exists",
                params={"table_name": payload.table_name},
                details={"table_name": payload.table_name},
            )
        tabel_def: TableDef = TableMapper.to_table_def_for_create(payload)
        db_td: TableDef = self.table_repository.create(db, tabel_def)
        logger.info(f"Table definition created successfully: {db_td.table_name}, ID: {db_td.id}")
        return TableMapper.to_table_def_out(db_td)

    @transactional
    def update_table(
        self, db: Session, td_id: str, payload: TableDefUpdate
    ) -> TableDefOut:
        logger.info(f"Updating table definition: {td_id}")
        existing = self.table_repository.get_by_id(db, td_id)
        if not existing:
            logger.warning(f"Table update failed: Table not found - {td_id}")
            raise AppException(
                http_status=400,
                code="TABLE_NOT_FOUND",
                message_key="table.not.found",
                params={"table_id": td_id},
                details={"table_id": td_id},
            )
        TableMapper.apply_update(existing, payload)
        db_td: TableDef = self.table_repository.update(db, existing)
        logger.info(f"Table definition updated successfully: {db_td.table_name}, ID: {td_id}")
        return TableMapper.to_table_def_out(db_td)

    @transactional
    def delete(self, db: Session, td_id: str) -> str:
        logger.info(f"Deleting table definition: {td_id}")
        db_table: TableDef = self.table_repository.get_by_id(db, td_id)
        if not db_table:
            logger.warning(f"Table deletion failed: Table not found - {td_id}")
            raise AppException(
                http_status=404,
                code="TABLE_NOT_FOUND",
                message_key="table.delete.not.found",
                params={"table_id": td_id},
                details={"table_id": td_id},
            )
        self.table_repository.delete(db, db_table)
        logger.info(f"Table definition deleted successfully: {db_table.table_name}, ID: {td_id}")
        return db_table.table_name

    def list(self, db: Session, skip: int, limit: int) -> List[TableDefOut]:
        logger.debug(f"Listing table definitions with skip={skip}, limit={limit}")
        tables: List[TableDef] = self.table_repository.list(db, skip=skip, limit=limit)
        logger.info(f"Retrieved {len(tables)} table definitions")
        return TableMapper.to_table_def_out_list(tables)

    def get_by_id(self, db: Session, td_id: str) -> TableDefOut:
        logger.debug(f"Retrieving table definition by ID: {td_id}")
        table: TableDef = self.table_repository.get_by_id(db, td_id)
        if not table:
            logger.warning(f"Table definition not found: {td_id}")
            raise AppException(
                http_status=404,
                code="TABLE_NOT_FOUND",
                message_key="table.not.found",
                params={"table_id": td_id},
                details={"table_id": td_id},
            )
        logger.debug(f"Table definition retrieved: {table.table_name}")
        return TableMapper.to_table_def_out(table)
