from fastapi import APIRouter
from typing import List
import os

router = APIRouter()

def get_kes_codes_from_file():
    # Construct the path to the file relative to this file's location
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, 'parser', 'data', 'all_kes.txt')
    
    codes = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    codes.append(line)
    except FileNotFoundError:
        return ["File not found"]
    return codes

def get_kes_themes_from_file():
    # Construct the path to the file relative to this file's location
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, 'parser', 'data', 'all_themes.txt')
    
    themes = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    themes.append(line)
    except FileNotFoundError:
        return ["File not found"]
    return themes

@router.get("/kes-codes/", response_model=List[str])
def get_kes_codes():
    """
    Получить список всех кодов КЭС.
    """
    return get_kes_codes_from_file()

@router.get("/themes-codes/", response_model=List[str])
def get_themes_codes():
    """
    Получить список всех кодов КЭС.
    """
    return get_kes_themes_from_file()
