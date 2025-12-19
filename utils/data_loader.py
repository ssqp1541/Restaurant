"""
데이터 로딩 및 처리 유틸리티 모듈

이 모듈은 매장 데이터를 JSON 파일에서 로드하고, 저장하며, 검증하는 기능을 제공합니다.

주요 기능:
- JSON 파일에서 매장 데이터 로드
- 매장 데이터를 JSON 파일에 저장
- 매장 데이터 유효성 검증
- 매장 추가 및 검색

사용 예시:
    >>> from utils.data_loader import load_restaurants_data, add_restaurant
    >>> restaurants = load_restaurants_data('data/restaurants.json')
    >>> new_restaurant = {"name": "새 매장", "address": "주소"}
    >>> add_restaurant(restaurants, new_restaurant)
    True
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from utils.logger import get_logger
from utils.security import sanitize_path, validate_file_path
from utils.file_utils import validate_and_normalize_path
from utils.constants import DEFAULT_DATA_PATH
from exceptions.restaurant_exceptions import RestaurantDataError, FileAccessError, ValidationError

# 로거 초기화
logger = get_logger('restaurant_app.data_loader')


def load_restaurants_data(file_path: str = DEFAULT_DATA_PATH) -> List[Dict[str, Any]]:
    """
    JSON 파일에서 매장 데이터를 로드합니다.
    
    Args:
        file_path: JSON 파일 경로
        
    Returns:
        매장 데이터 리스트
    """
    try:
        # 파일 경로 검증 및 정규화 (중복 코드 제거)
        normalized_path, _ = validate_and_normalize_path(file_path)
        if normalized_path is None:
            logger.warning(f"안전하지 않은 파일 경로: {file_path}")
            return []
        
        data_file = normalized_path
        if not data_file.exists():
            logger.warning(f"파일을 찾을 수 없습니다: {file_path}")
            return []
        
        logger.debug(f"데이터 파일 로드 시작: {file_path}")
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        result = data if isinstance(data, list) else []
        logger.info(f"데이터 로드 완료: {file_path} ({len(result)}개 매장)")
        return result
    
    except json.JSONDecodeError as e:
        error_msg = f"JSON 형식 오류: {file_path}"
        logger.error(f"{error_msg} - {e}", exc_info=True)
        raise RestaurantDataError(error_msg, error_code="JSON_DECODE_ERROR", details={"file_path": file_path}) from e
    except FileNotFoundError as e:
        error_msg = f"파일을 찾을 수 없습니다: {file_path}"
        logger.error(error_msg, exc_info=True)
        raise FileAccessError(error_msg, file_path=file_path, error_code="FILE_NOT_FOUND", original_error=e) from e
    except PermissionError as e:
        error_msg = f"파일 읽기 권한이 없습니다: {file_path}"
        logger.error(error_msg, exc_info=True)
        raise FileAccessError(error_msg, file_path=file_path, error_code="PERMISSION_DENIED", original_error=e) from e
    except Exception as e:
        error_msg = f"데이터 로드 중 예외 발생: {file_path}"
        logger.error(f"{error_msg} - {e}", exc_info=True)
        raise RestaurantDataError(error_msg, error_code="LOAD_ERROR", details={"file_path": file_path}) from e


def save_restaurants_data(data: List[Dict[str, Any]], file_path: str = DEFAULT_DATA_PATH) -> bool:
    """
    매장 데이터를 JSON 파일에 저장합니다.
    
    Args:
        data: 저장할 매장 데이터 리스트
        file_path: JSON 파일 경로
        
    Returns:
        저장 성공 여부
    """
    try:
        # 파일 경로 검증 및 정규화 (중복 코드 제거)
        normalized_path, _ = validate_and_normalize_path(file_path)
        if normalized_path is None:
            logger.error(f"안전하지 않은 파일 경로: {file_path}")
            return False
        
        data_file = normalized_path
        data_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.debug(f"데이터 파일 저장 시작: {file_path} ({len(data)}개 매장)")
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"데이터 저장 완료: {file_path}")
        return True
    
    except PermissionError as e:
        error_msg = f"파일 저장 권한 오류: {file_path}"
        logger.error(f"{error_msg} - {e}", exc_info=True)
        raise FileAccessError(error_msg, file_path=file_path, error_code="PERMISSION_DENIED", original_error=e) from e
    except OSError as e:
        error_msg = f"파일 시스템 오류: {file_path}"
        logger.error(f"{error_msg} - {e}", exc_info=True)
        raise FileAccessError(error_msg, file_path=file_path, error_code="OS_ERROR", original_error=e) from e
    except Exception as e:
        error_msg = f"데이터 저장 중 예외 발생: {file_path}"
        logger.error(f"{error_msg} - {e}", exc_info=True)
        raise RestaurantDataError(error_msg, error_code="SAVE_ERROR", details={"file_path": file_path}) from e


def _validate_blog_links(blog_links: Any) -> bool:
    """
    블로그 링크 배열의 유효성을 검사합니다. (내부 헬퍼 함수)
    
    Args:
        blog_links: 검사할 블로그 링크 데이터
        
    Returns:
        유효성 여부
    """
    if not isinstance(blog_links, list):
        return False
    if len(blog_links) > 0:
        for blog in blog_links:
            if not isinstance(blog, dict) or 'url' not in blog:
                return False
    return True


def _validate_menu_images(menu_images: Any) -> bool:
    """
    메뉴 이미지 배열의 유효성을 검사합니다. (내부 헬퍼 함수)
    
    Args:
        menu_images: 검사할 메뉴 이미지 데이터
        
    Returns:
        유효성 여부
    """
    return isinstance(menu_images, list)


def _validate_reviews(reviews: Any) -> bool:
    """
    후기 배열의 유효성을 검사합니다. (내부 헬퍼 함수)
    
    Args:
        reviews: 검사할 후기 데이터
        
    Returns:
        유효성 여부
    """
    if not isinstance(reviews, list):
        return False
    for review in reviews:
        if not isinstance(review, dict) or 'text' not in review:
            return False
    return True


def validate_restaurant_data(restaurant: Dict[str, Any]) -> bool:
    """
    매장 데이터의 유효성을 검사합니다.
    
    Args:
        restaurant: 검사할 매장 데이터
        
    Returns:
        유효성 여부 (True: 유효함, False: 유효하지 않음)
    """
    # 필수 필드 검증
    required_fields = ['name']
    for field in required_fields:
        if field not in restaurant:
            return False
    
    # 블로그 링크 검증
    if 'blogLinks' in restaurant:
        if not _validate_blog_links(restaurant['blogLinks']):
            return False
    
    # 메뉴 이미지 검증
    if 'menuImages' in restaurant:
        if not _validate_menu_images(restaurant['menuImages']):
            return False
    
    # 후기 검증
    if 'reviews' in restaurant:
        if not _validate_reviews(restaurant['reviews']):
            return False
    
    return True


def _validate_blog_links_with_error(blog_links: Any) -> Tuple[bool, Optional[str]]:
    """
    블로그 링크 배열의 유효성을 검사하고 에러 메시지를 반환합니다. (내부 헬퍼 함수)
    
    Args:
        blog_links: 검사할 블로그 링크 데이터
        
    Returns:
        (유효성 여부, 에러 메시지) 튜플
    """
    if not isinstance(blog_links, list):
        return False, "blogLinks는 배열이어야 합니다."
    if len(blog_links) > 0:
        for idx, blog in enumerate(blog_links):
            if not isinstance(blog, dict):
                return False, f"blogLinks[{idx}]는 객체여야 합니다."
            if 'url' not in blog:
                return False, f"blogLinks[{idx}]에 'url' 필드가 필요합니다."
    return True, None


def _validate_reviews_with_error(reviews: Any) -> Tuple[bool, Optional[str]]:
    """
    후기 배열의 유효성을 검사하고 에러 메시지를 반환합니다. (내부 헬퍼 함수)
    
    Args:
        reviews: 검사할 후기 데이터
        
    Returns:
        (유효성 여부, 에러 메시지) 튜플
    """
    if not isinstance(reviews, list):
        return False, "reviews는 배열이어야 합니다."
    for idx, review in enumerate(reviews):
        if not isinstance(review, dict):
            return False, f"reviews[{idx}]는 객체여야 합니다."
        if 'text' not in review:
            return False, f"reviews[{idx}]에 'text' 필드가 필요합니다."
    return True, None


def validate_restaurant_data_with_error(restaurant: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    매장 데이터의 유효성을 검사하고 에러 메시지를 반환합니다.
    
    Args:
        restaurant: 검사할 매장 데이터
        
    Returns:
        (유효성 여부, 에러 메시지) 튜플
        - 유효한 경우: (True, None)
        - 유효하지 않은 경우: (False, 에러 메시지 문자열)
    """
    # 필수 필드 검증
    required_fields = ['name']
    for field in required_fields:
        if field not in restaurant:
            return False, f"필수 필드 '{field}'가 누락되었습니다."
    
    # 블로그 링크 검증
    if 'blogLinks' in restaurant:
        is_valid, error_msg = _validate_blog_links_with_error(restaurant['blogLinks'])
        if not is_valid:
            return False, error_msg
    
    # 메뉴 이미지 검증
    if 'menuImages' in restaurant:
        if not isinstance(restaurant['menuImages'], list):
            return False, "menuImages는 배열이어야 합니다."
    
    # 후기 검증
    if 'reviews' in restaurant:
        is_valid, error_msg = _validate_reviews_with_error(restaurant['reviews'])
        if not is_valid:
            return False, error_msg
    
    return True, None


def validate_restaurants_data_list(data: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    매장 데이터 리스트의 유효성을 검사하고 에러 메시지 리스트를 반환합니다.
    
    Args:
        data: 검사할 매장 데이터 리스트
        
    Returns:
        (유효성 여부, 에러 메시지 리스트) 튜플
    """
    errors = []
    
    if not isinstance(data, list):
        return False, ["데이터는 배열이어야 합니다."]
    
    for idx, restaurant in enumerate(data):
        if not isinstance(restaurant, dict):
            errors.append(f"데이터[{idx}]: 매장 데이터는 객체여야 합니다.")
            continue
        
        is_valid, error_msg = validate_restaurant_data_with_error(restaurant)
        if not is_valid:
            errors.append(f"데이터[{idx}]: {error_msg}")
    
    return len(errors) == 0, errors


def add_restaurant(
    data: List[Dict[str, Any]], 
    restaurant: Dict[str, Any],
    allow_duplicate: bool = True
) -> bool:
    """
    새로운 매장을 데이터에 추가합니다.
    
    Args:
        data: 기존 매장 데이터 리스트
        restaurant: 추가할 매장 데이터
        allow_duplicate: 중복 매장명 허용 여부 (기본값: True)
        
    Returns:
        추가 성공 여부
    """
    if not validate_restaurant_data(restaurant):
        logger.warning(f"유효하지 않은 매장 데이터 추가 시도: {restaurant.get('name', 'Unknown')}")
        return False
    
    restaurant_name = restaurant.get('name', 'Unknown')
    
    # 중복 체크 (allow_duplicate가 False인 경우)
    if not allow_duplicate:
        existing = get_restaurant_by_name(data, restaurant_name)
        if existing is not None:
            logger.warning(f"중복 매장명으로 인한 추가 실패: {restaurant_name}")
            return False
    
    logger.info(f"매장 추가: {restaurant_name}")
    data.append(restaurant)
    return True


def get_restaurant_by_name(data: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
    """
    이름으로 매장을 검색합니다.
    
    Args:
        data: 매장 데이터 리스트
        name: 검색할 매장 이름
        
    Returns:
        매장 데이터 또는 None (매장을 찾지 못한 경우)
    """
    for restaurant in data:
        if restaurant.get('name') == name:
            return restaurant
    return None

