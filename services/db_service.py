"""
Sentinel GRC - Database Service
Handles all database operations with proper connection management.
"""

import sqlite3
import logging
import threading
from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
import pandas as pd

from config import config, security_config
from utils.security import password_hasher

logger = logging.getLogger(__name__)


class DatabaseService:
    """
    Thread-safe database service with connection pooling.
    
    Uses SQLite with proper connection management and error handling.
    """
    
    _instance = None
    _lock = threading.Lock()
    _local = threading.local()
    
    def __new__(cls):
        """Singleton pattern for database service."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the database service."""
        if self._initialized:
            return
        
        self.db_file = config.DB_FILE
        self.timeout = config.DB_TIMEOUT
        self._initialized = True
        
        # Initialize the database schema
        self._init_schema()
    
    @contextmanager
    def get_connection(self):
        """
        Get a thread-local database connection.
        
        Yields:
            sqlite3.Connection: Database connection
            
        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(...)
        """
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            self._local.connection = sqlite3.connect(
                self.db_file,
                timeout=self.timeout,
                check_same_thread=False
            )
            self._local.connection.row_factory = sqlite3.Row
            # Enable foreign keys
            self._local.connection.execute("PRAGMA foreign_keys = ON")
        
        try:
            yield self._local.connection
            self._local.connection.commit()
        except Exception as e:
            self._local.connection.rollback()
            logger.error(f"Database error: {e}")
            raise
    
    def close_connection(self):
        """Close the thread-local connection."""
        if hasattr(self._local, 'connection') and self._local.connection:
            self._local.connection.close()
            self._local.connection = None
    
    def _init_schema(self):
        """Initialize database schema with all required tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table with enhanced security fields
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    api_key TEXT,
                    email TEXT,
                    role TEXT DEFAULT 'user',
                    is_active INTEGER DEFAULT 1,
                    failed_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            
            # Risks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS risks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_user TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    asset_name TEXT,
                    field1 TEXT,
                    field2 TEXT,
                    field3 TEXT,
                    field4 TEXT,
                    threat TEXT,
                    probability INTEGER,
                    impact INTEGER,
                    risk_score INTEGER,
                    risk_level TEXT,
                    mitigation TEXT,
                    status TEXT DEFAULT 'open',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (owner_user) REFERENCES users(username)
                )
            """)
            
            # Projects/Roadmap table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_user TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    phase TEXT,
                    initiative TEXT,
                    duration REAL,
                    cost REAL,
                    role TEXT,
                    kpi TEXT,
                    status TEXT DEFAULT 'planned',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (owner_user) REFERENCES users(username)
                )
            """)
            
            # Audit log table for security tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    action TEXT NOT NULL,
                    resource TEXT,
                    details TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Sessions table for session management
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_risks_owner ON risks(owner_user)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_risks_domain ON risks(domain)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_projects_owner ON projects(owner_user)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_projects_domain ON projects(domain)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_username ON audit_log(username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(session_token)")
            
            # Migrate existing data if needed
            self._migrate_legacy_data(cursor)
            
            # Create default admin user if not exists
            self._create_default_admin(cursor)
            
            conn.commit()
            logger.info("Database schema initialized successfully")
    
    def _migrate_legacy_data(self, cursor):
        """Migrate data from legacy schema if needed."""
        try:
            # Check if we need to migrate (old schema had different columns)
            cursor.execute("PRAGMA table_info(users)")
            columns = {row[1] for row in cursor.fetchall()}
            
            if 'password' in columns and 'password_hash' not in columns:
                # Old schema detected - rename column
                logger.info("Migrating legacy user schema...")
                cursor.execute("""
                    ALTER TABLE users RENAME COLUMN password TO password_hash
                """)
        except Exception as e:
            logger.debug(f"Migration check: {e}")
    
    def _create_default_admin(self, cursor):
        """Create default admin user if not exists."""
        cursor.execute("SELECT id FROM users WHERE username = ?", (security_config.ADMIN_USERNAME,))
        if not cursor.fetchone():
            admin_password = security_config.get_admin_password()
            password_hash = password_hasher.hash_password(admin_password)
            cursor.execute(
                """INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)""",
                (security_config.ADMIN_USERNAME, password_hash, 'admin')
            )
            logger.info(f"Created default admin user: {security_config.ADMIN_USERNAME}")


class UserRepository:
    """Repository for user-related database operations."""
    
    def __init__(self, db: DatabaseService):
        self.db = db
    
    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND is_active = 1",
                (username,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def create(self, username: str, password: str, email: str = None, role: str = 'user') -> bool:
        """
        Create a new user.
        
        Args:
            username: Unique username
            password: Plain text password (will be hashed)
            email: Optional email address
            role: User role (default: 'user')
            
        Returns:
            bool: True if created successfully
        """
        try:
            password_hash = password_hasher.hash_password(password)
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO users (username, password_hash, email, role)
                       VALUES (?, ?, ?, ?)""",
                    (username, password_hash, email, role)
                )
                logger.info(f"User created: {username}")
                return True
        except sqlite3.IntegrityError:
            logger.warning(f"User creation failed - username exists: {username}")
            return False
        except Exception as e:
            logger.error(f"User creation error: {e}")
            return False
    
    def verify_password(self, username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """
        Verify user password.
        
        Args:
            username: Username to verify
            password: Password to check
            
        Returns:
            Tuple of (success, user_data)
        """
        user = self.get_by_username(username)
        if not user:
            return False, None
        
        if password_hasher.verify_password(password, user['password_hash']):
            # Check if password needs rehashing (legacy format)
            if password_hasher.needs_rehash(user['password_hash']):
                self._update_password_hash(username, password)
            
            # Update last login
            self._update_last_login(username)
            return True, user
        
        return False, None
    
    def _update_password_hash(self, username: str, password: str):
        """Upgrade password hash to current format."""
        new_hash = password_hasher.hash_password(password)
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = ?, updated_at = ? WHERE username = ?",
                (new_hash, datetime.now(), username)
            )
        logger.info(f"Upgraded password hash for user: {username}")
    
    def _update_last_login(self, username: str):
        """Update user's last login timestamp."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE username = ?",
                (datetime.now(), username)
            )
    
    def delete(self, username: str) -> bool:
        """
        Delete a user and all associated data.
        
        Args:
            username: Username to delete
            
        Returns:
            bool: True if deleted
        """
        if username == security_config.ADMIN_USERNAME:
            logger.warning("Cannot delete admin user")
            return False
        
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                # Delete associated data
                cursor.execute("DELETE FROM risks WHERE owner_user = ?", (username,))
                cursor.execute("DELETE FROM projects WHERE owner_user = ?", (username,))
                cursor.execute("DELETE FROM sessions WHERE username = ?", (username,))
                # Delete user
                cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                logger.info(f"User deleted: {username}")
                return True
        except Exception as e:
            logger.error(f"User deletion error: {e}")
            return False
    
    def get_all(self) -> pd.DataFrame:
        """Get all users as DataFrame."""
        with self.db.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT username, email, role, is_active, created_at, last_login FROM users",
                conn
            )
    
    def update_api_key(self, username: str, api_key: str) -> bool:
        """Update user's API key."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET api_key = ?, updated_at = ? WHERE username = ?",
                    (api_key, datetime.now(), username)
                )
                return True
        except Exception as e:
            logger.error(f"API key update error: {e}")
            return False


class RiskRepository:
    """Repository for risk-related database operations."""
    
    def __init__(self, db: DatabaseService):
        self.db = db
    
    def create(
        self,
        owner: str,
        domain: str,
        asset_name: str,
        field1: str,
        field2: str,
        field3: str,
        field4: str,
        threat: str,
        probability: int,
        impact: int,
        risk_score: int,
        risk_level: str,
        mitigation: str
    ) -> bool:
        """Create a new risk entry."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO risks 
                       (owner_user, domain, asset_name, field1, field2, field3, field4,
                        threat, probability, impact, risk_score, risk_level, mitigation)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (owner, domain, asset_name, field1, field2, field3, field4,
                     threat, probability, impact, risk_score, risk_level, mitigation)
                )
                return True
        except Exception as e:
            logger.error(f"Risk creation error: {e}")
            return False
    
    def get_by_owner(self, owner: str, domain: str = None) -> pd.DataFrame:
        """Get risks by owner, optionally filtered by domain."""
        try:
            with self.db.get_connection() as conn:
                if domain:
                    return pd.read_sql_query(
                        "SELECT * FROM risks WHERE owner_user = ? AND domain = ? ORDER BY created_at DESC",
                        conn,
                        params=(owner, domain)
                    )
                return pd.read_sql_query(
                    "SELECT * FROM risks WHERE owner_user = ? ORDER BY created_at DESC",
                    conn,
                    params=(owner,)
                )
        except Exception as e:
            logger.error(f"Risk fetch error: {e}")
            return pd.DataFrame()
    
    def update_status(self, risk_id: int, status: str) -> bool:
        """Update risk status."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE risks SET status = ?, updated_at = ? WHERE id = ?",
                    (status, datetime.now(), risk_id)
                )
                return True
        except Exception as e:
            logger.error(f"Risk status update error: {e}")
            return False
    
    def delete_by_owner(self, owner: str) -> bool:
        """Delete all risks for an owner."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM risks WHERE owner_user = ?", (owner,))
                return True
        except Exception as e:
            logger.error(f"Risk deletion error: {e}")
            return False


class ProjectRepository:
    """Repository for project/roadmap database operations."""
    
    def __init__(self, db: DatabaseService):
        self.db = db
    
    def save_roadmap(self, owner: str, domain: str, df: pd.DataFrame) -> bool:
        """Save roadmap data, replacing existing entries for the domain."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                # Clear existing entries
                cursor.execute(
                    "DELETE FROM projects WHERE owner_user = ? AND domain = ?",
                    (owner, domain)
                )
                # Insert new entries
                for _, row in df.iterrows():
                    cursor.execute(
                        """INSERT INTO projects 
                           (owner_user, domain, phase, initiative, duration, cost, role, kpi)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (owner, domain, row.get("Phase"), row.get("Initiative"),
                         row.get("Duration"), row.get("Cost"), row.get("Role"), row.get("KPI"))
                    )
                return True
        except Exception as e:
            logger.error(f"Roadmap save error: {e}")
            return False
    
    def get_by_owner(self, owner: str, domain: str = None) -> pd.DataFrame:
        """Get projects by owner, optionally filtered by domain."""
        try:
            with self.db.get_connection() as conn:
                if domain:
                    df = pd.read_sql_query(
                        "SELECT * FROM projects WHERE owner_user = ? AND domain = ? ORDER BY created_at",
                        conn,
                        params=(owner, domain)
                    )
                else:
                    df = pd.read_sql_query(
                        "SELECT * FROM projects WHERE owner_user = ? ORDER BY created_at",
                        conn,
                        params=(owner,)
                    )
                
                if not df.empty:
                    # Normalize column names
                    df.columns = [c.capitalize() for c in df.columns]
                    
                    # Add computed date columns for Gantt chart
                    df["Duration"] = pd.to_numeric(df["Duration"], errors="coerce").fillna(1)
                    start = datetime.today()
                    df["Start"] = [start + pd.DateOffset(months=i * 3) for i in range(len(df))]
                    df["Finish"] = [
                        s + pd.DateOffset(months=int(d))
                        for s, d in zip(df["Start"], df["Duration"])
                    ]
                
                return df
        except Exception as e:
            logger.error(f"Project fetch error: {e}")
            return pd.DataFrame()
    
    def delete_by_owner(self, owner: str) -> bool:
        """Delete all projects for an owner."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM projects WHERE owner_user = ?", (owner,))
                return True
        except Exception as e:
            logger.error(f"Project deletion error: {e}")
            return False


class AuditLogRepository:
    """Repository for audit logging."""
    
    def __init__(self, db: DatabaseService):
        self.db = db
    
    def log(
        self,
        action: str,
        username: str = None,
        resource: str = None,
        details: str = None,
        ip_address: str = None,
        user_agent: str = None
    ):
        """Log an audit event."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO audit_log 
                       (username, action, resource, details, ip_address, user_agent)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (username, action, resource, details, ip_address, user_agent)
                )
        except Exception as e:
            logger.error(f"Audit log error: {e}")
    
    def get_recent(self, limit: int = 100) -> pd.DataFrame:
        """Get recent audit log entries."""
        try:
            with self.db.get_connection() as conn:
                return pd.read_sql_query(
                    "SELECT * FROM audit_log ORDER BY created_at DESC LIMIT ?",
                    conn,
                    params=(limit,)
                )
        except Exception as e:
            logger.error(f"Audit log fetch error: {e}")
            return pd.DataFrame()


class StatisticsService:
    """Service for database statistics."""
    
    def __init__(self, db: DatabaseService):
        self.db = db
    
    def get_stats(self) -> Dict[str, Any]:
        """Get overall database statistics."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            user_count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            risk_count = cursor.execute("SELECT COUNT(*) FROM risks").fetchone()[0]
            project_count = cursor.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
            
            users_df = pd.read_sql_query("SELECT username, role FROM users", conn)
            
            return {
                "user_count": user_count,
                "risk_count": risk_count,
                "project_count": project_count,
                "users": users_df
            }


# =============================================================================
# SINGLETON INSTANCES
# =============================================================================

# Create database service singleton
db_service = DatabaseService()

# Create repository instances
user_repo = UserRepository(db_service)
risk_repo = RiskRepository(db_service)
project_repo = ProjectRepository(db_service)
audit_log = AuditLogRepository(db_service)
stats_service = StatisticsService(db_service)
