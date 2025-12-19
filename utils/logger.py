"""
로깅 유틸리티 모듈
Python logging 모듈을 활용한 로깅 시스템
"""
import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = 'restaurant_app',
    log_level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_dir: str = 'logs'
) -> logging.Logger:
    """
    로거를 설정하고 반환합니다.
    
    Args:
        name: 로거 이름
        log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR)
        log_file: 로그 파일명 (None이면 파일 로깅 안 함)
        log_dir: 로그 디렉토리 경로
        
    Returns:
        설정된 로거 객체
    """
    logger = logging.getLogger(name)
    
    # 이미 핸들러가 설정되어 있으면 기존 로거 반환
    if logger.handlers:
        return logger
    
    logger.setLevel(log_level)
    
    # 로그 포맷 설정
    # 사용자 친화적 메시지와 개발자용 상세 정보 포함
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 콘솔 핸들러 (표준 출력)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 파일 핸들러 (로그 파일 저장)
    if log_file:
        log_dir_path = Path(log_dir)
        log_dir_path.mkdir(parents=True, exist_ok=True)
        
        log_file_path = log_dir_path / log_file
        
        file_handler = logging.FileHandler(
            log_file_path,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = 'restaurant_app') -> logging.Logger:
    """
    기존 로거를 가져오거나 새로 생성합니다.
    
    Args:
        name: 로거 이름
        
    Returns:
        로거 객체
    """
    logger = logging.getLogger(name)
    
    # 로거가 설정되지 않았으면 기본 설정으로 생성
    if not logger.handlers:
        return setup_logger(name=name)
    
    return logger

