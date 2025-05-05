"""多语言翻译支持"""

# 中文翻译
ZH_TRANSLATIONS = {
    # 页面标题
    'page_title': '问答对评分系统',
    
    # 按钮文本
    'evaluate': '评估',
    'batch_evaluate': '批量评估',
    'edit': '编辑',
    'delete': '删除',
    
    # 主题
    'theme_light': '浅色主题',
    'theme_dark': '深色主题',
    
    # 评分维度
    'accuracy': '准确性',
    'completeness': '完整性',
    'relevance': '相关性',
    'clarity': '清晰度',
    'total': '总分',
    
    # 消息提示
    'evaluate_success': '评估成功',
    'batch_evaluate_success': '批量评估成功',
    'qa_not_found': '未找到问答对',
    'scores_not_found': '未找到评分数据',
    'evaluate_failed': '评估失败',
    'load_failed': '加载失败',
}

# 英文翻译
EN_TRANSLATIONS = {
    # Page titles
    'page_title': 'QA Pair Scoring System',
    
    # Button texts
    'evaluate': 'Evaluate',
    'batch_evaluate': 'Batch Evaluate',
    'edit': 'Edit',
    'delete': 'Delete',
    
    # Themes
    'theme_light': 'Light Theme',
    'theme_dark': 'Dark Theme',
    
    # Score dimensions
    'accuracy': 'Accuracy',
    'completeness': 'Completeness',
    'relevance': 'Relevance',
    'clarity': 'Clarity',
    'total': 'Total',
    
    # Messages
    'evaluate_success': 'Evaluation successful',
    'batch_evaluate_success': 'Batch evaluation successful',
    'qa_not_found': 'QA pair not found',
    'scores_not_found': 'Scores not found',
    'evaluate_failed': 'Evaluation failed',
    'load_failed': 'Load failed',
}

def get_translations(lang='zh'):
    """获取指定语言的翻译
    
    Args:
        lang (str): 语言代码，支持 'zh' 和 'en'
        
    Returns:
        dict: 翻译字典
    """
    if lang == 'en':
        return EN_TRANSLATIONS
    return ZH_TRANSLATIONS 