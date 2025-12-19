"""
메트릭 수집 모듈
애플리케이션 메트릭을 수집하고 관리하는 클래스입니다.
"""
from typing import Dict, Any, List, Optional
from time import time
from utils.logger import get_logger
from utils.constants import MAX_RESPONSE_TIMES

logger = get_logger('restaurant_app.metrics')


class MetricsCollector:
    """
    메트릭 수집 및 관리 클래스
    
    싱글톤 패턴을 사용하여 전역 메트릭 상태를 관리합니다.
    """
    _instance: Optional['MetricsCollector'] = None
    _request_count: int = 0
    _error_count: int = 0
    _response_times: List[float] = []
    _start_time: float = time()
    
    def __new__(cls) -> 'MetricsCollector':
        """싱글톤 패턴 구현"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def increment_request(self) -> None:
        """요청 수를 증가시킵니다."""
        self._request_count += 1
    
    def increment_error(self) -> None:
        """에러 수를 증가시킵니다."""
        self._error_count += 1
    
    def add_response_time(self, elapsed_time: float) -> None:
        """
        응답 시간을 추가합니다.
        
        Args:
            elapsed_time: 응답 시간 (초)
        """
        self._response_times.append(elapsed_time)
        # 최근 MAX_RESPONSE_TIMES개만 유지 (메모리 효율성)
        if len(self._response_times) > MAX_RESPONSE_TIMES:
            self._response_times = self._response_times[-MAX_RESPONSE_TIMES:]
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        현재 메트릭 정보를 반환합니다.
        
        Returns:
            메트릭 정보 딕셔너리
        """
        metrics_data = {
            "request_count": self._request_count,
            "error_count": self._error_count,
            "error_rate": round(self._error_count / max(self._request_count, 1), 4),
            "uptime_seconds": round(time() - self._start_time, 2)
        }
        
        if self._response_times:
            response_times = self._response_times
            metrics_data["response_time"] = {
                "average": round(sum(response_times) / len(response_times), 4),
                "min": round(min(response_times), 4),
                "max": round(max(response_times), 4),
                "count": len(response_times)
            }
        
        return metrics_data
    
    def get_health_metrics(self) -> Dict[str, Any]:
        """
        헬스 체크용 메트릭 정보를 반환합니다.
        
        Returns:
            헬스 체크 메트릭 정보 딕셔너리
        """
        if not self._response_times:
            return {}
        
        avg_response_time = sum(self._response_times) / len(self._response_times)
        return {
            "request_count": self._request_count,
            "error_count": self._error_count,
            "average_response_time": round(avg_response_time, 4),
            "uptime_seconds": round(time() - self._start_time, 2)
        }
    
    def reset(self) -> None:
        """메트릭을 초기화합니다. (테스트용)"""
        self._request_count = 0
        self._error_count = 0
        self._response_times = []
        self._start_time = time()
        logger.debug("메트릭 초기화 완료")


# 싱글톤 인스턴스 생성 함수
def get_metrics() -> MetricsCollector:
    """
    MetricsCollector 싱글톤 인스턴스를 반환합니다.
    
    Returns:
        MetricsCollector 인스턴스
    """
    return MetricsCollector()

