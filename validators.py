"""Общие валидаторы для проекта"""

import re
from django.core.exceptions import ValidationError

def validate_github_url(value):
    """Проверяет, что URL является корректной ссылкой на GitHub."""
    if not value:
        return value
    
    # Регулярное выражение для точной проверки GitHub URL
    github_pattern = re.compile(
        r'^(https?://)?(www\.)?github\.com/[\w.-]+/?',
        re.IGNORECASE
    )
    
    if not github_pattern.match(value.strip()):
        raise ValidationError('Введите корректный URL GitHub (например: https://github.com/username)')
    
    return value
