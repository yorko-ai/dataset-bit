import sqlite3
import json
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import csv
import io

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
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    accuracy_score REAL,
                    completeness_score REAL,
                    relevance_score REAL,
                    clarity_score REAL,
                    total_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)

                # 创建评分历史表
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS score_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    qa_id INTEGER NOT NULL,
                    accuracy_score REAL,
                    completeness_score REAL,
                    relevance_score REAL,
                    clarity_score REAL,
                    total_score REAL,
                    feedback TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (qa_id) REFERENCES qa_pairs (id)
                )
                """)

                # 创建保存的筛选条件表
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS saved_filters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    filter_conditions TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    def save_qa_pairs(self, qa_pairs: List[Dict[str, Any]]) -> List[int]:
        """保存问答对"""
        try:
            qa_ids = []
            with self.get_conn() as conn:
                cursor = conn.cursor()
                for qa in qa_pairs:
                    cursor.execute("""
                    INSERT INTO qa_pairs (
                        question, answer,
                        accuracy_score, completeness_score,
                        relevance_score, clarity_score, total_score
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        qa["question"],
                        qa["answer"],
                        qa.get("accuracy_score", 0),
                        qa.get("completeness_score", 0),
                        qa.get("relevance_score", 0),
                        qa.get("clarity_score", 0),
                        qa.get("total_score", 0)
                    ))
                    qa_ids.append(cursor.lastrowid)
                conn.commit()
            return qa_ids
        except Exception as e:
            logger.error(f"保存问答对失败: {str(e)}")
            raise

    def update_qa_scores(self, qa_id: int, scores: Dict[str, float]) -> None:
        """更新问答对评分"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE qa_pairs
                SET accuracy_score = ?,
                    completeness_score = ?,
                    relevance_score = ?,
                    clarity_score = ?,
                    total_score = ?,
                    updated_at = ?
                WHERE id = ?
                """, (
                    scores.get("accuracy", 0),
                    scores.get("completeness", 0),
                    scores.get("relevance", 0),
                    scores.get("clarity", 0),
                    scores.get("total", 0),
                    datetime.now(),
                    qa_id
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"更新问答对评分失败: {str(e)}")
            raise

    def get_qa_scores(self, qa_id: int) -> Dict[str, float]:
        """获取问答对评分"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT accuracy_score, completeness_score,
                       relevance_score, clarity_score, total_score
                FROM qa_pairs
                WHERE id = ?
                """, (qa_id,))
                row = cursor.fetchone()
                if row:
                    return {
                        "accuracy": row[0],
                        "completeness": row[1],
                        "relevance": row[2],
                        "clarity": row[3],
                        "total": row[4]
                    }
                return {}
        except Exception as e:
            logger.error(f"获取问答对评分失败: {str(e)}")
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

    def get_qa_pairs(self) -> List[Dict[str, Any]]:
        """获取所有问答对"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM qa_pairs ORDER BY created_at DESC")
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取问答对失败: {str(e)}")
            raise

    def get_qa_pair(self, qa_id: int) -> Optional[Dict[str, Any]]:
        """获取单个问答对"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM qa_pairs WHERE id = ?", (qa_id,))
                columns = [description[0] for description in cursor.description]
                row = cursor.fetchone()
                return dict(zip(columns, row)) if row else None
        except Exception as e:
            logger.error(f"获取问答对失败: {str(e)}")
            raise

    def get_score_history(self, qa_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """获取评分历史记录"""
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT id,
                       accuracy_score,
                       completeness_score,
                       relevance_score,
                       clarity_score,
                       total_score,
                       feedback,
                       created_at
                FROM score_history
                WHERE qa_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """, (qa_id, limit))
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取评分历史记录失败: {str(e)}")
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

    def export_qa_pairs(self, 
                       min_total_score: float = None,
                       max_total_score: float = None,
                       min_accuracy_score: float = None,
                       min_completeness_score: float = None,
                       min_relevance_score: float = None,
                       min_clarity_score: float = None,
                       start_date: str = None,
                       end_date: str = None,
                       format: str = 'csv') -> bytes:
        """导出问答对数据
        
        Args:
            min_total_score: 最小总分
            max_total_score: 最大总分
            min_accuracy_score: 最小准确性分数
            min_completeness_score: 最小完整性分数
            min_relevance_score: 最小相关性分数
            min_clarity_score: 最小清晰度分数
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            format: 导出格式 ('csv' 或 'json')
            
        Returns:
            bytes: 导出的数据
        """
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                
                # 构建查询条件
                conditions = []
                params = []
                
                if min_total_score is not None:
                    conditions.append("total_score >= ?")
                    params.append(min_total_score)
                if max_total_score is not None:
                    conditions.append("total_score <= ?")
                    params.append(max_total_score)
                if min_accuracy_score is not None:
                    conditions.append("accuracy_score >= ?")
                    params.append(min_accuracy_score)
                if min_completeness_score is not None:
                    conditions.append("completeness_score >= ?")
                    params.append(min_completeness_score)
                if min_relevance_score is not None:
                    conditions.append("relevance_score >= ?")
                    params.append(min_relevance_score)
                if min_clarity_score is not None:
                    conditions.append("clarity_score >= ?")
                    params.append(min_clarity_score)
                if start_date:
                    conditions.append("created_at >= ?")
                    params.append(f"{start_date} 00:00:00")
                if end_date:
                    conditions.append("created_at <= ?")
                    params.append(f"{end_date} 23:59:59")
                
                # 构建SQL查询
                query = """
                SELECT id, question, answer, created_at
                FROM qa_pairs
                """
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                query += " ORDER BY created_at DESC"
                
                # 执行查询
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # 准备导出数据
                data = []
                for row in rows:
                    data.append({
                        'id': row[0],
                        'question': row[1],
                        'answer': row[2],
                        'created_at': row[3]
                    })
                
                # 根据格式导出
                if format == 'csv':
                    output = io.StringIO()
                    writer = csv.DictWriter(output, fieldnames=['id', 'question', 'answer', 'created_at'])
                    writer.writeheader()
                    writer.writerows(data)
                    return output.getvalue().encode('utf-8-sig')
                else:  # json
                    return json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
                    
        except Exception as e:
            logger.error(f"导出问答对失败: {str(e)}")
            raise

    def get_all_score_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取所有问答对的评分历史记录
        
        Args:
            limit: 返回记录的最大数量
            
        Returns:
            List[Dict[str, Any]]: 评分历史记录列表
        """
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT id,
                       qa_id,
                       accuracy_score,
                       completeness_score,
                       relevance_score,
                       clarity_score,
                       total_score,
                       feedback,
                       created_at
                FROM score_history
                ORDER BY created_at DESC
                LIMIT ?
                """, (limit,))
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取所有评分历史记录失败: {str(e)}")
            raise

    def get_filtered_qa_pairs(self,
                             min_total_score: float = None,
                             max_total_score: float = None,
                             min_accuracy_score: float = None,
                             min_completeness_score: float = None,
                             min_relevance_score: float = None,
                             min_clarity_score: float = None,
                             start_date: str = None,
                             end_date: str = None,
                             keyword: str = None,
                             filter_id: int = None) -> List[Dict[str, Any]]:
        """获取筛选后的问答对列表
        
        Args:
            min_total_score: 最小总分
            max_total_score: 最大总分
            min_accuracy_score: 最小准确性分数
            min_completeness_score: 最小完整性分数
            min_relevance_score: 最小相关性分数
            min_clarity_score: 最小清晰度分数
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            keyword: 关键词搜索
            filter_id: 保存的筛选条件ID
            
        Returns:
            List[Dict[str, Any]]: 筛选后的问答对列表
        """
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                
                # 如果提供了筛选条件ID，从数据库加载保存的条件
                if filter_id:
                    cursor.execute("""
                    SELECT filter_conditions
                    FROM saved_filters
                    WHERE id = ?
                    """, (filter_id,))
                    row = cursor.fetchone()
                    if row:
                        conditions = json.loads(row[0])
                        min_total_score = conditions.get('min_total_score')
                        max_total_score = conditions.get('max_total_score')
                        min_accuracy_score = conditions.get('min_accuracy_score')
                        min_completeness_score = conditions.get('min_completeness_score')
                        min_relevance_score = conditions.get('min_relevance_score')
                        min_clarity_score = conditions.get('min_clarity_score')
                        start_date = conditions.get('start_date')
                        end_date = conditions.get('end_date')
                        keyword = conditions.get('keyword')
                
                # 构建查询条件
                conditions = []
                params = []
                
                if min_total_score is not None:
                    conditions.append("total_score >= ?")
                    params.append(min_total_score)
                if max_total_score is not None:
                    conditions.append("total_score <= ?")
                    params.append(max_total_score)
                if min_accuracy_score is not None:
                    conditions.append("accuracy_score >= ?")
                    params.append(min_accuracy_score)
                if min_completeness_score is not None:
                    conditions.append("completeness_score >= ?")
                    params.append(min_completeness_score)
                if min_relevance_score is not None:
                    conditions.append("relevance_score >= ?")
                    params.append(min_relevance_score)
                if min_clarity_score is not None:
                    conditions.append("clarity_score >= ?")
                    params.append(min_clarity_score)
                if start_date:
                    conditions.append("created_at >= ?")
                    params.append(f"{start_date} 00:00:00")
                if end_date:
                    conditions.append("created_at <= ?")
                    params.append(f"{end_date} 23:59:59")
                if keyword:
                    conditions.append("(question LIKE ? OR answer LIKE ?)")
                    params.extend([f"%{keyword}%", f"%{keyword}%"])
                
                # 构建SQL查询
                query = """
                SELECT id, question, answer, created_at,
                       accuracy_score, completeness_score,
                       relevance_score, clarity_score, total_score
                FROM qa_pairs
                """
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                query += " ORDER BY created_at DESC"
                
                # 执行查询
                cursor.execute(query, params)
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"获取筛选后的问答对失败: {str(e)}")
            raise

    def save_filter(self, name: str, conditions: Dict[str, Any]) -> int:
        """保存筛选条件
        
        Args:
            name: 筛选条件名称
            conditions: 筛选条件字典
            
        Returns:
            int: 保存的筛选条件ID
        """
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO saved_filters (name, filter_conditions)
                VALUES (?, ?)
                """, (name, json.dumps(conditions)))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"保存筛选条件失败: {str(e)}")
            raise

    def get_saved_filters(self) -> List[Dict[str, Any]]:
        """获取所有保存的筛选条件
        
        Returns:
            List[Dict[str, Any]]: 保存的筛选条件列表
        """
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT id, name, filter_conditions, created_at
                FROM saved_filters
                ORDER BY created_at DESC
                """)
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取保存的筛选条件失败: {str(e)}")
            raise

    def delete_filter(self, filter_id: int) -> bool:
        """删除保存的筛选条件
        
        Args:
            filter_id: 筛选条件ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM saved_filters WHERE id = ?", (filter_id,))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"删除筛选条件失败: {str(e)}")
            raise 