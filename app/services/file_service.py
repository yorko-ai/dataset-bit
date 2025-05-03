import os
from docx import Document
import PyPDF2
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class FileService:
    def __init__(self, upload_folder: str = "uploads"):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)

    def save_file(self, file) -> Dict[str, Any]:
        """保存上传的文件"""
        try:
            # 检查文件类型
            file_ext = os.path.splitext(file.filename)[1].lower()
            if file_ext not in ['.txt', '.md', '.docx', '.pdf']:
                raise ValueError("不支持的文件类型")

            # 生成安全的文件名
            safe_filename = ''.join(c for c in file.filename if c.isalnum() or c in '._-')
            file_path = os.path.join(self.upload_folder, safe_filename)

            # 保存文件
            with open(file_path, "wb") as f:
                content = file.file.read()
                f.write(content)

            return {
                "filename": safe_filename,
                "filepath": file_path,
                "filetype": file_ext[1:],  # 去掉点号
                "size": len(content)
            }
        except Exception as e:
            logger.error(f"文件保存失败: {str(e)}")
            raise

    def extract_text(self, file_path: str) -> str:
        """从文件中提取文本内容"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif file_ext == '.docx':
                doc = Document(file_path)
                return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            
            elif file_ext == '.pdf':
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    return '\n'.join([page.extract_text() for page in pdf_reader.pages])
            
            else:
                raise ValueError("不支持的文件类型")
        except Exception as e:
            logger.error(f"文本提取失败: {str(e)}")
            raise

    def split_text(self, text: str, method: str = "paragraph", 
                  min_length: int = 100, max_length: int = 2000) -> List[str]:
        """分割文本内容"""
        try:
            segments = []
            
            if method == "paragraph":
                # 按段落分割
                raw_segments = text.split('\n\n')
                segments = [s.strip() for s in raw_segments if s.strip()]
            
            elif method == "heading":
                # 按标题分割
                lines = text.split('\n')
                current_segment = []
                
                for line in lines:
                    if line.strip().startswith('#'):
                        if current_segment:
                            segments.append('\n'.join(current_segment))
                            current_segment = []
                        current_segment.append(line)
                    else:
                        current_segment.append(line)
                
                if current_segment:
                    segments.append('\n'.join(current_segment))
            
            elif method == "smart":
                # 占位：用段落分割，后续可实现智能分块
                raw_segments = text.split('\n\n')
                segments = [s.strip() for s in raw_segments if s.strip()]
            else:
                raise ValueError("不支持的分割方法")

            # 过滤段落长度
            valid_segments = [
                s for s in segments 
                if min_length <= len(s) <= max_length
            ]

            return valid_segments
        except Exception as e:
            logger.error(f"文本分割失败: {str(e)}")
            raise

    def process_file(self, file_path: str, method: str = "paragraph",
                    min_length: int = 100, max_length: int = 2000) -> List[str]:
        """处理文件：提取文本并分割"""
        try:
            # 提取文本
            text = self.extract_text(file_path)
            
            # 分割文本
            segments = self.split_text(
                text,
                method=method,
                min_length=min_length,
                max_length=max_length
            )
            
            return segments
        except Exception as e:
            logger.error(f"文件处理失败: {str(e)}")
            raise

    def get_file_stats(self, file_path: str) -> Dict[str, Any]:
        """获取文件统计信息"""
        try:
            text = self.extract_text(file_path)
            
            # 计算基本统计信息
            stats = {
                "total_chars": len(text),
                "total_words": len(text.split()),
                "total_lines": len(text.splitlines()),
                "total_paragraphs": len(text.split('\n\n')),
            }
            
            # 计算平均段落长度
            paragraphs = [p for p in text.split('\n\n') if p.strip()]
            if paragraphs:
                stats["avg_paragraph_length"] = sum(len(p) for p in paragraphs) / len(paragraphs)
            else:
                stats["avg_paragraph_length"] = 0
            
            return stats
        except Exception as e:
            logger.error(f"获取文件统计信息失败: {str(e)}")
            raise 