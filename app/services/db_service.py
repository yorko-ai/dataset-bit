import sqlite3
import json
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DBService:
    def __init__(self, db_path: str = "dataset_bit.db"):
        """初始化数据库服务"""
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """初始化数据库表"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                
                # 创建文件表
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)

                # 创建文本段落表
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS text_segments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    segment_index INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (file_id) REFERENCES files (id)
                )
                """)

                # 创建问答对表
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS qa_pairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    segment_id INTEGER NOT NULL,
                    file_id INTEGER NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    quality_scores TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (segment_id) REFERENCES text_segments (id),
                    FOREIGN KEY (file_id) REFERENCES files (id)
                )
                """)

                # 检查是否需要添加file_id字段
                cursor.execute("PRAGMA table_info(qa_pairs)")
                columns = [row[1] for row in cursor.fetchall()]
                if 'file_id' not in columns:
                    cursor.execute("ALTER TABLE qa_pairs ADD COLUMN file_id INTEGER")
                    # 补全历史数据
                    cursor.execute("""
                    UPDATE qa_pairs 
                    SET file_id = (
                        SELECT file_id 
                        FROM text_segments 
                        WHERE text_segments.id = qa_pairs.segment_id
                    )
                    WHERE file_id IS NULL
                    """)

                conn.commit()
        except Exception as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            raise

    def get_conn(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def save_file(self, filename: str, file_path: str, file_type: str, file_size: int) -> int:
        """保存文件信息"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO files (filename, file_path, file_type, file_size)
                VALUES (?, ?, ?, ?)
                """, (filename, file_path, file_type, file_size))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"保存文件信息失败: {str(e)}")
            raise

    def save_text_segments(self, file_id: int, segments: List[str]) -> List[int]:
        """保存文本段落"""
        try:
            segment_ids = []
            with self.get_conn() as conn:
                cursor = conn.cursor()
                for i, segment in enumerate(segments):
                    cursor.execute("""
                    INSERT INTO text_segments (file_id, content, segment_index)
                    VALUES (?, ?, ?)
                    """, (file_id, segment, i))
                    segment_ids.append(cursor.lastrowid)
                conn.commit()
            return segment_ids
        except Exception as e:
            logger.error(f"保存文本段落失败: {str(e)}")
            raise

    def save_qa_pairs(self, segment_id: int, qa_pairs: List[Dict[str, Any]]) -> List[int]:
        """保存问答对"""
        try:
            qa_ids = []
            with self.get_conn() as conn:
                cursor = conn.cursor()
                for qa in qa_pairs:
                    cursor.execute("""
                    INSERT INTO qa_pairs (segment_id, file_id, question, answer, quality_scores)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        segment_id,
                        qa["file_id"],
                        qa["question"],
                        qa["answer"],
                        json.dumps(qa["quality_scores"])
                    ))
                    qa_ids.append(cursor.lastrowid)
                conn.commit()
            return qa_ids
        except Exception as e:
            logger.error(f"保存问答对失败: {str(e)}")
            raise

    def get_file(self, file_id: int) -> Optional[Dict[str, Any]]:
        """获取文件信息"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM files WHERE id = ?", (file_id,))
                row = cursor.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "filename": row[1],
                        "file_path": row[2],
                        "file_type": row[3],
                        "file_size": row[4],
                        "created_at": row[5],
                        "updated_at": row[6]
                    }
                return None
        except Exception as e:
            logger.error(f"获取文件信息失败: {str(e)}")
            raise

    def get_text_segments(self, file_id: int) -> List[Dict[str, Any]]:
        """获取文本段落"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT id, content, segment_index, created_at
                FROM text_segments
                WHERE file_id = ?
                ORDER BY segment_index
                """, (file_id,))
                rows = cursor.fetchall()
                return [{
                    "id": row[0],
                    "content": row[1],
                    "segment_index": row[2],
                    "created_at": row[3]
                } for row in rows]
        except Exception as e:
            logger.error(f"获取文本段落失败: {str(e)}")
            raise

    def get_qa_pairs(self, segment_id: int) -> List[Dict[str, Any]]:
        """获取问答对"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT id, question, answer, quality_scores, created_at
                FROM qa_pairs
                WHERE segment_id = ?
                """, (segment_id,))
                rows = cursor.fetchall()
                return [{
                    "id": row[0],
                    "question": row[1],
                    "answer": row[2],
                    "quality_scores": json.loads(row[3]),
                    "created_at": row[4]
                } for row in rows]
        except Exception as e:
            logger.error(f"获取问答对失败: {str(e)}")
            raise

    def get_all_files(self) -> List[Dict[str, Any]]:
        """获取所有文件信息"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM files ORDER BY created_at DESC")
                rows = cursor.fetchall()
                return [{
                    "id": row[0],
                    "filename": row[1],
                    "file_path": row[2],
                    "file_type": row[3],
                    "file_size": row[4],
                    "created_at": row[5],
                    "updated_at": row[6]
                } for row in rows]
        except Exception as e:
            logger.error(f"获取所有文件信息失败: {str(e)}")
            raise

    def delete_file(self, file_id: int) -> bool:
        """删除文件及其相关数据"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                # 删除相关的问答对
                cursor.execute("""
                DELETE FROM qa_pairs
                WHERE segment_id IN (
                    SELECT id FROM text_segments WHERE file_id = ?
                )
                """, (file_id,))
                # 删除相关的文本段落
                cursor.execute("DELETE FROM text_segments WHERE file_id = ?", (file_id,))
                # 删除文件记录
                cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"删除文件失败: {str(e)}")
            raise

    def get_dataset_stats(self) -> Dict[str, Any]:
        """获取数据集统计信息"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                stats = {}
                
                # 文件统计
                cursor.execute("SELECT COUNT(*) FROM files")
                stats["total_files"] = cursor.fetchone()[0]
                
                # 文本段落统计
                cursor.execute("SELECT COUNT(*) FROM text_segments")
                stats["total_segments"] = cursor.fetchone()[0]
                
                # 问答对统计
                cursor.execute("SELECT COUNT(*) FROM qa_pairs")
                stats["total_qa_pairs"] = cursor.fetchone()[0]
                
                # 平均质量分数
                cursor.execute("""
                SELECT AVG(json_extract(quality_scores, '$.total'))
                FROM qa_pairs
                """)
                stats["average_quality_score"] = cursor.fetchone()[0] or 0
                
                return stats
        except Exception as e:
            logger.error(f"获取数据集统计信息失败: {str(e)}")
            raise

    def update_file_status(self, file_id: int, status: str) -> None:
        """更新文件状态"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE files SET status = ? WHERE id = ?",
                    (status, file_id)
                )
                conn.commit()
            logger.info(f"文件ID {file_id} 状态已更新为 {status}")
        except Exception as e:
            logger.error(f"更新文件状态失败: {str(e)}")
            raise 