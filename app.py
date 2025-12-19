"""
천안시 맛집 안내 웹 애플리케이션
Flask 기반 Python 웹 서버
"""
from flask import Flask, render_template, jsonify, send_from_directory
from utils.data_loader import load_restaurants_data

app = Flask(__name__)

@app.route('/')
def index():
    """메인 페이지"""
    restaurants = load_restaurants_data('data/restaurants.json')
    return render_template('index.html', restaurants=restaurants)

@app.route('/api/restaurants')
def api_restaurants():
    """REST API: 매장 데이터 반환"""
    restaurants = load_restaurants_data('data/restaurants.json')
    return jsonify(restaurants)

@app.route('/images/<path:filename>')
def serve_images(filename):
    """이미지 파일 서빙"""
    return send_from_directory('images', filename)

@app.errorhandler(404)
def not_found(error):
    """404 에러 처리"""
    return render_template('error.html', error_code=404, message='페이지를 찾을 수 없습니다.'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 에러 처리"""
    return render_template('error.html', error_code=500, message='서버 오류가 발생했습니다.'), 500

if __name__ == '__main__':
    # 개발 서버 실행
    print("=" * 50)
    print("천안시 맛집 안내 웹사이트")
    print("=" * 50)
    print(f"서버 시작: http://localhost:5000")
    print("종료하려면 Ctrl+C를 누르세요.")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

