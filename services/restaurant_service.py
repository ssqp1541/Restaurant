"""
매장 서비스 모듈
매장 데이터 관련 비즈니스 로직을 담당합니다.
"""
from typing import List, Dict, Any, Optional
from repositories.restaurant_repository import RestaurantRepository, IDataRepository
from utils.cache import get_cache
from utils.logger import get_logger

logger = get_logger('restaurant_app.services.restaurant')


class RestaurantService:
    """
    매장 데이터 관리 서비스 클래스
    
    단일 책임: 매장 데이터 관련 비즈니스 로직만 담당
    Repository 패턴을 사용하여 데이터 접근 로직과 분리
    """
    
    def __init__(self, repository: Optional[IDataRepository] = None):
        """
        서비스 초기화
        
        Args:
            repository: 데이터 리포지토리 (의존성 주입, None이면 기본 리포지토리 사용)
        """
        self._repository = repository or RestaurantRepository()
        self._cache = get_cache()
        logger.debug("RestaurantService 초기화 완료")
    
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
    
    def get_restaurant_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        이름으로 매장을 검색합니다.
        
        Args:
            name: 검색할 매장 이름
            
        Returns:
            매장 데이터 또는 None
        """
        return self._repository.find_by_name(name)
    
    def add_restaurant(self, restaurant: Dict[str, Any], allow_duplicate: bool = True) -> bool:
        """
        새로운 매장을 추가합니다.
        
        Args:
            restaurant: 추가할 매장 데이터
            allow_duplicate: 중복 매장명 허용 여부
            
        Returns:
            추가 성공 여부
        """
        if not self._repository.validate(restaurant):
            logger.warning(f"유효하지 않은 매장 데이터: {restaurant.get('name', 'Unknown')}")
            return False
        
        success = self._repository.add(restaurant, allow_duplicate)
        if success:
            # 캐시 무효화
            self._cache.clear_cache()
            # 데이터 저장
            data = self._repository.load_all()
            self._repository.save_all(data)
        
        return success

