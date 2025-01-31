from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

class BaseQuery:
    """Base class for database queries"""
    def __init__(self, db: Session):
        self.db = db

    def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a raw SQL query and return results as a list of dictionaries"""
        result = self.db.execute(query, params or {})
        return [dict(row) for row in result]

    def commit(self):
        """Commit the current transaction"""
        self.db.commit()

    def rollback(self):
        """Rollback the current transaction"""
        self.db.rollback()
