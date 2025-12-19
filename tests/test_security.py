"""
보안 기능 테스트
N5. 보안 강화 테스트
"""
import pytest
from pathlib import Path
from utils.security import (
    sanitize_path,
    validate_file_path,
    sanitize_string,
    validate_url
)


class TestPathSanitization:
    """경로 정규화 및 검증 테스트 (N5.2)"""
    
    def test_sanitize_safe_path(self):
        """안전한 경로 정규화"""
        result = sanitize_path('data/restaurants.json', base_dir='.')
        assert result is not None
        assert isinstance(result, Path)
    
    def test_sanitize_path_traversal_attack(self):
        """경로 탐색 공격 방지 테스트"""
        # 상위 디렉토리로 이동 시도
        result = sanitize_path('../../etc/passwd', base_dir='data')
        assert result is None
        
        # 절대 경로 사용 시도
        result = sanitize_path('/etc/passwd', base_dir='data')
        # base_dir 밖으로 나가는 경로는 차단되어야 함
        assert result is None or str(result).replace('\\', '/') != '/etc/passwd'
    
    def test_validate_file_path_with_extension(self):
        """파일 확장자 검증 테스트"""
        # 허용된 확장자
        assert validate_file_path('data/restaurants.json', allowed_extensions=['.json'], base_dir='.') is True
        
        # 허용되지 않은 확장자
        assert validate_file_path('data/script.exe', allowed_extensions=['.json'], base_dir='.') is False


class TestStringSanitization:
    """문자열 정리 테스트 (N5.1: XSS 방지)"""
    
    def test_sanitize_string_length_limit(self):
        """문자열 길이 제한 테스트"""
        long_string = 'a' * 2000
        result = sanitize_string(long_string, max_length=1000)
        assert len(result) == 1000
    
    def test_sanitize_string_removes_script_tags(self):
        """스크립트 태그 제거 테스트"""
        dangerous_string = '<script>alert("XSS")</script>안전한 텍스트'
        result = sanitize_string(dangerous_string)
        assert '<script>' not in result.lower()
        assert '안전한 텍스트' in result
    
    def test_sanitize_string_removes_javascript_protocol(self):
        """javascript: 프로토콜 제거 테스트"""
        dangerous_string = 'javascript:alert("XSS")'
        result = sanitize_string(dangerous_string)
        assert 'javascript:' not in result.lower()


class TestURLValidation:
    """URL 검증 테스트"""
    
    def test_validate_valid_url(self):
        """유효한 URL 검증"""
        assert validate_url('https://example.com') is True
        assert validate_url('http://blog.naver.com/test') is True
        assert validate_url('https://example.com/path?query=value') is True
    
    def test_validate_invalid_url(self):
        """유효하지 않은 URL 검증"""
        assert validate_url('not a url') is False
        assert validate_url('') is False
        assert validate_url('javascript:alert(1)') is False

