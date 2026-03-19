from utils.file_utils import FileUtils
from typing import List, Dict, Any, Optional

import logging
import os
import csv
import json

logger = logging.getLogger(__name__)

class CSVExporter:
    
    def __init__(self, base_output_dir: str = "data/output"):
        self.base_output_dir = base_output_dir
        FileUtils.ensure_directory_exists(base_output_dir)

    def export_query_results(
        self, 
        data: List[Dict[str, Any]], 
        session_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        file_path = FileUtils.get_csv_file_path(session_id, self.base_output_dir)
        
        if self.export_to_csv(data, file_path):
            return file_path
        else:
            raise Exception(f"Failed to export CSV file: {file_path}")

    def get_preview_data(
        self, 
        data: List[Dict[str, Any]], 
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        if len(data) <= limit:
            return data
        else:
            return data[-limit:]  # Return last N rows

    @staticmethod
    def export_to_csv(
        data: List[Dict[str, Any]], 
        file_path: str, 
        encoding: str = 'utf-8'
    ) -> bool:
        try:
            if not data:
                logger.warning("No data to export to CSV")
                return False

            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            FileUtils.ensure_directory_exists(directory)

            # Get column names from the first row
            fieldnames = list(data[0].keys())
            
            with open(file_path, 'w', newline='', encoding=encoding) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in data:
                    # Convert complex data types to strings for CSV compatibility
                    csv_row = {}
                    for key, value in row.items():
                        if isinstance(value, (dict, list)):
                            csv_row[key] = json.dumps(value)
                        elif value is None:
                            csv_row[key] = ''
                        else:
                            csv_row[key] = str(value)
                    
                    writer.writerow(csv_row)
            
            logger.info(f"Successfully exported {len(data)} rows to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export data to CSV: {str(e)}")
            return False

    @staticmethod
    def read_csv(file_path: str, encoding: str = 'utf-8') -> List[Dict[str, Any]]:
        try:
            data = []
            with open(file_path, 'r', encoding=encoding) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(dict(row))
            
            logger.info(f"Successfully read {len(data)} rows from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to read CSV file: {str(e)}")
            return []
