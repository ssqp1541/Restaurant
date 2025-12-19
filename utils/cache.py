"""
캐시 관리 모듈
매장 데이터 캐싱을 담당하는 클래스입니다.
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
from time import time
from utils.data_loader import load_restaurants_data
from utils.logger import get_logger
from utils.constants import DEFAULT_DATA_PATH

logger = get_logger('restaurant_app.cache')


class RestaurantCache:
    """
    매장 데이터 캐시 관리 클래스
    
    싱글톤 패턴을 사용하여 전역 상태를 관리합니다.
    파일 변경 감지 및 TTL 기반 캐시 무효화를 지원합니다.
    """
    _instance: Optional['RestaurantCache'] = None
    _cache: List[Dict[str, Any]] = []
    _file_path: str = DEFAULT_DATA_PATH
    _file_mtime: Optional[float] = None  # 파일 수정 시간
    _cache_time: Optional[float] = None  # 캐시 생성 시간
    _ttl: int = 300  # TTL (초), 기본값 5분
    
    def __new__(cls) -> 'RestaurantCache':
        """싱글톤 패턴 구현"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """캐시 초기화"""
        if not self._cache:
            self._load_cache()
    
    def _get_file_mtime(self) -> Optional[float]:
        """
        파일의 수정 시간을 반환합니다.
        
        Returns:
            파일 수정 시간 (타임스탬프) 또는 None
        """
        try:
            file_path = Path(self._file_path)
            if file_path.exists():
                return file_path.stat().st_mtime
        except Exception as e:
            logger.warning(f"파일 수정 시간 확인 실패: {e}")
        return None
    
    def _is_cache_valid(self) -> bool:
        """
        캐시가 유효한지 확인합니다.
        
        Returns:
            캐시 유효성 여부
        """
        # 캐시가 없으면 무효
        if not self._cache or self._cache_time is None:
            return False
        
        # TTL 체크
        if time() - self._cache_time > self._ttl:
            logger.debug("캐시 TTL 만료")
            return False
        
        # 파일 변경 감지
        current_mtime = self._get_file_mtime()
        if current_mtime is not None and self._file_mtime is not None:
            if current_mtime > self._file_mtime:
                logger.debug("파일 변경 감지로 캐시 무효화")
                return False
        
        return True
    
    def _load_cache(self) -> None:
        """캐시 데이터 로드"""
        self._cache = load_restaurants_data(self._file_path)
        self._file_mtime = self._get_file_mtime()
        self._cache_time = time()
        logger.debug(f"캐시 로드 완료: {len(self._cache)}개 매장 (TTL: {self._ttl}초)")
    
    def get_data(self) -> List[Dict[str, Any]]:
        """
        캐시된 데이터를 반환합니다.
        
        캐시가 유효하지 않으면 자동으로 다시 로드합니다.
        
        Returns:
            매장 데이터 리스트
        """
        if not self._is_cache_valid():
            self._load_cache()
        return self._cache
    
    def set_ttl(self, ttl: int) -> None:
        """
        캐시 TTL을 설정합니다.
        
        Args:
            ttl: TTL (초)
        """
        self._ttl = ttl
        logger.debug(f"캐시 TTL 설정: {ttl}초")
    
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

