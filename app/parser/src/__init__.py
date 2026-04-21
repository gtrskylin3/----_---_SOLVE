"""
FIPI Parser & Checker
Система для парсинга и проверки заданий из Открытого банка ФИПИ
"""

__version__ = "1.0.0"

from .config import BASE_URL, SUBJECTS
from .models import Task, TaskType, CheckResult
from .parser import FIPIParser
from .checker import FIPIChecker, AnswerHelper
from .utils import save_tasks_to_json, extract_image_urls_from_html, clean_text

__all__ = [
    'BASE_URL',
    'SUBJECTS',
    'Task',
    'TaskType',
    'CheckResult',
    'FIPIParser',
    'FIPIChecker',
    'AnswerHelper',
    'save_tasks_to_json',
    'extract_image_urls_from_html',
    'clean_text',
]

