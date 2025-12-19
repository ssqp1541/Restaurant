"""
보안 유틸리티 모듈
보안 관련 함수들을 제공합니다.
"""
import os
import re
from pathlib import Path
from typing import Optional
from urllib.parse import quote, unquote
from utils.logger import get_logger

logger = get_logger('restaurant_app.security')


def sanitize_path(file_path: str, base_dir: Optional[str] = None, allow_absolute: bool = False) -> Optional[Path]:
    """
    파일 경로를 검증하고 정규화합니다. (경로 탐색 공격 방지)
    
    Args:
        file_path: 검증할 파일 경로
        base_dir: 기준 디렉토리 (None이면 현재 작업 디렉토리)
        allow_absolute: 절대 경로 허용 여부 (테스트 환경용, 기본값: False)
        
    Returns:
        정규화된 Path 객체 또는 None (안전하지 않은 경로인 경우)
    """
    try:
        # 절대 경로인 경우 처리
        file_path_obj = Path(file_path)
        if file_path_obj.is_absolute():
            if allow_absolute:
                # 테스트 환경에서 절대 경로 허용 (임시 파일 등)
                # 임시 디렉토리인지 확인
                temp_dirs = ['temp', 'tmp', 'appdata']
                file_path_str = str(file_path).lower()
                if any(temp_dir in file_path_str for temp_dir in temp_dirs):
                    return file_path_obj.resolve()
                else:
                    logger.warning(f"허용되지 않은 절대 경로: {file_path}")
                    return None
            else:
                # 절대 경로는 base_dir 기준 검증 불가
                logger.warning(f"절대 경로는 허용되지 않습니다: {file_path}")
                return None
        
        if base_dir is None:
            base_dir = os.getcwd()
        
        # 경로 정규화
        base_path = Path(base_dir).resolve()
        full_path = (base_path / file_path).resolve()
        
        # 경로 탐색 공격 방지: base_dir 밖으로 나가는 경로 차단
        try:
            full_path.relative_to(base_path)
        except ValueError:
            logger.warning(f"경로 탐색 공격 시도 감지: {file_path}")
            return None
        
        return full_path
    except Exception as e:
        logger.error(f"경로 검증 중 오류 발생: {file_path} - {e}", exc_info=True)
        return None


def validate_file_path(file_path: str, allowed_extensions: Optional[list[str]] = None, base_dir: Optional[str] = None) -> bool:
    """
    파일 경로의 유효성을 검증합니다.
    
    Args:
        file_path: 검증할 파일 경로
        allowed_extensions: 허용된 파일 확장자 리스트 (예: ['.json', '.jpg'])
        base_dir: 기준 디렉토리
        
    Returns:
        유효성 여부
    """
    # 경로 정규화 및 검증
    normalized_path = sanitize_path(file_path, base_dir)
    if normalized_path is None:
        return False
    
    # 파일 확장자 검증
    if allowed_extensions:
        file_ext = normalized_path.suffix.lower()
        if file_ext not in allowed_extensions:
            logger.warning(f"허용되지 않은 파일 확장자: {file_ext}")
            return False
    
    return True


def sanitize_string(input_str: str, max_length: int = 1000) -> str:
    """
    문자열을 정리하고 안전하게 만듭니다. (XSS 방지 기본 처리)
    
    Args:
        input_str: 정리할 문자열
        max_length: 최대 길이
        
    Returns:
        정리된 문자열
    """
    if not isinstance(input_str, str):
        return ""
    
    # 길이 제한
    if len(input_str) > max_length:
        input_str = input_str[:max_length]
        logger.warning(f"문자열 길이 제한: {max_length}자로 잘림")
    
    # 위험한 문자 패턴 제거 (기본적인 XSS 방지)
    # 실제로는 Jinja2 템플릿이 자동으로 이스케이프하므로 추가 보호
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
    ]
    
    sanitized = input_str
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    
    return sanitized


def validate_url(url: str) -> bool:
    """
    URL의 유효성을 검증합니다.
    
    Args:
        url: 검증할 URL
        
    Returns:
        유효성 여부
    """
    if not isinstance(url, str) or not url:
        return False
    
    # 기본 URL 형식 검증
    url_pattern = re.compile(
        r'^https?://'  # http:// 또는 https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # 도메인
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP 주소
        r'(?::\d+)?'  # 포트
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    return bool(url_pattern.match(url))

