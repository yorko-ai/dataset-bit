from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import os
import logging
from datetime import datetime
import threading
import time
from uuid import uuid4

from app.services.file_service import FileService
from app.services.llm_service import LLMService
from app.services.db_service import DBService

router = APIRouter()
logger = logging.getLogger(__name__)

# 初始化服务
file_service = FileService()
llm_service = LLMService()
db_service = DBService()

PROCESS_TASKS = {}

def smart_split_task(file_id, task_id, method, min_tokens, max_tokens, overlap_rate, semantic):
    try:
        # 1. 获取文件信息
        file_info = db_service.get_file(file_id)
        if not file_info:
            PROCESS_TASKS[task_id]["status"] = "error"
            PROCESS_TASKS[task_id]["error"] = "文件不存在"
            return
        # 2. 智能分块（可用file_service.process_file或自定义算法）
        segments = file_service.process_file(
            file_info["file_path"],
            method=method,
            min_length=min_tokens,
            max_length=max_tokens
        )
        total_blocks = len(segments)
        PROCESS_TASKS[task_id]["total"] = total_blocks
        segment_ids = []
        # 3. 保存分块到数据库，并实时上报进度
        for i, seg in enumerate(segments):
            seg_id = db_service.save_text_segments(file_id, [seg])
            segment_ids.extend(seg_id)
            PROCESS_TASKS[task_id]["current"] = i + 1
            PROCESS_TASKS[task_id]["progress"] = (i + 1) / total_blocks
        # 4. 更新文件状态
        db_service.update_file_status(file_id, "已完成")
        PROCESS_TASKS[task_id]["status"] = "done"
        PROCESS_TASKS[task_id]["result"] = "分割完成"
    except Exception as e:
        PROCESS_TASKS[task_id]["status"] = "error"
        PROCESS_TASKS[task_id]["error"] = str(e)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传文件"""
    try:
        # 保存文件
        file_info = file_service.save_file(file)
        file_size = os.path.getsize(file_info["filepath"])
        file_type = os.path.splitext(file.filename)[1][1:].lower()
        
        # 保存到数据库
        file_id = db_service.save_file(
            filename=file.filename,
            file_path=file_info["filepath"],
            file_type=file_type,
            file_size=file_size
        )
        
        return {
            "status": "success",
            "message": "文件上传成功",
            "data": {
                "file_id": file_id,
                "filename": file.filename,
                "file_type": file_type,
                "file_size": file_size
            }
        }
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process/{file_id}")
async def process_file(
    file_id: int,
    method: str = "smart",
    min_tokens: int = 512,
    max_tokens: int = 1024,
    overlap_rate: float = 0.15,
    semantic: bool = True
):
    task_id = str(uuid4())
    PROCESS_TASKS[task_id] = {"status": "processing", "progress": 0, "total": 1, "current": 0, "result": None, "error": None}
    threading.Thread(target=smart_split_task, args=(file_id, task_id, method, min_tokens, max_tokens, overlap_rate, semantic)).start()
    return {"status": "success", "task_id": task_id}

@router.get("/process/progress/{task_id}")
async def get_process_progress(task_id: str):
    task = PROCESS_TASKS.get(task_id)
    if not task:
        return {"status": "not_found"}
    return {
        "status": task["status"],
        "progress": task["progress"],
        "current": task["current"],
        "total": task["total"],
        "error": task["error"]
    }

@router.get("/files")
async def get_files():
    """获取所有文件信息"""
    try:
        files = db_service.get_all_files()
        logger.info(f"数据库返回的文件信息: {files}")
        # 字段映射，保证前端字段一致
        mapped_files = []
        for f in files:
            mapped_files.append({
                "id": f["id"],
                "filename": f["filename"],
                "filetype": f.get("file_type", ""),
                "filesize": f.get("file_size", 0),
                "upload_time": f.get("created_at", ""),
                "status": f.get("status", "待处理")
            })
        return {
            "status": "success",
            "data": mapped_files
        }
    except Exception as e:
        logger.error(f"获取文件列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files/{file_id}")
async def get_file(file_id: int):
    """获取文件详细信息"""
    try:
        file_info = db_service.get_file(file_id)
        if not file_info:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        segments = db_service.get_text_segments(file_id)
        return {
            "status": "success",
            "data": {
                "file": file_info,
                "segments": segments
            }
        }
    except Exception as e:
        logger.error(f"获取文件详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/segments/{segment_id}/qa")
async def get_segment_qa(segment_id: int):
    """获取文本段落的问答对"""
    try:
        qa_pairs = db_service.get_qa_pairs(segment_id)
        return {
            "status": "success",
            "data": qa_pairs
        }
    except Exception as e:
        logger.error(f"获取问答对失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/files/{file_id}")
async def delete_file(file_id: int):
    """删除文件及其相关数据"""
    try:
        success = db_service.delete_file(file_id)
        if not success:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        return {
            "status": "success",
            "message": "文件删除成功"
        }
    except Exception as e:
        logger.error(f"删除文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_stats():
    """获取数据集统计信息"""
    try:
        stats = db_service.get_dataset_stats()
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        logger.error(f"获取统计信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export/{file_id}")
async def export_dataset(
    file_id: int,
    format: str = "alpaca"
):
    """导出数据集"""
    try:
        # 获取文件信息
        file_info = db_service.get_file(file_id)
        if not file_info:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 获取所有文本段落
        segments = db_service.get_text_segments(file_id)
        
        # 收集所有问答对
        all_qa_pairs = []
        for segment in segments:
            qa_pairs = db_service.get_qa_pairs(segment["id"])
            for qa in qa_pairs:
                qa["source_file"] = file_info["filename"]
            all_qa_pairs.extend(qa_pairs)
        
        if not all_qa_pairs:
            raise HTTPException(status_code=404, detail="没有找到问答对数据")
        
        # 格式化数据集
        formatted_data = llm_service.format_dataset(all_qa_pairs, format)
        
        # 确保导出目录存在
        export_dir = os.path.join(os.getcwd(), "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # 生成导出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_filename = f"dataset_{file_info['filename']}_{timestamp}.json"
        export_path = os.path.join(export_dir, export_filename)
        
        # 保存导出文件
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(formatted_data)
        
        return {
            "status": "success",
            "message": "数据集导出成功",
            "data": {
                "export_path": export_path,
                "total_qa_pairs": len(all_qa_pairs)
            }
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"导出数据集失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 