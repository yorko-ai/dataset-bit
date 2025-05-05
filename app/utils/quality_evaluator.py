import logging
from typing import Dict, List, Any
import json

logger = logging.getLogger(__name__)

class QualityEvaluator:
    def __init__(self, llm_service):
        self.llm_service = llm_service

    async def evaluate_qa_pair(self, question: str, answer: str, context: str = None) -> Dict[str, float]:
        """评估单个问答对的质量"""
        try:
            # 构建评分提示
            prompt = f"""请评估以下问答对的质量，从以下维度进行评分（0-1分）：

1. 准确性（accuracy）：答案是否准确反映了文本内容
2. 完整性（completeness）：答案是否完整覆盖了问题要点
3. 相关性（relevance）：答案是否与问题高度相关
4. 清晰度（clarity）：答案是否表达清晰、易于理解

问题：{question}
答案：{answer}
文本内容：{context if context else "无"}

请直接返回JSON格式的评分结果，格式如下：
{{
    "accuracy": 0.9,
    "completeness": 0.8,
    "relevance": 0.95,
    "clarity": 0.85
}}"""

            # 调用LLM服务获取评分
            response = await self.llm_service.generate_response(prompt)
            scores = json.loads(response)
            
            # 计算总分
            total_score = sum(scores.values()) / len(scores)
            scores["total"] = total_score

            return scores
        except Exception as e:
            logger.error(f"评估问答对质量失败: {str(e)}")
            raise

    async def evaluate_dataset(self, qa_pairs: List[Dict[str, str]], context: str = None) -> Dict[str, Any]:
        """评估整个数据集的质量"""
        try:
            total_scores = {
                "accuracy": 0,
                "completeness": 0,
                "relevance": 0,
                "clarity": 0,
                "total": 0
            }
            
            for qa in qa_pairs:
                scores = await self.evaluate_qa_pair(qa["question"], qa["answer"], context)
                for key in total_scores:
                    total_scores[key] += scores[key]
            
            # 计算平均分
            count = len(qa_pairs)
            for key in total_scores:
                total_scores[key] /= count
            
            return total_scores
        except Exception as e:
            logger.error(f"评估数据集质量失败: {str(e)}")
            raise

    def get_quality_report(self, metrics: Dict[str, float]) -> str:
        """生成质量评估报告"""
        report = f"""数据集质量评估报告：

1. 准确性：{metrics['accuracy']:.2f}
2. 完整性：{metrics['completeness']:.2f}
3. 相关性：{metrics['relevance']:.2f}
4. 清晰度：{metrics['clarity']:.2f}
5. 总分：{metrics['total']:.2f}

评估说明：
- 所有分数范围：0-1分
- 分数越高表示质量越好
- 总分是所有维度的平均值"""
        
        return report 