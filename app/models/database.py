import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_path='dataset_bit.db'):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.get_connection()
        c = conn.cursor()

        # 创建文件表
        c.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                filetype TEXT NOT NULL,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')

        # 创建文本片段表
        c.execute('''
            CREATE TABLE IF NOT EXISTS segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER,
                content TEXT NOT NULL,
                segment_index INTEGER NOT NULL,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (file_id) REFERENCES files (id)
            )
        ''')

        # 创建问答对表
        c.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                accuracy_score REAL DEFAULT 0,
                completeness_score REAL DEFAULT 0,
                relevance_score REAL DEFAULT 0,
                clarity_score REAL DEFAULT 0,
                total_score REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建评分历史记录表
        c.execute('''
            CREATE TABLE IF NOT EXISTS score_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                qa_id INTEGER NOT NULL,
                accuracy_score REAL NOT NULL,
                completeness_score REAL NOT NULL,
                relevance_score REAL NOT NULL,
                clarity_score REAL NOT NULL,
                total_score REAL NOT NULL,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (qa_id) REFERENCES qa_pairs (id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_file(self, filename, filepath, filetype):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO files (filename, filepath, filetype) VALUES (?, ?, ?)",
            (filename, filepath, filetype)
        )
        file_id = c.lastrowid
        conn.commit()
        conn.close()
        return file_id

    def get_file(self, file_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM files WHERE id = ?", (file_id,))
        file = c.fetchone()
        conn.close()
        return dict(file) if file else None

    def get_files(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM files ORDER BY upload_time DESC")
        files = [dict(row) for row in c.fetchall()]
        conn.close()
        return files

    def update_file_status(self, file_id, status):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(
            "UPDATE files SET status = ? WHERE id = ?",
            (status, file_id)
        )
        conn.commit()
        conn.close()

    def delete_file(self, file_id):
        conn = self.get_connection()
        c = conn.cursor()
        
        # 获取文件信息
        c.execute("SELECT * FROM files WHERE id = ?", (file_id,))
        file = c.fetchone()
        if file:
            # 删除物理文件
            try:
                os.remove(file['filepath'])
            except OSError:
                pass

            # 删除相关的问答对
            c.execute("""
                DELETE FROM qa_pairs 
                WHERE segment_id IN (
                    SELECT id FROM segments WHERE file_id = ?
                )
            """, (file_id,))

            # 删除相关的文本片段
            c.execute("DELETE FROM segments WHERE file_id = ?", (file_id,))

            # 删除文件记录
            c.execute("DELETE FROM files WHERE id = ?", (file_id,))

            conn.commit()
        conn.close()

    def add_segment(self, file_id, content, segment_index):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO segments (file_id, content, segment_index) VALUES (?, ?, ?)",
            (file_id, content, segment_index)
        )
        segment_id = c.lastrowid
        conn.commit()
        conn.close()
        return segment_id

    def get_segments(self, file_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM segments WHERE file_id = ? ORDER BY segment_index",
            (file_id,)
        )
        segments = [dict(row) for row in c.fetchall()]
        conn.close()
        return segments

    def add_qa_pair(self, segment_id, question, answer, quality_score=0):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO qa_pairs (segment_id, question, answer, quality_score)
            VALUES (?, ?, ?, ?)
            """,
            (segment_id, question, answer, quality_score)
        )
        qa_id = c.lastrowid
        conn.commit()
        conn.close()
        return qa_id

    def get_qa_pairs(self, segment_id=None):
        conn = self.get_connection()
        c = conn.cursor()
        if segment_id:
            c.execute(
                "SELECT * FROM qa_pairs WHERE segment_id = ? ORDER BY created_time",
                (segment_id,)
            )
        else:
            c.execute("SELECT * FROM qa_pairs ORDER BY created_time")
        qa_pairs = [dict(row) for row in c.fetchall()]
        conn.close()
        return qa_pairs

    def update_qa_scores(self, qa_id, scores):
        """更新问答对评分"""
        conn = self.get_connection()
        c = conn.cursor()
        
        # 更新问答对表
        c.execute(
            "UPDATE qa_pairs SET accuracy_score = ?, completeness_score = ?, relevance_score = ?, clarity_score = ?, total_score = ?, updated_at = ? WHERE id = ?",
            (scores['accuracy'], scores['completeness'], scores['relevance'], scores['clarity'], scores['total'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), qa_id)
        )
        
        # 添加评分历史记录
        c.execute(
            "INSERT INTO score_history (qa_id, accuracy_score, completeness_score, relevance_score, clarity_score, total_score, feedback) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (qa_id, scores['accuracy'], scores['completeness'], scores['relevance'], scores['clarity'], scores['total'], scores.get('feedback', ''))
        )
        
        conn.commit()
        conn.close()

    def get_score_history(self, qa_id, limit=10):
        """获取评分历史记录"""
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT * FROM score_history 
            WHERE qa_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (qa_id, limit))
        history = [dict(row) for row in c.fetchall()]
        conn.close()
        return history

# 添加create_tables函数
def create_tables():
    db = Database()
    db.init_db() 