"""
메트릭 서비스 모듈
메트릭 수집 및 관리 비즈니스 로직을 담당합니다.
"""
from typing import Dict, Any
from utils.metrics import get_metrics
from utils.logger import get_logger

logger = get_logger('restaurant_app.services.metrics')


class MetricsService:
    """
    메트릭 관리 서비스 클래스
    
    단일 책임: 메트릭 수집 및 관리 비즈니스 로직만 담당
    """
    
    def __init__(self):
        """서비스 초기화"""
        self._metrics_collector = get_metrics()
    
    def increment_request(self) -> None:
        """요청 수를 증가시킵니다."""
        self._metrics_collector.increment_request()
    
    def increment_error(self) -> None:
        """에러 수를 증가시킵니다."""
        self._metrics_collector.increment_error()
    
    def add_response_time(self, elapsed_time: float) -> None:
        """
        응답 시간을 추가합니다.
        
        Args:
            elapsed_time: 응답 시간 (초)
        """
        self._metrics_collector.add_response_time(elapsed_time)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        현재 메트릭 정보를 반환합니다.
        
        Returns:
            메트릭 정보 딕셔너리
        """
        return self._metrics_collector.get_metrics()
    
    def get_health_metrics(self) -> Dict[str, Any]:
        """
        헬스 체크용 메트릭 정보를 반환합니다.
        
        Returns:
            헬스 체크 메트릭 정보 딕셔너리
        """
        return self._metrics_collector.get_health_metrics()

