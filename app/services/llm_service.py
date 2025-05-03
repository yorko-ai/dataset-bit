import os
from typing import List, Dict, Any
import openai
import logging
from dotenv import load_dotenv
import json

# 加载环境变量
load_dotenv()

# 配置OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, api_key=None):
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 2000
        self.temperature = 0.7
        if api_key:
            openai.api_key = api_key

    def generate_questions(self, text: str, question_types: List[str] = None,
                         difficulty: str = "medium", questions_per_segment: int = 3) -> List[str]:
        """生成问题"""
        try:
            if question_types is None:
                question_types = ["factual", "analytical", "inferential"]

            # 构建提示
            prompt = f"""基于以下文本生成{questions_per_segment}个问题。要求：
1. 问题类型：{', '.join(question_types)}
2. 难度级别：{difficulty}
3. 问题应该多样化，覆盖文本的主要内容
4. 每个问题应该是完整的句子，以问号结尾

文本内容：
{text}

请直接返回问题列表，每个问题占一行。"""

            # 调用API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的问题生成助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            # 处理响应
            questions = response.choices[0].message.content.strip().split('\n')
            questions = [q.strip() for q in questions if q.strip()]

            return questions[:questions_per_segment]
        except Exception as e:
            logger.error(f"问题生成失败: {str(e)}")
            raise

    def generate_answer(self, question: str, context: str,
                       answer_style: str = "professional") -> str:
        """生成答案"""
        try:
            # 构建提示
            prompt = f"""基于以下文本回答问题。要求：
1. 答案风格：{answer_style}
2. 答案应该准确、完整、清晰
3. 如果文本中没有相关信息，请明确说明

问题：{question}

文本内容：
{context}"""

            # 调用API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的问答助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"答案生成失败: {str(e)}")
            raise

    def evaluate_quality(self, question: str, answer: str, context: str) -> Dict[str, float]:
        """评估问答对的质量"""
        try:
            # 构建提示
            prompt = f"""评估以下问答对的质量。请从以下维度评分（0-1分）：
1. 准确性：答案是否准确反映了文本内容
2. 完整性：答案是否完整覆盖了问题要点
3. 相关性：答案是否与问题高度相关
4. 清晰度：答案是否表达清晰、易于理解

问题：{question}
答案：{answer}
文本内容：{context}

请直接返回JSON格式的评分结果。"""

            # 调用API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的质量评估助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            # 解析响应
            scores = json.loads(response.choices[0].message.content.strip())
            
            # 计算总分
            total_score = sum(scores.values()) / len(scores)
            scores["total"] = total_score

            return scores
        except Exception as e:
            logger.error(f"质量评估失败: {str(e)}")
            raise

    def generate_qa_pairs(self, text: str, question_types: List[str] = None,
                         difficulty: str = "medium", questions_per_segment: int = 3,
                         answer_style: str = "professional") -> List[Dict[str, Any]]:
        """生成问答对"""
        try:
            # 生成问题
            questions = self.generate_questions(
                text,
                question_types=question_types,
                difficulty=difficulty,
                questions_per_segment=questions_per_segment
            )

            # 生成答案并评估质量
            qa_pairs = []
            for question in questions:
                answer = self.generate_answer(question, text, answer_style)
                quality_scores = self.evaluate_quality(question, answer, text)
                
                qa_pairs.append({
                    "question": question,
                    "answer": answer,
                    "quality_scores": quality_scores
                })

            return qa_pairs
        except Exception as e:
            logger.error(f"问答对生成失败: {str(e)}")
            raise

    def format_dataset(self, qa_pairs: List[Dict[str, Any]], format: str = "alpaca") -> str:
        """格式化数据集为指定格式"""
        try:
            if format == "alpaca":
                formatted_data = []
                for qa in qa_pairs:
                    formatted_data.append({
                        "instruction": qa["question"],
                        "input": "",
                        "output": qa["answer"],
                        "metadata": {
                            "source_file": qa.get("source_file", ""),
                            "quality_scores": qa.get("quality_scores", {})
                        }
                    })
                return json.dumps(formatted_data, ensure_ascii=False, indent=2)
            
            elif format == "sharegpt":
                formatted_data = []
                for qa in qa_pairs:
                    formatted_data.append({
                        "conversations": [
                            {"from": "human", "value": qa["question"]},
                            {"from": "assistant", "value": qa["answer"]}
                        ],
                        "metadata": {
                            "source_file": qa.get("source_file", ""),
                            "quality_scores": qa.get("quality_scores", {})
                        }
                    })
                return json.dumps(formatted_data, ensure_ascii=False, indent=2)
            
            else:
                formatted_data = []
                for qa in qa_pairs:
                    formatted_data.append({
                        "question": qa["question"],
                        "answer": qa["answer"],
                        "source_file": qa.get("source_file", ""),
                        "quality_scores": qa.get("quality_scores", {})
                    })
                return json.dumps(formatted_data, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"格式化数据集失败: {str(e)}")
            raise 