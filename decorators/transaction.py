
from sqlalchemy.orm import Session
from functools import wraps
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

def transactional(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        db_session = None
        
        if 'db' in kwargs:
            db_session = kwargs['db']
        else:
            for arg in args:
                if isinstance(arg, Session):
                    db_session = arg
                    break
        
        if not db_session:
            return func(*args, **kwargs)
        
        try:
            result = func(*args, **kwargs)
            db_session.commit()
            logger.debug(f"Transaction committed for {func.__name__}")
            return result
        except Exception as e:
            db_session.rollback()
            logger.error(f"Transaction rolled back for {func.__name__}: {str(e)}")
            raise
    
    return wrapper


def db_transactional(auto_commit: bool = True):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Find the db session in the arguments
            db_session = None
            
            # Check if db is in kwargs
            if 'db' in kwargs:
                db_session = kwargs['db']
            else:
                # Check positional arguments for Session instance
                for arg in args:
                    if isinstance(arg, Session):
                        db_session = arg
                        break
            
            if not db_session:
                # If no session found, execute without transaction handling
                return func(*args, **kwargs)
            
            try:
                result = func(*args, **kwargs)
                if auto_commit:
                    db_session.commit()
                    logger.debug(f"Transaction auto-committed for {func.__name__}")
                return result
            except Exception as e:
                db_session.rollback()
                logger.error(f"Transaction rolled back for {func.__name__}: {str(e)}")
                raise
        
        return wrapper
    return decorator