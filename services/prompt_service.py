import os
from typing import List, Dict, Any
from models.chat import ChatConversation
from models.table import TableDef
from utils.logger import get_logger

logger = get_logger(__name__)


class PromptService:

    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        self._template_cache = {}

    def _load_template(self, template_name: str) -> str:
        if template_name in self._template_cache:
            return self._template_cache[template_name]

        template_path = os.path.join(self.templates_dir, f"{template_name}.txt")

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()

            self._template_cache[template_name] = template_content
            logger.debug(f"Loaded template: {template_name}")
            return template_content

        except FileNotFoundError:
            logger.error(f"Template file not found: {template_path}")
            raise FileNotFoundError(f"Prompt template '{template_name}' not found")

    def build_table_identification_prompt(
        self,
        query_text: str,
        conversation_history: List[ChatConversation],
        available_tables: List[TableDef],
    ) -> str:
        template = self._load_template("table_identification")

        # Build conversation history section
        conversation_section = ""
        if conversation_history:
            conversation_section = "--- RECENT CONVERSATION ---\n"
            for conv in conversation_history[-3:]:  # Last 3 conversations for context
                conversation_section += f"User: {conv.query_text}\n"
                if conv.sql_generated:
                    conversation_section += f"SQL: {conv.sql_generated}\n"
            conversation_section += "\n"

        # Build available tables list
        tables_list = []
        for table in available_tables:
            table_line = table.table_name
            if table.description:
                table_line += f" - {table.description}"
            if table.notes:
                table_line += f" - {table.notes}"
            tables_list.append(table_line)

        # Format the template
        formatted_prompt = template.format(
            conversation_history_section=conversation_section,
            available_tables="\n".join(tables_list),
            query_text=query_text,
        )

        return formatted_prompt

    def build_sql_generation_prompt(
        self,
        query_text: str,
        conversation_history: List[ChatConversation],
        table_metadata: List[Dict[str, Any]],
    ) -> str:
        template = self._load_template("sql_generation")

        # Build conversation history section
        conversation_section = ""
        if conversation_history:
            conversation_section = "--- CONVERSATION HISTORY ---\n"
            for conv in conversation_history:
                conversation_section += f"User: {conv.query_text}\n"
                if conv.sql_generated:
                    conversation_section += f"SQL: {conv.sql_generated}\n"
            conversation_section += "\n"

        # Build database schema section
        schema_sections = []
        for table in table_metadata:
            schema_section = f"Table: {table['table_name']}\n"

            if table.get("description"):
                schema_section += f"Description: {table['description']}\n"

            if table.get("columns"):
                schema_section += "Columns:\n"
                for col in table["columns"]:
                    col_info = f"  - {col.get('name', 'unknown')}"
                    if "type" in col:
                        col_info += f" ({col['type']})"
                    if "description" in col:
                        col_info += f" - {col['description']}"
                    schema_section += col_info + "\n"

            if table.get("sample_rows"):
                schema_section += "Sample data:\n"
                for i, row in enumerate(
                    table["sample_rows"][:2]
                ):  # Show max 2 sample rows
                    schema_section += f"  Row {i+1}: {row}\n"

            schema_sections.append(schema_section)

        # Format the template
        formatted_prompt = template.format(
            conversation_history_section=conversation_section,
            database_schema="\n".join(schema_sections),
            query_text=query_text,
        )

        return formatted_prompt

    def build_context_help_message_prompt(
        self, query_text: str, available_tables: List[TableDef]
    ) -> str:
        template = self._load_template("context_help_message")

        # Build table context for the prompt
        table_info_lines = []
        for table in available_tables[
            :20
        ]:  # Limit to first 20 tables to avoid token limits
            desc_part = f" - {table.description}" if table.description else ""
            table_info_lines.append(f"  • {table.table_name}{desc_part}")

        table_context = "\n".join(table_info_lines)
        if len(available_tables) > 20:
            table_context += f"\n  ... and {len(available_tables) - 20} more tables"

        # Format the template
        formatted_prompt = template.format(
            query_text=query_text, table_context=table_context
        )

        return formatted_prompt

    def build_session_title_prompt(self, query_text: str) -> str:
        template = self._load_template("session_title")

        # Format the template
        formatted_prompt = template.format(query_text=query_text)

        return formatted_prompt

    def build_suggestions_prompt(
        self,
        query_text: str,
        sql_query: str,
        result_count: int,
        result_columns: List[str],
        conversation_history: List[ChatConversation],
        tables_meta: List[TableDef],
    ) -> str:
        template = self._load_template("suggestions")

        # Build conversation history section
        conversation_section = ""
        if conversation_history:
            conversation_section = "--- RECENT CONVERSATION HISTORY ---\n"
            for conv in conversation_history[-5:]:  # Last 5 conversations for context
                conversation_section += f"User asked: {conv.query_text}\n"
                if conv.sql_generated:
                    conversation_section += f"SQL generated: {conv.sql_generated}\n"
            conversation_section += "\n"

        # Build results summary (metadata only, no actual data)
        results_summary = "No results returned"
        if result_count > 0:
            results_summary = f"Returned {result_count} row(s)\n"
            
            # Show only column names (no actual data)
            if result_columns:
                results_summary += f"Columns: {', '.join(result_columns)}\n"

        # Build tables context
        tables_context = ""
        if tables_meta:
            tables_context = "Tables used in this query:\n"
            for table in tables_meta:
                tables_context += f"  • {table.table_name}"
                if table.description:
                    tables_context += f" - {table.description}"
                tables_context += "\n"
                
                # Show key columns
                if table.get_columns():
                    key_cols = [col['name'] for col in table.get_columns()[:5]]
                    tables_context += f"    Key columns: {', '.join(key_cols)}\n"

        # Format the template
        formatted_prompt = template.format(
            query_text=query_text,
            sql_query=sql_query,
            results_summary=results_summary,
            conversation_history_section=conversation_section,
            tables_context=tables_context,
        )

        return formatted_prompt
