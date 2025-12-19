"""
천안시 맛집 안내 웹 애플리케이션
Flask 기반 Python 웹 서버

이 모듈은 천안시 맛집 정보를 제공하는 웹 애플리케이션의 메인 진입점입니다.
주요 기능:
- 메인 페이지 렌더링
- REST API를 통한 매장 데이터 제공
- 이미지 파일 서빙
- 에러 처리 (404, 500)

사용 방법:
    python app.py

서버가 시작되면 http://localhost:5000 에서 접속할 수 있습니다.
"""
from typing import Tuple, Optional, Callable, Any, TypeVar, cast
from functools import wraps
from pathlib import Path
from flask import Flask, render_template, jsonify, send_from_directory, Response
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest
from utils.logger import setup_logger
from utils.security import validate_file_path
from utils.constants import (
    ERROR_MESSAGES,
    ERROR_CODES,
    ALLOWED_IMAGE_EXTENSIONS,
    SERVER_CONFIG
)
from factories.service_factory import ServiceFactory
from exceptions.restaurant_exceptions import RestaurantDataError, FileAccessError, ValidationError

F = TypeVar('F', bound=Callable[..., Any])

# 로거 초기화
logger = setup_logger('restaurant_app', log_file='app.log')

app = Flask(__name__)

# 서비스 레이어 초기화 (Factory 패턴 사용)
restaurant_service, metrics_service, health_check_service = ServiceFactory.create_all_services()


def _track_request_time(func: F) -> F:
    """
    요청 처리 시간을 추적하는 데코레이터 (N6.1)
    
    Args:
        func: 추적할 함수
        
    Returns:
        래핑된 함수
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        from time import time
        start_time = time()
        try:
            response = func(*args, **kwargs)
            elapsed_time = time() - start_time
            metrics_service.add_response_time(elapsed_time)
            return response
        except Exception as e:
            metrics_service.increment_error()
            raise
    return cast(F, wrapper)


@app.route('/')
@_track_request_time
def index() -> str:
    """
    메인 페이지 라우트
    
    Returns:
        렌더링된 HTML 템플릿 (Jinja2가 자동으로 XSS 방지)
    """
    metrics_service.increment_request()
    logger.info("메인 페이지 요청")
    restaurants = restaurant_service.get_all_restaurants()
    logger.debug(f"메인 페이지 렌더링: {len(restaurants)}개 매장")
    # Jinja2 템플릿은 자동으로 HTML 이스케이프를 수행하므로 XSS 방지됨 (N5.1)
    return render_template('index.html', restaurants=restaurants)


def _create_error_response(
    message: str,
    status_code: int,
    error_code: Optional[str] = None
) -> Tuple[Response, int]:
    """
    표준화된 API 에러 응답을 생성합니다.
    
    Args:
        message: 에러 메시지
        status_code: HTTP 상태 코드
        error_code: 에러 코드 (선택사항)
        
    Returns:
        JSON 응답과 상태 코드 튜플
    """
    error_response = {
        "success": False,
        "error": {
            "message": message,
            "code": error_code or f"ERR_{status_code}",
            "status": status_code
        }
    }
    return jsonify(error_response), status_code


@app.route('/api/restaurants')
@_track_request_time
def api_restaurants() -> Response:
    """
    REST API: 매장 데이터 반환
    
    Returns:
        JSON 형식의 매장 데이터 리스트 또는 에러 응답
        
    성공 응답 (200):
        {
            "success": true,
            "data": [...],
            "count": 3
        }
        
    에러 응답 (500):
        {
            "success": false,
            "error": {
                "message": "데이터를 불러올 수 없습니다.",
                "code": "ERR_500",
                "status": 500
            }
        }
    """
    try:
        metrics_service.increment_request()
        logger.info("API 엔드포인트 요청: /api/restaurants")
        restaurants = restaurant_service.get_all_restaurants()
        logger.debug(f"API 응답: {len(restaurants)}개 매장")
        
        # 표준화된 성공 응답 형식
        response_data = {
            "success": True,
            "data": restaurants,
            "count": len(restaurants)
        }
        return jsonify(response_data), 200
    except (RestaurantDataError, FileAccessError) as e:
        metrics_service.increment_error()
        logger.error(f"API 데이터 로드 중 오류 발생: {e}", exc_info=True)
        return _create_error_response(
            str(e),
            500,
            getattr(e, 'error_code', ERROR_CODES['DATA_LOAD_FAILED'])
        )
    except Exception as e:
        metrics_service.increment_error()
        logger.error(f"API 데이터 로드 중 예상치 못한 오류 발생: {e}", exc_info=True)
        return _create_error_response(
            ERROR_MESSAGES['DATA_LOAD_FAILED'],
            500,
            ERROR_CODES['DATA_LOAD_FAILED']
        )


@app.route('/images/<path:filename>')
@_track_request_time
def serve_images(filename: str) -> Response:
    """
    이미지 파일 서빙 (N5.2: 파일 접근 보안)
    
    Args:
        filename: 이미지 파일 경로
        
    Returns:
        이미지 파일 응답 또는 404 에러
    """
    # 경로 탐색 공격 방지 (N5.1, N5.2)
    if not validate_file_path(
        filename,
        allowed_extensions=ALLOWED_IMAGE_EXTENSIONS,
        base_dir='images'
    ):
        logger.warning(f"안전하지 않은 이미지 경로 접근 시도: {filename}")
        raise BadRequest(ERROR_MESSAGES['UNSAFE_FILE_PATH'])
    
    return send_from_directory('images', filename)


@app.route('/test-error-500')
def test_error_500() -> None:
    """
    500 에러 테스트용 라우트
    
    Raises:
        Exception: 테스트용 500 에러
    """
    logger.warning("500 에러 테스트 라우트 호출됨")
    # 의도적으로 500 에러 발생
    raise Exception("테스트용 500 에러")


@app.errorhandler(404)
def not_found(error: NotFound) -> Tuple[str, int]:
    """
    404 에러 핸들러
    
    Args:
        error: NotFound 예외 객체
        
    Returns:
        렌더링된 에러 페이지와 404 상태 코드
    """
    logger.warning(f"404 에러 발생: {error}")
    return render_template(
        'error.html',
        error_code=404,
        message=ERROR_MESSAGES['PAGE_NOT_FOUND']
    ), 404


@app.errorhandler(400)
def bad_request(error: BadRequest) -> Tuple[Response, int]:
    """
    400 에러 핸들러 (API용)
    
    Args:
        error: BadRequest 예외 객체
        
    Returns:
        JSON 에러 응답과 400 상태 코드
    """
    logger.warning(f"400 에러 발생: {error}")
    return _create_error_response(
        ERROR_MESSAGES['BAD_REQUEST'],
        400,
        ERROR_CODES['BAD_REQUEST']
    )


@app.errorhandler(500)
def internal_error(error: InternalServerError) -> Tuple[str, int]:
    """
    500 에러 핸들러
    
    Args:
        error: InternalServerError 예외 객체
        
    Returns:
        렌더링된 에러 페이지와 500 상태 코드
    """
    metrics_service.increment_error()
    logger.error(f"500 에러 발생: {error}", exc_info=True)
    return render_template(
        'error.html',
        error_code=500,
        message=ERROR_MESSAGES['SERVER_ERROR']
    ), 500


@app.route('/health')
def health_check() -> Tuple[Response, int]:
    """
    헬스 체크 엔드포인트 (N6.2)
    
    Returns:
        JSON 형식의 헬스 체크 응답
    """
    health_metrics = metrics_service.get_health_metrics()
    health_status, status_code = health_check_service.perform_health_check(health_metrics)
    return jsonify(health_status), status_code


@app.route('/api/metrics')
def api_metrics() -> Response:
    """
    메트릭 정보 API 엔드포인트 (N6.1)
    
    Returns:
        JSON 형식의 메트릭 정보
    """
    metrics_data = metrics_service.get_metrics()
    return jsonify(metrics_data), 200

if __name__ == '__main__':
    # 개발 서버 실행
    logger.info("=" * 50)
    logger.info("천안시 맛집 안내 웹사이트")
    logger.info("=" * 50)
    logger.info("서버 시작: http://localhost:5000")
    logger.info("종료하려면 Ctrl+C를 누르세요.")
    logger.info("=" * 50)
    
    print("=" * 50)
    print("천안시 맛집 안내 웹사이트")
    print("=" * 50)
    print(f"서버 시작: http://localhost:5000")
    print("종료하려면 Ctrl+C를 누르세요.")
    print("=" * 50)
    
    app.run(
        debug=SERVER_CONFIG['DEBUG'],
        host=SERVER_CONFIG['HOST'],
        port=SERVER_CONFIG['PORT']
    )

