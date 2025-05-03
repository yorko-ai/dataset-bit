from pydantic import BaseModel

class SplitSettings(BaseModel):
    method: str = "paragraph"
    min_length: int = 100
    max_length: int = 2000

class QASettings(BaseModel):
    question_types: list = []
    difficulty: str = "medium"
    questions_per_segment: int = 1
    answer_style: str = "concise"

class ExportSettings(BaseModel):
    format: str = "alpaca"
    include_metadata: bool = True 