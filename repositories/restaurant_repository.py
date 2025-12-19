"""
매장 리포지토리 모듈
매장 데이터 접근 로직을 담당합니다.
"""
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from utils.data_loader import (
    load_restaurants_data,
    save_restaurants_data,
    validate_restaurant_data,
    add_restaurant,
    get_restaurant_by_name
)
from utils.logger import get_logger
from utils.constants import DEFAULT_DATA_PATH

logger = get_logger('restaurant_app.repositories.restaurant')


class IDataRepository(ABC):
    """
    데이터 리포지토리 인터페이스
    
    데이터 소스 추상화를 위한 인터페이스입니다.
    향후 데이터베이스 전환 시에도 동일한 인터페이스를 사용할 수 있습니다.
    """
    
    @abstractmethod
    def load_all(self) -> List[Dict[str, Any]]:
        """모든 데이터를 로드합니다."""
        pass
    
    @abstractmethod
    def save_all(self, data: List[Dict[str, Any]]) -> bool:
        """모든 데이터를 저장합니다."""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """이름으로 데이터를 검색합니다."""
        pass
    
    @abstractmethod
    def add(self, item: Dict[str, Any], allow_duplicate: bool = True) -> bool:
        """새로운 항목을 추가합니다."""
        pass


class RestaurantRepository(IDataRepository):
    """
    매장 데이터 리포지토리 클래스
    
    Repository 패턴을 적용하여 데이터 접근 로직을 캡슐화합니다.
    파일 시스템 기반 구현이지만, 인터페이스를 통해 향후 데이터베이스로 전환 가능합니다.
    """
    
    def __init__(self, file_path: str = DEFAULT_DATA_PATH):
        """
        리포지토리 초기화
        
        Args:
            file_path: 데이터 파일 경로
        """
        self._file_path = file_path
        logger.debug(f"RestaurantRepository 초기화: {file_path}")
    
    def load_all(self) -> List[Dict[str, Any]]:
        """
        모든 매장 데이터를 로드합니다.
        
        Returns:
            매장 데이터 리스트
        """
        logger.debug(f"데이터 로드 시작: {self._file_path}")
        data = load_restaurants_data(self._file_path)
        logger.info(f"데이터 로드 완료: {len(data)}개 매장")
        return data
    
    def save_all(self, data: List[Dict[str, Any]]) -> bool:
        """
        모든 매장 데이터를 저장합니다.
        
        Args:
            data: 저장할 매장 데이터 리스트
            
        Returns:
            저장 성공 여부
        """
        logger.debug(f"데이터 저장 시작: {self._file_path} ({len(data)}개 매장)")
        success = save_restaurants_data(data, self._file_path)
        if success:
            logger.info(f"데이터 저장 완료: {self._file_path}")
        else:
            logger.error(f"데이터 저장 실패: {self._file_path}")
        return success
    
    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        이름으로 매장을 검색합니다.
        
        Args:
            name: 검색할 매장 이름
            
        Returns:
            매장 데이터 또는 None (매장을 찾지 못한 경우)
        """
        data = self.load_all()
        result = get_restaurant_by_name(data, name)
        if result:
            logger.debug(f"매장 검색 성공: {name}")
        else:
            logger.debug(f"매장 검색 실패: {name}")
        return result
    
    def add(self, item: Dict[str, Any], allow_duplicate: bool = True) -> bool:
        """
        새로운 매장을 추가합니다.
        
        Args:
            item: 추가할 매장 데이터
            allow_duplicate: 중복 매장명 허용 여부 (기본값: True)
            
        Returns:
            추가 성공 여부
        """
        data = self.load_all()
        success = add_restaurant(data, item, allow_duplicate)
        if success:
            # 저장은 호출자가 결정하도록 함 (트랜잭션 관리)
            logger.debug(f"매장 추가 성공: {item.get('name', 'Unknown')}")
        else:
            logger.warning(f"매장 추가 실패: {item.get('name', 'Unknown')}")
        return success
    
    def validate(self, item: Dict[str, Any]) -> bool:
        """
        매장 데이터의 유효성을 검사합니다.
        
        Args:
            item: 검사할 매장 데이터
            
        Returns:
            유효성 여부
        """
        return validate_restaurant_data(item)

