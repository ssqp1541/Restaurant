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
from typing import Tuple
from flask import Flask, render_template, jsonify, send_from_directory, Response
from werkzeug.exceptions import NotFound, InternalServerError
from utils.data_loader import load_restaurants_data
from utils.logger import setup_logger

# 로거 초기화
logger = setup_logger('restaurant_app', log_file='app.log')

app = Flask(__name__)

# 데이터 캐싱을 위한 전역 변수
_restaurants_cache: list = []
_cache_file_path: str = 'data/restaurants.json'


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
def index() -> str:
    """
    메인 페이지 라우트
    
    Returns:
        렌더링된 HTML 템플릿
    """
    logger.info("메인 페이지 요청")
    restaurants = _get_restaurants_data()
    logger.debug(f"메인 페이지 렌더링: {len(restaurants)}개 매장")
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
        logger.error(f"API 데이터 로드 중 오류 발생: {e}", exc_info=True)
        return _create_error_response(
            "데이터를 불러올 수 없습니다.",
            500,
            "ERR_DATA_LOAD_FAILED"
        )


@app.route('/images/<path:filename>')
def serve_images(filename: str) -> Response:
    """
    이미지 파일 서빙
    
    Args:
        filename: 이미지 파일 경로
        
    Returns:
        이미지 파일 응답 또는 404 에러
    """
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
    logger.error(f"500 에러 발생: {error}", exc_info=True)
    return render_template('error.html', error_code=500, message='서버 오류가 발생했습니다.'), 500

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

