import os
from datetime import datetime
from typing import Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FileUtils:
    
    @staticmethod
    def ensure_directory_exists(directory_path: str) -> None:
        Path(directory_path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def generate_timestamp() -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def generate_csv_filename(session_id: str, timestamp: Optional[str] = None) -> str:
        if not timestamp:
            timestamp = FileUtils.generate_timestamp()
        
        return f"{session_id}_{timestamp}.csv"

    @staticmethod
    def get_csv_file_path(session_id: str, base_dir: str = "data/output") -> str:
        FileUtils.ensure_directory_exists(base_dir)
        filename = FileUtils.generate_csv_filename(session_id)
        return os.path.join(base_dir, filename)

    @staticmethod
    def get_file_size(file_path: str) -> int:
        try:
            return os.path.getsize(file_path)
        except OSError:
            return 0

    @staticmethod
    def file_exists(file_path: str) -> bool:
        return os.path.isfile(file_path)

    @staticmethod
    def delete_file(file_path: str) -> bool:
        try:
            if FileUtils.file_exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {str(e)}")
            return False

    @staticmethod
    def get_relative_path(file_path: str, base_path: str = ".") -> str:
        try:
            return os.path.relpath(file_path, base_path)
        except Exception:
            return file_path

