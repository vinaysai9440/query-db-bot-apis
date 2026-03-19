import subprocess
import re
import time
from typing import List
from models.chat import ChatConversation
from models.table import TableDef
from services.prompt_service import PromptService
from utils.logger import get_logger

logger = get_logger(__name__)

class LLMService:

    def __init__(self, model_name: str = "mistral"):
        self.model_name = model_name
        self.table_identification_timeout = 200
        self.sql_generation_timeout = 200
        self.title_generation_timeout = 200
        self.context_help_message_timeout = 200
        self.suggestions_generation_timeout = 150
        self.prompt_service = PromptService()

    def identify_relevant_tables(
        self, 
        query_text: str, 
        conversation_history: List[ChatConversation], 
        available_tables: List[TableDef]
    ) -> List[TableDef]:
        try:
            # Build table identification prompt using prompt service
            prompt = self.prompt_service.build_table_identification_prompt(
                query_text, conversation_history, available_tables
            )
            
            # Execute Ollama for table identification
            response = self._execute_ollama_request("table_identification", prompt, self.table_identification_timeout)
            
            # Parse the response to extract TableDef objects (integrated parsing logic)
            identified_tables = []
            
            # If response is empty or just whitespace, return empty list
            if not response.strip():
                return []
            
            # Create lookup dictionary for fast table matching
            available_table_lookup = {table.table_name.upper(): table for table in available_tables}
            
            # Clean and split the response
            lines = response.strip().split('\n')
            
            for line in lines:
                # Clean the line
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Remove common prefixes
                prefixes_to_remove = [
                    "table:", "tables:", "-", "*", "•", "1.", "2.", "3.", "4.", "5."
                ]
                
                for prefix in prefixes_to_remove:
                    if line.lower().startswith(prefix):
                        line = line[len(prefix):].strip()
                
                # Extract potential table name
                # Handle cases like "TABLE_NAME - description" or just "TABLE_NAME"
                table_name = line.split(' ')[0].split('-')[0].strip()
                
                # Skip if empty after cleaning
                if not table_name:
                    continue
                
                # Validate against available tables (case-insensitive)
                if table_name.upper() in available_table_lookup:
                    table_def = available_table_lookup[table_name.upper()]
                    if table_def not in identified_tables:
                        identified_tables.append(table_def)
            
            logger.info(f"LLM identified tables: {[table.table_name for table in identified_tables]}")
            return identified_tables
            
        except Exception as e:
            logger.warning(f"Table identification failed: {str(e)}")
            return []  # Return empty list to trigger user guidance

    def generate_sql_query(
        self, 
        query_text: str, 
        conversation_history: List[ChatConversation],
        tables_meta: List[TableDef]
    ) -> str:
        try:
            
            metadata_dicts = []
            for table in tables_meta:
                metadata_dicts.append(
                    {
                        "table_name": table.table_name,
                        "description": table.description,
                        "notes": table.notes,
                        "columns": table.get_columns(),
                        "sample_rows": table.get_sample_rows(),
                    }
                )
            
            # Build SQL generation prompt using prompt service
            prompt = self.prompt_service.build_sql_generation_prompt(
                query_text, conversation_history, metadata_dicts
            )
            
            # Execute Ollama for SQL generation
            response = self._execute_ollama_request("sql_generation", prompt, self.sql_generation_timeout)
            
            # Clean up the response
            sql_query = self._clean_sql_response(response)
            
            logger.info(f"LLM generated SQL: {sql_query}")
            return sql_query
            
        except Exception as e:
            logger.error(f"SQL generation failed: {str(e)}")
            raise

    def create_context_help_message(self, query_text: str, available_tables: List[TableDef]) -> str:
        try:
            # Build table suggestions prompt using prompt service
            prompt = self.prompt_service.build_context_help_message_prompt(
                query_text, available_tables
            )
            
            # Call Ollama with a shorter timeout for suggestions
            response = self._execute_ollama_request("context_help_message", prompt, self.context_help_message_timeout)
            
            # Clean up the response
            response = response.strip()
            
            # Ensure response is helpful
            if len(response) < 50 or not response:
                raise ValueError("Response too short or empty")
            
            return response
            
        except Exception as e:
            logger.warning(f"Failed to generate AI table suggestions: {e}")
            
            # Fallback to basic message if Ollama fails
            table_list = [
                f"- {table.table_name}"
                + (f": {table.description}" if table.description else "")
                for table in available_tables[:8]
            ]
            
            fallback_message = (
                "I wasn't able to clearly identify which business areas your request refers to. "
                "Please try to be more specific about the type of information you need.\n\n"
                f"Available data areas include:\n"
                + "\n".join(table_list)
                + (
                    f"\n... and {len(available_tables) - 8} more areas."
                    if len(available_tables) > 8
                    else ""
                )
            )
            
            return fallback_message

    def generate_session_title(self, query_text: str) -> str:
        try:
            prompt = self.prompt_service.build_session_title_prompt(query_text)
            
            # Use shorter timeout for title generation
            response = self._execute_ollama_request("session_title", prompt, self.title_generation_timeout)
            
            # Clean up the response
            title = response.strip()
            
            # Remove quotes if present
            title = title.strip('"\'')
            
            # Ensure title is not empty and within length limit
            if not title or len(title) < 3:
                raise ValueError("Generated title too short")
            
            # Truncate to 50 characters max
            if len(title) > 50:
                title = title[:47] + "..."
            
            logger.info(f"LLM generated session title: '{title}'")
            return title
            
        except Exception as e:
            logger.warning(f"Failed to generate session title: {e}")
            
            # Fallback: Use first part of query, cleaned up
            fallback_title = query_text.strip()
            
            # Remove common question words and clean up
            words_to_remove = ['please', 'can you', 'could you', 'show me', 'give me', 'i want', 'i need']
            for phrase in words_to_remove:
                fallback_title = fallback_title.lower().replace(phrase, '').strip()
            
            # Capitalize first letter
            if fallback_title:
                fallback_title = fallback_title[0].upper() + fallback_title[1:]
            
            # Truncate to 50 characters
            if len(fallback_title) > 50:
                fallback_title = fallback_title[:47] + "..."
            
            # Final fallback if still empty
            if not fallback_title:
                fallback_title = "New Chat Session"
            
            logger.info(f"Using fallback session title: '{fallback_title}'")
            return fallback_title

    def generate_query_suggestions(self, query_text: str, sql_query: str, result_count: int, result_columns: List[str], conversation_history: List[ChatConversation], tables_meta: List[TableDef]) -> List[str]:
        try:
            prompt = self.prompt_service.build_suggestions_prompt(
                query_text, sql_query, result_count, result_columns, conversation_history, tables_meta
            )
            
            response = self._execute_ollama_request("suggestions_generation", prompt, self.suggestions_generation_timeout)
            suggestions = self._parse_suggestions_response(response)
            
            logger.info(f"LLM generated {len(suggestions)} suggestions")
            return suggestions
            
        except Exception as e:
            logger.warning(f"Failed to generate suggestions: {str(e)}")
            # Return empty list if generation fails
            return []
    
    def _parse_suggestions_response(self, response: str) -> List[str]:
        """Parse LLM response to extract clean suggestions."""
        suggestions = []
        
        # Split by newlines and clean
        lines = response.strip().split('\n')
        
        for line in lines:
            # Clean the line
            line = line.strip()
            
            # Skip empty lines, headers, or explanatory text
            if not line or len(line) < 10:
                continue
            
            # Remove common prefixes (numbers, bullets, etc.)
            prefixes_to_remove = [
                r'^\d+\.\s*',  # "1. ", "2. ", etc.
                r'^[-*•]\s*',   # "- ", "* ", "• "
                r'^[a-zA-Z]\)\s*',  # "a) ", "b) ", etc.
            ]
            
            
            for pattern in prefixes_to_remove:
                line = re.sub(pattern, '', line)
            
            # Skip if it's a section header or meta text
            skip_patterns = [
                'suggestions:', 'next questions:', 'you could ask:', 
                'try asking:', 'here are', 'following questions',
                'related questions:', 'possible questions:'
            ]
            
            if any(skip.lower() in line.lower() for skip in skip_patterns):
                continue
            
            # Remove surrounding quotes if present
            line = line.strip('"\'')
            
            # Add if it looks like a valid question suggestion
            if line and len(line) >= 10 and len(line) <= 200:
                suggestions.append(line)
        
        # Limit to top 5 suggestions
        return suggestions[:5]

    def _execute_ollama_request(self, prompt_id: str, prompt: str, timeout: int) -> str:
        start_time = time.time()
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=timeout
            )
            
            if result.returncode != 0:
                error_msg = f"Ollama execution failed: {result.stderr}"
                raise Exception(error_msg)
            
            execution_time = time.time() - start_time
            logger.info(f"Ollama execution succeeded, prompt_id: {prompt_id}, time taken: {execution_time:.2f} seconds")
            return result.stdout.strip()
            
        except subprocess.TimeoutExpired:
            raise Exception(f"Ollama request timed out after {timeout} seconds")
        except FileNotFoundError:
            raise Exception("Ollama not found. Please install Ollama and ensure it's in PATH")

    def _clean_sql_response(self, response: str) -> str:
        # Remove markdown code blocks if present
        if '```sql' in response:
            # Extract content between ```sql and ```
            start = response.find('```sql') + 6
            end = response.find('```', start)
            if end != -1:
                response = response[start:end].strip()
        elif '```' in response:
            # Extract content between ``` blocks
            start = response.find('```') + 3
            end = response.find('```', start)
            if end != -1:
                response = response[start:end].strip()
        
        # Remove common prefixes that models might add
        prefixes_to_remove = [
            "Here's the SQL query:",
            "The SQL query is:",
            "Query:",
            "SQL:",
            "Answer:"
        ]
        
        for prefix in prefixes_to_remove:
            if response.lower().startswith(prefix.lower()):
                response = response[len(prefix):].strip()
        
        # Remove trailing semicolon and whitespace
        response = response.rstrip('; \n\r\t')
        
        return response