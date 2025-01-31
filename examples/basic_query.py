from typing import List, Dict, Any
from database import get_db, init_db
from query import BaseQuery
from utils import format_response, handle_error

class UserQuery(BaseQuery):
    """Example query class for user-related operations"""
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Get user by ID"""
        try:
            result = self.execute(
                "SELECT * FROM users WHERE id = :id",
                {"id": user_id}
            )
            return format_response(result[0] if result else None)
        except Exception as e:
            return handle_error(e)
    
    def get_all_users(self) -> Dict[str, Any]:
        """Get all users"""
        try:
            result = self.execute("SELECT * FROM users ORDER BY id")
            return format_response(result)
        except Exception as e:
            return handle_error(e)
    
    def create_user(self, username: str, email: str) -> Dict[str, Any]:
        """Create a new user"""
        try:
            result = self.execute(
                """
                INSERT INTO users (username, email)
                VALUES (:username, :email)
                RETURNING id, username, email
                """,
                {"username": username, "email": email}
            )
            self.commit()
            return format_response(result[0])
        except Exception as e:
            self.rollback()
            return handle_error(e)

def example_usage():
    """Demonstrate how to use the UserQuery class"""
    try:
        # Initialize database (creates tables if they don't exist)
        init_db()
        
        # Get database session
        db = next(get_db())
        
        # Create query instance
        user_query = UserQuery(db)
        
        # Example operations
        print("Creating new user...")
        create_result = user_query.create_user(
            username="john_doe",
            email="john@example.com"
        )
        print(f"Create result: {create_result}")
        
        print("\nGetting all users...")
        users_result = user_query.get_all_users()
        print(f"All users: {users_result}")
        
        if users_result["success"] and users_result["data"]:
            user_id = users_result["data"][0]["id"]
            print(f"\nGetting user with ID {user_id}...")
            user_result = user_query.get_user_by_id(user_id)
            print(f"Single user: {user_result}")
            
    except Exception as e:
        print(f"Error in example: {str(e)}")

if __name__ == "__main__":
    example_usage()
