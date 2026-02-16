import sqlite3

class MoodboardDB:
    def __init__(self, db_path="moodboard.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """
        Create all necessary tables if they don't exist
        """
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                image_data BLOB NOT NULL,
                original_filename TEXT,
                width INTEGER,
                height INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS canvas_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                image_id INTEGER NOT NULL,
                x REAL NOT NULL,
                y REAL NOT NULL,
                display_width REAL NOT NULL,
                display_height REAL NOT NULL,
                z_index INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS staging_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                image_id INTEGER NOT NULL,
                position_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
            );
            
            CREATE INDEX IF NOT EXISTS idx_canvas_project ON canvas_items(project_id);
            CREATE INDEX IF NOT EXISTS idx_staging_project ON staging_items(project_id);
        ''')
        self.conn.commit()
    
    def close(self):
        """
        Close database connection
        """
        self.conn.close()
