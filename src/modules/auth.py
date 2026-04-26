import hashlib
import os
import sys

# Handle imports for both direct run and packaged app
try:
    from src.database.db_manager import DatabaseManager
except ImportError:
    from database.db_manager import DatabaseManager

class AuthManager:
    """Manages user authentication"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.current_user = None
        self.init_default_admin()
    
    def init_default_admin(self):
        """Create default admin user if none exists"""
        result = self.db.fetch_one("SELECT * FROM users WHERE username = ?", ('admin',))
        if not result:
            password_hash = self._hash_password('admin123')
            self.db.execute_query(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ('admin', password_hash, 'admin')
            )
    
    @staticmethod
    def _hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username, password):
        """Authenticate user"""
        user = self.db.fetch_one(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        
        if user:
            stored_password = user[2]
            if self._hash_password(password) == stored_password:
                self.current_user = {
                    'id': user[0],
                    'username': user[1],
                    'role': user[3]
                }
                return True, "Login successful"
        
        return False, "Invalid username or password"
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get current logged-in user"""
        return self.current_user
    
    def create_user(self, username, password, role='teacher'):
        """Create new user (admin only)"""
        if self.current_user['role'] != 'admin':
            return False, "Only admins can create users"
        
        existing = self.db.fetch_one("SELECT * FROM users WHERE username = ?", (username,))
        if existing:
            return False, "Username already exists"
        
        password_hash = self._hash_password(password)
        success = self.db.execute_query(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        
        if success:
            return True, "User created successfully"
        else:
            return False, "Failed to create user"
    
    def change_password(self, old_password, new_password):
        """Change password for current user"""
        if not self.current_user:
            return False, "No user logged in"
        
        user = self.db.fetch_one(
            "SELECT * FROM users WHERE id = ?",
            (self.current_user['id'],)
        )
        
        if user:
            stored_password = user[2]
            if self._hash_password(old_password) == stored_password:
                new_hash = self._hash_password(new_password)
                success = self.db.execute_query(
                    "UPDATE users SET password = ? WHERE id = ?",
                    (new_hash, self.current_user['id'])
                )
                if success:
                    return True, "Password changed successfully"
        
        return False, "Invalid current password"

