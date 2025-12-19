"""
데이터 로딩 및 처리 유틸리티
Python으로 매장 데이터를 관리하고 처리하는 함수들
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional


def load_restaurants_data(file_path: str = 'data/restaurants.json') -> List[Dict[str, Any]]:
    """
    JSON 파일에서 매장 데이터를 로드합니다.
    
    Args:
        file_path: JSON 파일 경로
        
    Returns:
        매장 데이터 리스트
    """
    try:
        data_file = Path(file_path)
        if not data_file.exists():
            print(f"경고: {file_path} 파일을 찾을 수 없습니다.")
            return []
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data if isinstance(data, list) else []
    
    except json.JSONDecodeError as e:
        print(f"경고: {file_path} 파일의 JSON 형식이 올바르지 않습니다: {e}")
        return []
    except Exception as e:
        print(f"오류: 데이터 로드 중 문제가 발생했습니다: {e}")
        return []


def save_restaurants_data(data: List[Dict[str, Any]], file_path: str = 'data/restaurants.json') -> bool:
    """
    매장 데이터를 JSON 파일에 저장합니다.
    
    Args:
        data: 저장할 매장 데이터 리스트
        file_path: JSON 파일 경로
        
    Returns:
        저장 성공 여부
    """
    try:
        data_file = Path(file_path)
        data_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    
    except PermissionError as e:
        print(f"오류: 파일 저장 권한이 없습니다. {file_path}: {e}")
        return False
    except OSError as e:
        print(f"오류: 파일 시스템 오류가 발생했습니다. {file_path}: {e}")
        return False
    except Exception as e:
        print(f"오류: 데이터 저장 중 문제가 발생했습니다: {e}")
        return False


def validate_restaurant_data(restaurant: Dict[str, Any]) -> bool:
    """
    매장 데이터의 유효성을 검사합니다.
    
    Args:
        restaurant: 검사할 매장 데이터
        
    Returns:
        유효성 여부
    """
    required_fields = ['name']
    
    for field in required_fields:
        if field not in restaurant:
            return False
    
    # 블로그 링크 검증
    if 'blogLinks' in restaurant:
        if not isinstance(restaurant['blogLinks'], list):
            return False
        if len(restaurant['blogLinks']) > 0:
            for blog in restaurant['blogLinks']:
                if not isinstance(blog, dict) or 'url' not in blog:
                    return False
    
    # 메뉴 이미지 검증
    if 'menuImages' in restaurant:
        if not isinstance(restaurant['menuImages'], list):
            return False
    
    # 후기 검증
    if 'reviews' in restaurant:
        if not isinstance(restaurant['reviews'], list):
            return False
        for review in restaurant['reviews']:
            if not isinstance(review, dict) or 'text' not in review:
                return False
    
    return True


def validate_restaurant_data_with_error(restaurant: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    매장 데이터의 유효성을 검사하고 에러 메시지를 반환합니다.
    
    Args:
        restaurant: 검사할 매장 데이터
        
    Returns:
        (유효성 여부, 에러 메시지) 튜플
    """
    required_fields = ['name']
    
    # 필수 필드 검증
    for field in required_fields:
        if field not in restaurant:
            return False, f"필수 필드 '{field}'가 누락되었습니다."
    
    # 블로그 링크 검증
    if 'blogLinks' in restaurant:
        if not isinstance(restaurant['blogLinks'], list):
            return False, "blogLinks는 배열이어야 합니다."
        if len(restaurant['blogLinks']) > 0:
            for idx, blog in enumerate(restaurant['blogLinks']):
                if not isinstance(blog, dict):
                    return False, f"blogLinks[{idx}]는 객체여야 합니다."
                if 'url' not in blog:
                    return False, f"blogLinks[{idx}]에 'url' 필드가 필요합니다."
    
    # 메뉴 이미지 검증
    if 'menuImages' in restaurant:
        if not isinstance(restaurant['menuImages'], list):
            return False, "menuImages는 배열이어야 합니다."
    
    # 후기 검증
    if 'reviews' in restaurant:
        if not isinstance(restaurant['reviews'], list):
            return False, "reviews는 배열이어야 합니다."
        for idx, review in enumerate(restaurant['reviews']):
            if not isinstance(review, dict):
                return False, f"reviews[{idx}]는 객체여야 합니다."
            if 'text' not in review:
                return False, f"reviews[{idx}]에 'text' 필드가 필요합니다."
    
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


def add_restaurant(data: List[Dict[str, Any]], restaurant: Dict[str, Any]) -> bool:
    """
    새로운 매장을 데이터에 추가합니다.
    
    Args:
        data: 기존 매장 데이터 리스트
        restaurant: 추가할 매장 데이터
        
    Returns:
        추가 성공 여부
    """
    if not validate_restaurant_data(restaurant):
        print("오류: 매장 데이터가 유효하지 않습니다.")
        return False
    
    data.append(restaurant)
    return True


def get_restaurant_by_name(data: List[Dict[str, Any]], name: str):
    """
    이름으로 매장을 검색합니다.
    
    Args:
        data: 매장 데이터 리스트
        name: 검색할 매장 이름
        
    Returns:
        매장 데이터 또는 None
    """
    for restaurant in data:
        if restaurant.get('name') == name:
            return restaurant
    return None

