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
from typing import Tuple, Optional
from functools import wraps
from pathlib import Path
from flask import Flask, render_template, jsonify, send_from_directory, Response
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest
from utils.cache import get_cache
from utils.metrics import get_metrics
from utils.logger import setup_logger
from utils.security import validate_file_path
from utils.constants import (
    DEFAULT_DATA_PATH,
    ERROR_MESSAGES,
    ERROR_CODES,
    ALLOWED_IMAGE_EXTENSIONS,
    SERVER_CONFIG
)

# 로거 초기화
logger = setup_logger('restaurant_app', log_file='app.log')

app = Flask(__name__)

# 싱글톤 인스턴스 초기화
cache = get_cache()
metrics = get_metrics()


def _track_request_time(func):
    """
    요청 처리 시간을 추적하는 데코레이터 (N6.1)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        try:
            response = func(*args, **kwargs)
            elapsed_time = time() - start_time
            metrics.add_response_time(elapsed_time)
            return response
        except Exception as e:
            metrics.increment_error()
            raise
    return wrapper


def _get_restaurants_data() -> list:
    """
    캐시된 매장 데이터를 반환하거나 로드합니다.
    
    Returns:
        매장 데이터 리스트
    """
    return cache.get_data()


@app.route('/')
@_track_request_time
def index() -> str:
    """
    메인 페이지 라우트
    
    Returns:
        렌더링된 HTML 템플릿 (Jinja2가 자동으로 XSS 방지)
    """
    metrics.increment_request()
    logger.info("메인 페이지 요청")
    restaurants = _get_restaurants_data()
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
        metrics.increment_request()
        logger.info("API 엔드포인트 요청: /api/restaurants")
        restaurants = _get_restaurants_data()
        logger.debug(f"API 응답: {len(restaurants)}개 매장")
        
        # 표준화된 성공 응답 형식
        response_data = {
            "success": True,
            "data": restaurants,
            "count": len(restaurants)
        }
        return jsonify(response_data), 200
    except Exception as e:
        metrics.increment_error()
        logger.error(f"API 데이터 로드 중 오류 발생: {e}", exc_info=True)
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
def bad_request(error) -> Tuple[Response, int]:
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
    metrics.increment_error()
    logger.error(f"500 에러 발생: {error}", exc_info=True)
    return render_template(
        'error.html',
        error_code=500,
        message=ERROR_MESSAGES['SERVER_ERROR']
    ), 500


def _check_filesystem_health() -> Tuple[str, bool]:
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
        return f"error: {str(e)}", False


def _check_data_load_health() -> Tuple[str, bool, int]:
    """
    데이터 로드 가능 여부를 확인합니다.
    
    Returns:
        (상태 메시지, 건강 여부, 데이터 개수) 튜플
    """
    try:
        restaurants = _get_restaurants_data()
        return "ok", True, len(restaurants)
    except Exception as e:
        return f"error: {str(e)}", False, 0


@app.route('/health')
def health_check() -> Tuple[Response, int]:
    """
    헬스 체크 엔드포인트 (N6.2)
    
    Returns:
        JSON 형식의 헬스 체크 응답
    """
    health_status = {
        "status": "healthy",
        "checks": {}
    }
    overall_healthy = True
    
    # 파일 시스템 접근 가능 여부 확인 (N6.2)
    fs_status, fs_healthy = _check_filesystem_health()
    health_status["checks"]["filesystem"] = fs_status
    if not fs_healthy:
        overall_healthy = False
    
    # 데이터 로드 가능 여부 확인
    data_status, data_healthy, data_count = _check_data_load_health()
    health_status["checks"]["data_load"] = data_status
    if not data_healthy:
        overall_healthy = False
    else:
        health_status["data_count"] = data_count
    
    # 메트릭 정보 추가 (N6.1)
    health_metrics = metrics.get_health_metrics()
    if health_metrics:
        health_status["metrics"] = health_metrics
    
    status_code = 200 if overall_healthy else 503
    health_status["status"] = "healthy" if overall_healthy else "degraded"
    
    return jsonify(health_status), status_code


@app.route('/api/metrics')
def api_metrics() -> Response:
    """
    메트릭 정보 API 엔드포인트 (N6.1)
    
    Returns:
        JSON 형식의 메트릭 정보
    """
    metrics_data = metrics.get_metrics()
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

