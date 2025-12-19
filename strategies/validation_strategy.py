"""
검증 전략 모듈
검증 로직을 전략 패턴으로 구현합니다.
"""
from typing import Dict, Any, Tuple, Optional
from abc import ABC, abstractmethod
from utils.data_loader import validate_restaurant_data, validate_restaurant_data_with_error
from utils.logger import get_logger

logger = get_logger('restaurant_app.strategies.validation')


class IValidationStrategy(ABC):
    """
    검증 전략 인터페이스
    
    Strategy 패턴을 적용하여 다양한 검증 로직을 유연하게 교체할 수 있습니다.
    """
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        데이터의 유효성을 검사합니다.
        
        Args:
            data: 검사할 데이터
            
        Returns:
            유효성 여부
        """
        pass
    
    @abstractmethod
    def validate_with_error(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        데이터의 유효성을 검사하고 에러 메시지를 반환합니다.
        
        Args:
            data: 검사할 데이터
            
        Returns:
            (유효성 여부, 에러 메시지) 튜플
        """
        pass


class RestaurantValidationStrategy(IValidationStrategy):
    """
    매장 데이터 검증 전략 클래스
    
    기본 검증 로직을 구현합니다.
    """
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        매장 데이터의 유효성을 검사합니다.
        
        Args:
            data: 검사할 매장 데이터
            
        Returns:
            유효성 여부
        """
        return validate_restaurant_data(data)
    
    def validate_with_error(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        매장 데이터의 유효성을 검사하고 에러 메시지를 반환합니다.
        
        Args:
            data: 검사할 매장 데이터
            
        Returns:
            (유효성 여부, 에러 메시지) 튜플
        """
        return validate_restaurant_data_with_error(data)

