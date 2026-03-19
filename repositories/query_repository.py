from sqlalchemy.orm import Session
from sqlalchemy import text, and_
from typing import List, Optional, Dict, Any
from datetime import datetime


class QueryRepository:

    def execute_sql_query(
        self, trans_db: Session, sql_query: str, fetch_limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Execute SQL query on the transactional database (not bot database)"""
        result = trans_db.execute(text(sql_query))

        columns = list(result.keys())

        if fetch_limit:
            rows = result.fetchmany(fetch_limit)
        else:
            rows = result.fetchall()

        return [
            {
                columns[i]: self._convert_oracle_value(row[i])
                for i in range(len(columns))
            }
            for row in rows
        ]

    def _convert_oracle_value(self, value: Any) -> Any:
        if value is None:
            return None
        elif isinstance(value, datetime):
            return value.isoformat()
        elif hasattr(value, "read"):
            return value.read()
        else:
            return value

    def validate_sql_query(self, sql_query: str) -> bool:
        sql_upper = sql_query.upper().strip()
        if sql_upper.startswith("SELECT"):
            dangerous_keywords = [
                "DROP",
                "DELETE",
                "INSERT",
                "UPDATE",
                "ALTER",
                "CREATE",
                "TRUNCATE",
            ]
            for keyword in dangerous_keywords:
                if keyword in sql_upper:
                    return False
            return True

        return False
