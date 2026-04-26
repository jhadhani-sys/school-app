import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """Manages all database operations for school management system"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            # Use dynamic path from helper if available
            try:
                from utils.helpers import StorageHelper
                db_path = StorageHelper.get_storage_path('data/school.db')
            except Exception:
                db_path = 'data/school.db'
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary tables"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS school (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                email TEXT,
                principal TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                specialization TEXT,
                hire_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                level TEXT NOT NULL,
                teacher_id INTEGER,
                max_students INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(teacher_id) REFERENCES teachers(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                class_id INTEGER NOT NULL,
                enrollment_date TEXT,
                parent_name TEXT,
                parent_phone TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(class_id) REFERENCES classes(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                exam_type TEXT NOT NULL,
                score REAL NOT NULL,
                total_marks REAL DEFAULT 100,
                date TEXT,
                teacher_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(teacher_id) REFERENCES teachers(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                class_id INTEGER NOT NULL,
                term TEXT NOT NULL,
                total_marks REAL,
                percentage REAL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(class_id) REFERENCES classes(id)
            )
        ''')
        
        self.conn.commit()
        self.init_default_classes()
    
    def init_default_classes(self):
        """Create default middle-school classes if none exist"""
        existing = self.fetch_one('SELECT COUNT(*) FROM classes')
        if existing and existing[0] == 0:
            default_classes = [
                ('الأول متوسط', 'متوسطة'),
                ('الثاني متوسط', 'متوسطة'),
                ('الثالث متوسط', 'متوسطة')
            ]
            for name, level in default_classes:
                self.cursor.execute(
                    'INSERT INTO classes (name, level, max_students) VALUES (?, ?, ?)',
                    (name, level, 30)
                )
            self.conn.commit()
    
    def execute_query(self, query, params=()):
        """Execute a query and return results"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def fetch_one(self, query, params=()):
        """Fetch a single row"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def fetch_all(self, query, params=()):
        """Fetch all rows"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        self.close()

