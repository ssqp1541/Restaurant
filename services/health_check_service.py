"""
헬스 체크 서비스 모듈
헬스 체크 관련 비즈니스 로직을 담당합니다.
"""
from typing import Tuple, Dict, Any
from pathlib import Path
from utils.constants import DEFAULT_DATA_PATH
from utils.logger import get_logger
from services.restaurant_service import RestaurantService

logger = get_logger('restaurant_app.services.health')


class HealthCheckService:
    """
    헬스 체크 서비스 클래스
    
    단일 책임: 헬스 체크 관련 비즈니스 로직만 담당
    """
    
    def __init__(self, restaurant_service: RestaurantService):
        """
        서비스 초기화
        
        Args:
            restaurant_service: 매장 서비스 인스턴스 (의존성 주입)
        """
        self._restaurant_service = restaurant_service
    
    def check_filesystem(self) -> Tuple[str, bool]:
        """
        파일 시스템 접근 가능 여부를 확인합니다.
        
        Returns:
            (상태 메시지, 건강 여부) 튜플
        """
        try:
            test_file = Path(DEFAULT_DATA_PATH)
            if test_file.exists():
                return "ok", True
            else:
                return "warning", False
        except Exception as e:
            logger.error(f"파일 시스템 체크 실패: {e}", exc_info=True)
            return f"error: {str(e)}", False
    
    def check_data_load(self) -> Tuple[str, bool, int]:
        """
        데이터 로드 가능 여부를 확인합니다.
        
        Returns:
            (상태 메시지, 건강 여부, 데이터 개수) 튜플
        """
        try:
            restaurants = self._restaurant_service.get_all_restaurants()
            return "ok", True, len(restaurants)
        except Exception as e:
            logger.error(f"데이터 로드 체크 실패: {e}", exc_info=True)
            return f"error: {str(e)}", False, 0
    
    def perform_health_check(
        self,
        metrics: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], int]:
        """
        전체 헬스 체크를 수행합니다.
        
        Args:
            metrics: 메트릭 정보
            
        Returns:
            (헬스 체크 결과, 상태 코드) 튜플
        """
        health_status = {
            "status": "healthy",
            "checks": {}
        }
        overall_healthy = True
        
        # 파일 시스템 체크
        fs_status, fs_healthy = self.check_filesystem()
        health_status["checks"]["filesystem"] = fs_status
        if not fs_healthy:
            overall_healthy = False
        
        # 데이터 로드 체크
        data_status, data_healthy, data_count = self.check_data_load()
        health_status["checks"]["data_load"] = data_status
        if not data_healthy:
            overall_healthy = False
        else:
            health_status["data_count"] = data_count
        
        # 메트릭 정보 추가
        if metrics:
            health_status["metrics"] = metrics
        
        status_code = 200 if overall_healthy else 503
        health_status["status"] = "healthy" if overall_healthy else "degraded"
        
        return health_status, status_code

