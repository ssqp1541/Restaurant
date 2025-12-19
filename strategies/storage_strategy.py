"""
저장 전략 모듈
저장 로직을 전략 패턴으로 구현합니다.
"""
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from utils.data_loader import load_restaurants_data, save_restaurants_data
from utils.logger import get_logger
from utils.constants import DEFAULT_DATA_PATH

logger = get_logger('restaurant_app.strategies.storage')


class IStorageStrategy(ABC):
    """
    저장 전략 인터페이스
    
    Strategy 패턴을 적용하여 다양한 저장 로직을 유연하게 교체할 수 있습니다.
    """
    
    @abstractmethod
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        """
        데이터를 로드합니다.
        
        Args:
            file_path: 파일 경로
            
        Returns:
            데이터 리스트
        """
        pass
    
    @abstractmethod
    def save(self, data: List[Dict[str, Any]], file_path: str) -> bool:
        """
        데이터를 저장합니다.
        
        Args:
            data: 저장할 데이터 리스트
            file_path: 파일 경로
            
        Returns:
            저장 성공 여부
        """
        pass


class FileStorageStrategy(IStorageStrategy):
    """
    파일 시스템 저장 전략 클래스
    
    JSON 파일 기반 저장 로직을 구현합니다.
    """
    
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        """
        JSON 파일에서 데이터를 로드합니다.
        
        Args:
            file_path: JSON 파일 경로
            
        Returns:
            데이터 리스트
        """
        return load_restaurants_data(file_path)
    
    def save(self, data: List[Dict[str, Any]], file_path: str) -> bool:
        """
        데이터를 JSON 파일에 저장합니다.
        
        Args:
            data: 저장할 데이터 리스트
            file_path: JSON 파일 경로
            
        Returns:
            저장 성공 여부
        """
        return save_restaurants_data(data, file_path)

