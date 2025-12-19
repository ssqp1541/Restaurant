"""
캐시 관리 모듈
매장 데이터 캐싱을 담당하는 클래스입니다.
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
from utils.data_loader import load_restaurants_data
from utils.logger import get_logger
from utils.constants import DEFAULT_DATA_PATH

logger = get_logger('restaurant_app.cache')


class RestaurantCache:
    """
    매장 데이터 캐시 관리 클래스
    
    싱글톤 패턴을 사용하여 전역 상태를 관리합니다.
    """
    _instance: Optional['RestaurantCache'] = None
    _cache: List[Dict[str, Any]] = []
    _file_path: str = DEFAULT_DATA_PATH
    
    def __new__(cls) -> 'RestaurantCache':
        """싱글톤 패턴 구현"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """캐시 초기화"""
        if not self._cache:
            self._load_cache()
    
    def _load_cache(self) -> None:
        """캐시 데이터 로드"""
        self._cache = load_restaurants_data(self._file_path)
        logger.debug(f"캐시 로드 완료: {len(self._cache)}개 매장")
    
    def get_data(self) -> List[Dict[str, Any]]:
        """
        캐시된 데이터를 반환합니다.
        
        Returns:
            매장 데이터 리스트
        """
        if not self._cache:
            self._load_cache()
        return self._cache
    
    def clear_cache(self) -> None:
        """캐시를 초기화합니다."""
        self._cache = []
        logger.debug("캐시 초기화 완료")
    
    def reload_cache(self) -> None:
        """캐시를 다시 로드합니다."""
        self.clear_cache()
        self._load_cache()
    
    def set_file_path(self, file_path: str) -> None:
        """
        데이터 파일 경로를 설정합니다.
        
        Args:
            file_path: 데이터 파일 경로
        """
        self._file_path = file_path
        self.reload_cache()
    
    def get_count(self) -> int:
        """
        캐시된 매장 수를 반환합니다.
        
        Returns:
            매장 수
        """
        return len(self.get_data())


# 싱글톤 인스턴스 생성 함수
def get_cache() -> RestaurantCache:
    """
    RestaurantCache 싱글톤 인스턴스를 반환합니다.
    
    Returns:
        RestaurantCache 인스턴스
    """
    return RestaurantCache()

