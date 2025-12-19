"""
매장 서비스 모듈
매장 데이터 관련 비즈니스 로직을 담당합니다.
"""
from typing import List, Dict, Any
from utils.cache import get_cache
from utils.logger import get_logger

logger = get_logger('restaurant_app.services.restaurant')


class RestaurantService:
    """
    매장 데이터 관리 서비스 클래스
    
    단일 책임: 매장 데이터 관련 비즈니스 로직만 담당
    """
    
    def __init__(self):
        """서비스 초기화"""
        self._cache = get_cache()
    
    def get_all_restaurants(self) -> List[Dict[str, Any]]:
        """
        모든 매장 데이터를 반환합니다.
        
        Returns:
            매장 데이터 리스트
        """
        restaurants = self._cache.get_data()
        logger.debug(f"매장 데이터 조회: {len(restaurants)}개")
        return restaurants
    
    def get_restaurants_count(self) -> int:
        """
        매장 수를 반환합니다.
        
        Returns:
            매장 수
        """
        return self._cache.get_count()

