"""
상수 정의 모듈
애플리케이션 전반에서 사용되는 상수들을 정의합니다.
"""
from pathlib import Path

# 파일 경로 상수
DEFAULT_DATA_PATH: str = 'data/restaurants.json'
DEFAULT_IMAGES_DIR: str = 'images'
DEFAULT_LOGS_DIR: str = 'logs'
DEFAULT_LOG_FILE: str = 'app.log'

# 메트릭 관련 상수
MAX_RESPONSE_TIMES: int = 100  # 최대 응답 시간 기록 수

# 이미지 파일 확장자
ALLOWED_IMAGE_EXTENSIONS: list[str] = ['.jpg', '.jpeg', '.png', '.gif']

# 에러 메시지 상수
ERROR_MESSAGES = {
    'PAGE_NOT_FOUND': '페이지를 찾을 수 없습니다.',
    'SERVER_ERROR': '서버 오류가 발생했습니다.',
    'BAD_REQUEST': '잘못된 요청입니다.',
    'DATA_LOAD_FAILED': '데이터를 불러올 수 없습니다.',
    'UNSAFE_FILE_PATH': '안전하지 않은 파일 경로입니다.',
    'FILE_NOT_FOUND': '파일을 찾을 수 없습니다.',
    'UNSAFE_PATH': '안전하지 않은 파일 경로입니다.',
}

# 에러 코드 상수
ERROR_CODES = {
    'BAD_REQUEST': 'ERR_BAD_REQUEST',
    'DATA_LOAD_FAILED': 'ERR_DATA_LOAD_FAILED',
    'SERVER_ERROR': 'ERR_500',
    'NOT_FOUND': 'ERR_404',
}

# 서버 설정 상수
SERVER_CONFIG = {
    'HOST': '0.0.0.0',
    'PORT': 5000,
    'DEBUG': True,
}

