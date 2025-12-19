"""
pytest 설정 파일
Flask 애플리케이션 테스트를 위한 픽스처 정의
"""
import pytest
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app import app as flask_app


@pytest.fixture
def app():
    """Flask 애플리케이션 픽스처"""
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['PROPAGATE_EXCEPTIONS'] = False  # 에러 핸들러가 작동하도록 설정
    return flask_app


@pytest.fixture
def client(app):
    """Flask 테스트 클라이언트 픽스처"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Flask CLI 테스트 러너 픽스처"""
    return app.test_cli_runner()

