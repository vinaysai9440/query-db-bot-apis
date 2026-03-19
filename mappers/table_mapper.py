from typing import List
from models.table import TableDef
from schemas.table import TableDefOut, TableDefCreate, TableDefUpdate


class TableMapper:

    @staticmethod
    def to_table_def_out(table: TableDef) -> TableDefOut:
        return TableDefOut(
            id=table.id,
            table_name=table.table_name,
            description=table.description,
            notes=table.notes,
            is_active=table.is_active,
            columns=table.get_columns(),
            sample_rows=table.get_sample_rows(),
            created_by=table.created_by,
            created_date=table.created_date,
            updated_by=table.updated_by,
            updated_date=table.updated_date,
        )

    @staticmethod
    def to_table_def_out_list(tables: List[TableDef]) -> List[TableDefOut]:
        return [TableMapper.to_table_def_out(table) for table in tables]

    @staticmethod
    def to_table_def_for_create(table_in: TableDefCreate) -> TableDef:
        db_td = TableDef(
            table_name=table_in.table_name,
            description=table_in.description,
            notes=table_in.notes,
            is_active=table_in.is_active if table_in.is_active is not None else True,
            created_by=table_in.created_by,
        )
        db_td.set_columns(table_in.columns or [])
        db_td.set_sample_rows(table_in.sample_rows or [])
        return db_td

    @staticmethod
    def apply_update(existing: TableDef, table_in: TableDefUpdate) -> TableDef:
        existing.table_name = table_in.table_name or existing.table_name
        existing.description = table_in.description or existing.description
        existing.notes = table_in.notes or existing.notes
        existing.is_active = (
            table_in.is_active if table_in.is_active is not None else existing.is_active
        )
        existing.updated_by = table_in.updated_by or existing.updated_by
        existing.set_columns(table_in.columns or existing.get_columns())
        existing.set_sample_rows(table_in.sample_rows or existing.get_sample_rows())
        return existing