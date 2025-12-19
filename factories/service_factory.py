"""
서비스 팩토리 모듈
서비스 객체 생성을 담당하는 팩토리 클래스입니다.
"""
from typing import Optional
from services.restaurant_service import RestaurantService
from services.metrics_service import MetricsService
from services.health_check_service import HealthCheckService
from repositories.restaurant_repository import RestaurantRepository, IDataRepository
from utils.logger import get_logger

logger = get_logger('restaurant_app.factories.service')


class ServiceFactory:
    """
    서비스 객체 생성 팩토리 클래스
    
    Factory 패턴을 적용하여 서비스 객체 생성을 캡슐화합니다.
    설정 기반으로 서비스 객체를 생성할 수 있습니다.
    """
    
    @staticmethod
    def create_restaurant_service(
        repository: Optional[IDataRepository] = None
    ) -> RestaurantService:
        """
        RestaurantService 인스턴스를 생성합니다.
        
        Args:
            repository: 데이터 리포지토리 (None이면 기본 리포지토리 사용)
            
        Returns:
            RestaurantService 인스턴스
        """
        if repository is None:
            repository = RestaurantRepository()
        service = RestaurantService(repository)
        logger.debug("RestaurantService 생성 완료")
        return service
    
    @staticmethod
    def create_metrics_service() -> MetricsService:
        """
        MetricsService 인스턴스를 생성합니다.
        
        Returns:
            MetricsService 인스턴스
        """
        service = MetricsService()
        logger.debug("MetricsService 생성 완료")
        return service
    
    @staticmethod
    def create_health_check_service(
        restaurant_service: Optional[RestaurantService] = None
    ) -> HealthCheckService:
        """
        HealthCheckService 인스턴스를 생성합니다.
        
        Args:
            restaurant_service: 매장 서비스 (None이면 기본 서비스 사용)
            
        Returns:
            HealthCheckService 인스턴스
        """
        if restaurant_service is None:
            restaurant_service = ServiceFactory.create_restaurant_service()
        service = HealthCheckService(restaurant_service)
        logger.debug("HealthCheckService 생성 완료")
        return service
    
    @staticmethod
    def create_all_services() -> tuple[RestaurantService, MetricsService, HealthCheckService]:
        """
        모든 서비스를 생성합니다.
        
        Returns:
            (RestaurantService, MetricsService, HealthCheckService) 튜플
        """
        restaurant_service = ServiceFactory.create_restaurant_service()
        metrics_service = ServiceFactory.create_metrics_service()
        health_check_service = ServiceFactory.create_health_check_service(restaurant_service)
        logger.info("모든 서비스 생성 완료")
        return restaurant_service, metrics_service, health_check_service

