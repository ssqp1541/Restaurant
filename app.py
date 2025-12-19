"""
천안시 맛집 안내 웹 애플리케이션
Flask 기반 Python 웹 서버
"""
from flask import Flask, render_template, jsonify, send_from_directory
from utils.data_loader import load_restaurants_data
from utils.logger import setup_logger

# 로거 초기화
logger = setup_logger('restaurant_app', log_file='app.log')

app = Flask(__name__)

@app.route('/')
def index():
    """메인 페이지"""
    logger.info("메인 페이지 요청")
    restaurants = load_restaurants_data('data/restaurants.json')
    logger.debug(f"메인 페이지 렌더링: {len(restaurants)}개 매장")
    return render_template('index.html', restaurants=restaurants)

@app.route('/api/restaurants')
def api_restaurants():
    """REST API: 매장 데이터 반환"""
    logger.info("API 엔드포인트 요청: /api/restaurants")
    restaurants = load_restaurants_data('data/restaurants.json')
    logger.debug(f"API 응답: {len(restaurants)}개 매장")
    return jsonify(restaurants)

@app.route('/images/<path:filename>')
def serve_images(filename):
    """이미지 파일 서빙"""
    return send_from_directory('images', filename)

@app.route('/test-error-500')
def test_error_500():
    """500 에러 테스트용 라우트"""
    logger.warning("500 에러 테스트 라우트 호출됨")
    # 의도적으로 500 에러 발생
    raise Exception("테스트용 500 에러")

@app.errorhandler(404)
def not_found(error):
    """404 에러 처리"""
    logger.warning(f"404 에러 발생: {error}")
    return render_template('error.html', error_code=404, message='페이지를 찾을 수 없습니다.'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 에러 처리"""
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

