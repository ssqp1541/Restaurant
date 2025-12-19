"""
전략 패턴 모듈
검증 및 저장 전략을 담당하는 클래스들을 제공합니다.
"""

from strategies.validation_strategy import IValidationStrategy, RestaurantValidationStrategy
from strategies.storage_strategy import IStorageStrategy, FileStorageStrategy

__all__ = [
    'IValidationStrategy',
    'RestaurantValidationStrategy',
    'IStorageStrategy',
    'FileStorageStrategy',
]

