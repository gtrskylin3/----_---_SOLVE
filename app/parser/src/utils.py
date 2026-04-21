"""
Utilities for file and data handling.
"""
import json
import re
from typing import List
from bs4 import BeautifulSoup # Added this import
from .models import Task


def save_tasks_to_json(tasks: List[Task], file_path: str):
    """
    Saves a list of tasks to a single JSON file.

    Args:
        tasks: A list of Task objects.
        file_path: The path to the output file.
    """
    tasks_data = [task.to_dict() for task in tasks]
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=2)
    print(f"[OK] All {len(tasks)} tasks have been saved to {file_path}")


def extract_image_urls_from_html(html: str) -> List[str]:
    """
    Extracts image URLs from HTML content.
    Looks for calls to ShowPictureQ and src attributes in img tags.
    """
    urls = []
    
    # Pattern for ShowPictureQ('...')
    show_picture_pattern = r"ShowPictureQ\(['\"]([^'\"]+)['\"]\)"
    matches = re.findall(show_picture_pattern, html)
    urls.extend(matches)
    
    # Pattern for <img src="...">
    img_src_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    matches = re.findall(img_src_pattern, html)
    urls.extend(matches)
    
    return urls


def clean_text(text: str) -> str:
    """Cleans up text by removing extra whitespace and newlines."""
    # Replace multiple whitespace characters with a single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    # Replace non-breaking spaces
    text = text.replace('&nbsp;', ' ')
    return text


def remove_mathml_prefix(html_content: str) -> str:
    """
    Removes 'm:' prefix from MathML tags in the given HTML content.
    For example, changes '<m:math>' to '<math>'.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup.find_all(True):  # find_all(True) gets all tags
        if tag.name and tag.name.startswith('m:'):
            tag.name = tag.name[2:]  # Remove 'm:' prefix
    return str(soup)
