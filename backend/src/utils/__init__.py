import logging
from typing import Any, Dict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def format_response(data: Any, success: bool = True) -> Dict[str, Any]:
    """Format a standard API response"""
    return {
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }

def handle_error(error: Exception) -> Dict[str, Any]:
    """Handle and format error responses"""
    logger.error(f"Error occurred: {str(error)}", exc_info=True)
    return format_response({
        "error": str(error),
        "type": error.__class__.__name__
    }, success=False)

def validate_db_connection(db_url: str) -> bool:
    """Validate database connection string"""
    required_parts = ['postgresql://', '@', '/']
    return all(part in db_url for part in required_parts)
