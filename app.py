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
from typing import Tuple, Dict, Any
from time import time
from functools import wraps
from flask import Flask, render_template, jsonify, send_from_directory, Response, request
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest
from utils.data_loader import load_restaurants_data
from utils.logger import setup_logger
from utils.security import sanitize_path, validate_file_path

# 로거 초기화
logger = setup_logger('restaurant_app', log_file='app.log')

app = Flask(__name__)

# 데이터 캐싱을 위한 전역 변수
_restaurants_cache: list = []
_cache_file_path: str = 'data/restaurants.json'

# 메트릭 수집을 위한 전역 변수 (N6.1)
_metrics: Dict[str, Any] = {
    'request_count': 0,
    'error_count': 0,
    'response_times': [],
    'start_time': time()
}


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
            _metrics['response_times'].append(elapsed_time)
            # 최근 100개만 유지 (메모리 효율성)
            if len(_metrics['response_times']) > 100:
                _metrics['response_times'] = _metrics['response_times'][-100:]
            return response
        except Exception as e:
            _metrics['error_count'] += 1
            raise
    return wrapper


def _get_restaurants_data() -> list:
    """
    캐시된 매장 데이터를 반환하거나 로드합니다.
    
    Returns:
        매장 데이터 리스트
    """
    global _restaurants_cache, _cache_file_path
    
    # 캐시가 비어있거나 파일이 변경되었는지 확인
    if not _restaurants_cache:
        _restaurants_cache = load_restaurants_data(_cache_file_path)
        logger.debug(f"데이터 캐시 로드: {len(_restaurants_cache)}개 매장")
    
    return _restaurants_cache


@app.route('/')
@_track_request_time
def index() -> str:
    """
    메인 페이지 라우트
    
    Returns:
        렌더링된 HTML 템플릿 (Jinja2가 자동으로 XSS 방지)
    """
    _metrics['request_count'] += 1
    logger.info("메인 페이지 요청")
    restaurants = _get_restaurants_data()
    logger.debug(f"메인 페이지 렌더링: {len(restaurants)}개 매장")
    # Jinja2 템플릿은 자동으로 HTML 이스케이프를 수행하므로 XSS 방지됨 (N5.1)
    return render_template('index.html', restaurants=restaurants)


def _create_error_response(message: str, status_code: int, error_code: str = None) -> Tuple[Response, int]:
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
        _metrics['request_count'] += 1
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
        _metrics['error_count'] += 1
        logger.error(f"API 데이터 로드 중 오류 발생: {e}", exc_info=True)
        return _create_error_response(
            "데이터를 불러올 수 없습니다.",
            500,
            "ERR_DATA_LOAD_FAILED"
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
    if not validate_file_path(filename, allowed_extensions=['.jpg', '.jpeg', '.png', '.gif'], base_dir='images'):
        logger.warning(f"안전하지 않은 이미지 경로 접근 시도: {filename}")
        raise BadRequest("안전하지 않은 파일 경로입니다.")
    
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
    return render_template('error.html', error_code=404, message='페이지를 찾을 수 없습니다.'), 404


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
        "잘못된 요청입니다.",
        400,
        "ERR_BAD_REQUEST"
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
    _metrics['error_count'] += 1
    logger.error(f"500 에러 발생: {error}", exc_info=True)
    return render_template('error.html', error_code=500, message='서버 오류가 발생했습니다.'), 500


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
    try:
        test_file = Path('data/restaurants.json')
        if test_file.exists():
            health_status["checks"]["filesystem"] = "ok"
        else:
            health_status["checks"]["filesystem"] = "warning"
            overall_healthy = False
    except Exception as e:
        health_status["checks"]["filesystem"] = f"error: {str(e)}"
        overall_healthy = False
    
    # 데이터 로드 가능 여부 확인
    try:
        restaurants = _get_restaurants_data()
        health_status["checks"]["data_load"] = "ok"
        health_status["data_count"] = len(restaurants)
    except Exception as e:
        health_status["checks"]["data_load"] = f"error: {str(e)}"
        overall_healthy = False
    
    # 메트릭 정보 추가 (N6.1)
    if _metrics['response_times']:
        avg_response_time = sum(_metrics['response_times']) / len(_metrics['response_times'])
        health_status["metrics"] = {
            "request_count": _metrics['request_count'],
            "error_count": _metrics['error_count'],
            "average_response_time": round(avg_response_time, 4),
            "uptime_seconds": round(time() - _metrics['start_time'], 2)
        }
    
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
    metrics_data = {
        "request_count": _metrics['request_count'],
        "error_count": _metrics['error_count'],
        "error_rate": round(_metrics['error_count'] / max(_metrics['request_count'], 1), 4),
        "uptime_seconds": round(time() - _metrics['start_time'], 2)
    }
    
    if _metrics['response_times']:
        response_times = _metrics['response_times']
        metrics_data["response_time"] = {
            "average": round(sum(response_times) / len(response_times), 4),
            "min": round(min(response_times), 4),
            "max": round(max(response_times), 4),
            "count": len(response_times)
        }
    
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
    
    app.run(debug=True, host='0.0.0.0', port=5000)

