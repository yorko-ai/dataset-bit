from flask import Blueprint, jsonify, request, send_file
from app.services.db_service import DBService
from app.utils.quality_evaluator import QualityEvaluator
from app.utils.translations import get_translations
from datetime import datetime
import io

qa_bp = Blueprint('qa', __name__)
db_service = DBService()
quality_evaluator = QualityEvaluator()

@qa_bp.route('/qa-pairs', methods=['GET'])
def get_qa_pairs():
    """获取问答对列表"""
    lang = request.args.get('lang', 'zh')
    t = get_translations(lang)
    
    try:
        qa_pairs = db_service.get_qa_pairs()
        return jsonify({
            'status': 'success',
            'data': qa_pairs,
            'translations': t
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@qa_bp.route('/qa-pairs/<int:qa_id>/evaluate', methods=['POST'])
def evaluate_qa_pair(qa_id):
    """评估单个问答对"""
    lang = request.args.get('lang', 'zh')
    t = get_translations(lang)
    
    try:
        qa_pair = db_service.get_qa_pair(qa_id)
        if not qa_pair:
            return jsonify({
                'status': 'error',
                'message': t['qa_not_found']
            }), 404
            
        scores = quality_evaluator.evaluate_qa_pair(qa_pair)
        db_service.update_qa_scores(qa_id, scores)
        
        return jsonify({
            'status': 'success',
            'data': scores,
            'message': t['evaluate_success']
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@qa_bp.route('/qa-pairs/batch-evaluate', methods=['POST'])
def batch_evaluate():
    """批量评估问答对"""
    lang = request.args.get('lang', 'zh')
    t = get_translations(lang)
    
    try:
        qa_pairs = db_service.get_qa_pairs()
        results = []
        
        for qa_pair in qa_pairs:
            scores = quality_evaluator.evaluate_qa_pair(qa_pair)
            db_service.update_qa_scores(qa_pair['id'], scores)
            results.append({
                'qa_id': qa_pair['id'],
                'scores': scores
            })
            
        return jsonify({
            'status': 'success',
            'data': results,
            'message': t['batch_evaluate_success']
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@qa_bp.route('/qa-pairs/<int:qa_id>/scores', methods=['GET'])
def get_qa_scores(qa_id):
    """获取问答对评分"""
    lang = request.args.get('lang', 'zh')
    t = get_translations(lang)
    
    try:
        scores = db_service.get_qa_scores(qa_id)
        if not scores:
            return jsonify({
                'status': 'error',
                'message': t['scores_not_found']
            }), 404
            
        return jsonify({
            'status': 'success',
            'data': scores
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@qa_bp.route('/qa-pairs/<int:qa_id>/history', methods=['GET'])
def get_qa_history(qa_id):
    """获取问答对评分历史记录"""
    lang = request.args.get('lang', 'zh')
    t = get_translations(lang)
    limit = request.args.get('limit', 10, type=int)
    
    try:
        history = db_service.get_score_history(qa_id, limit)
        return jsonify({
            'status': 'success',
            'data': history
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@qa_bp.route('/qa-pairs/history', methods=['GET'])
def get_all_qa_history():
    """获取所有问答对的评分历史记录"""
    lang = request.args.get('lang', 'zh')
    t = get_translations(lang)
    limit = request.args.get('limit', 100, type=int)
    
    try:
        history = db_service.get_all_score_history(limit)
        return jsonify({
            'status': 'success',
            'data': history
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@qa_bp.route('/qa-pairs/export', methods=['GET'])
def export_qa_pairs():
    """导出问答对数据"""
    lang = request.args.get('lang', 'zh')
    t = get_translations(lang)
    
    try:
        # 获取筛选参数
        min_total_score = request.args.get('min_total_score', type=float)
        max_total_score = request.args.get('max_total_score', type=float)
        min_accuracy_score = request.args.get('min_accuracy_score', type=float)
        min_completeness_score = request.args.get('min_completeness_score', type=float)
        min_relevance_score = request.args.get('min_relevance_score', type=float)
        min_clarity_score = request.args.get('min_clarity_score', type=float)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        format = request.args.get('format', 'csv')
        
        # 验证日期格式
        if start_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': t['invalid_start_date']
                }), 400
                
        if end_date:
            try:
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': t['invalid_end_date']
                }), 400
        
        # 导出数据
        data = db_service.export_qa_pairs(
            min_total_score=min_total_score,
            max_total_score=max_total_score,
            min_accuracy_score=min_accuracy_score,
            min_completeness_score=min_completeness_score,
            min_relevance_score=min_relevance_score,
            min_clarity_score=min_clarity_score,
            start_date=start_date,
            end_date=end_date,
            format=format
        )
        
        # 准备文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'qa_pairs_{timestamp}.{format}'
        
        # 返回文件
        return send_file(
            io.BytesIO(data),
            mimetype='text/csv' if format == 'csv' else 'application/json',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@qa_bp.route('/qa-pairs/filter', methods=['GET'])
def filter_qa_pairs():
    """获取筛选后的问答对列表"""
    try:
        # 获取筛选参数
        min_total_score = request.args.get('min_total_score', type=float)
        max_total_score = request.args.get('max_total_score', type=float)
        min_accuracy_score = request.args.get('min_accuracy_score', type=float)
        min_completeness_score = request.args.get('min_completeness_score', type=float)
        min_relevance_score = request.args.get('min_relevance_score', type=float)
        min_clarity_score = request.args.get('min_clarity_score', type=float)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        keyword = request.args.get('keyword')
        filter_id = request.args.get('filter_id', type=int)
        
        # 验证日期格式
        if start_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': get_translations()['invalid_date_format']
                }), 400
                
        if end_date:
            try:
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': get_translations()['invalid_date_format']
                }), 400
        
        # 获取筛选后的问答对
        qa_pairs = db_service.get_filtered_qa_pairs(
            min_total_score=min_total_score,
            max_total_score=max_total_score,
            min_accuracy_score=min_accuracy_score,
            min_completeness_score=min_completeness_score,
            min_relevance_score=min_relevance_score,
            min_clarity_score=min_clarity_score,
            start_date=start_date,
            end_date=end_date,
            keyword=keyword,
            filter_id=filter_id
        )
        
        return jsonify({
            'success': True,
            'data': qa_pairs
        })
        
    except Exception as e:
        logger.error(f"筛选问答对失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': get_translations()['filter_failed']
        }), 500

@qa_bp.route('/filters', methods=['POST'])
def save_filter():
    """保存筛选条件"""
    try:
        data = request.get_json()
        name = data.get('name')
        conditions = data.get('conditions')
        
        if not name or not conditions:
            return jsonify({
                'success': False,
                'message': get_translations()['invalid_filter_data']
            }), 400
        
        filter_id = db_service.save_filter(name, conditions)
        
        return jsonify({
            'success': True,
            'data': {'id': filter_id}
        })
        
    except Exception as e:
        logger.error(f"保存筛选条件失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': get_translations()['save_filter_failed']
        }), 500

@qa_bp.route('/filters', methods=['GET'])
def get_saved_filters():
    """获取所有保存的筛选条件"""
    try:
        filters = db_service.get_saved_filters()
        
        return jsonify({
            'success': True,
            'data': filters
        })
        
    except Exception as e:
        logger.error(f"获取保存的筛选条件失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': get_translations()['get_filters_failed']
        }), 500

@qa_bp.route('/filters/<int:filter_id>', methods=['DELETE'])
def delete_filter(filter_id):
    """删除保存的筛选条件"""
    try:
        success = db_service.delete_filter(filter_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': get_translations()['filter_not_found']
            }), 404
        
        return jsonify({
            'success': True
        })
        
    except Exception as e:
        logger.error(f"删除筛选条件失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': get_translations()['delete_filter_failed']
        }), 500 