"""
매장 데이터 모델
TypedDict를 사용한 타입 정의
"""
from typing import TypedDict, List, Optional


class BlogLink(TypedDict, total=False):
    """블로그 링크 타입 정의"""
    url: str
    title: Optional[str]


class Review(TypedDict, total=False):
    """후기 타입 정의"""
    text: str
    rating: Optional[int]


class RestaurantDict(TypedDict, total=False):
    """
    매장 데이터 타입 정의
    
    TypedDict를 사용하여 JSON 스키마를 타입으로 정의합니다.
    """
    name: str  # 필수 필드
    address: Optional[str]
    phone: Optional[str]
    hours: Optional[str]
    blogLinks: Optional[List[BlogLink]]
    menuImages: Optional[List[str]]
    reviews: Optional[List[Review]]


# 타입 별칭 (하위 호환성)
Restaurant = RestaurantDict

