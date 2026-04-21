"""
Модели данных для заданий ФИПИ
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from enum import Enum
import json


class TaskType(Enum):
    """Типы заданий"""
    SHORT_ANSWER = "short_answer"
    MULTIPLE_CHOICE = "multiple_choice"
    MATCHING = "matching"


class CheckResult(Enum):
    """Результаты проверки"""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIALLY_CORRECT = "partially_correct"
    ERROR = "error"


@dataclass
class AnswerVariant:
    """Вариант ответа для задания с выбором"""
    index: int
    text: str
    input_name: str  # Например: test0, test1


@dataclass
class MatchingOption:
    """Опция для задания на соответствие"""
    letter: str  # A, Б и т.д.
    text: str
    select_name: str  # ans0, ans1


@dataclass
class MatchingChoice:
    """Вариант выбора для соответствия"""
    number: str  # 1, 2, 3 и т.д.
    text: str


@dataclass
class Task:
    """Модель задания"""
    guid: str
    task_id: str  # Публичный номер (например, 0FDA4F)
    subject: str
    task_type: TaskType
    question_text: str
    question_html: str
    
    # Для заданий с вариантами ответов
    answer_variants: Optional[List[AnswerVariant]] = None
    
    # Для заданий на соответствие
    matching_options: Optional[List[MatchingOption]] = None
    matching_choices: Optional[List[MatchingChoice]] = None
    
    # Для краткого ответа
    answer_unit: Optional[str] = None  # Единица измерения
    
    # Медиафайлы
    images: List[str] = field(default_factory=list)
    
    # КЭС (Кодификатор элементов содержания)
    kes_codes: List[str] = field(default_factory=list)
    
    # Метаданные
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Конвертация в словарь"""
        data = asdict(self)
        data['task_type'] = self.task_type.value
        return data
    
    def to_json(self, indent: int = 2) -> str:
        """Конвертация в JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Создание из словаря"""
        data = data.copy()
        data['task_type'] = TaskType(data['task_type'])
        
        if data.get('answer_variants'):
            data['answer_variants'] = [
                AnswerVariant(**v) for v in data['answer_variants']
            ]
        
        if data.get('matching_options'):
            data['matching_options'] = [
                MatchingOption(**o) for o in data['matching_options']
            ]
        
        if data.get('matching_choices'):
            data['matching_choices'] = [
                MatchingChoice(**c) for c in data['matching_choices']
            ]
        
        return cls(**data)


@dataclass
class CheckResponse:
    """Результат проверки задания"""
    guid: str
    result: CheckResult
    user_answer: str
    
    def to_dict(self) -> dict:
        return {
            'guid': self.guid,
            'result': self.result.value,
            'user_answer': self.user_answer
        }

