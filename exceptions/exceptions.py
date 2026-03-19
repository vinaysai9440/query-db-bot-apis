from typing import Optional, Dict, Any


class AppException(Exception):
    def __init__(
        self,
        http_status: int,
        code: str,
        message_key: str,
        params: Optional[Dict[str, Any]] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.http_status = http_status
        self.code = code
        self.message_key = message_key
        self.params = params or {}
        self.details = details or {}
        super().__init__(code)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "http_status": self.http_status,
            "code": self.code,
            "message_key": self.message_key,
            "params": self.params,
            "details": self.details,
        }
