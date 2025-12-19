"""
통합 테스트
TDD RED 단계: 실패하는 테스트 작성
"""
import pytest
import json
from utils.data_loader import load_restaurants_data, validate_restaurant_data


class TestFlaskAppDataLoaderIntegration:
    """Flask 앱과 데이터 로더 통합 테스트"""
    
    def test_data_load_and_template_rendering(self, client):
        """데이터 로드 후 템플릿 렌더링 확인"""
        # 데이터 로드
        restaurants = load_restaurants_data('data/restaurants.json')
        
        # Flask 앱을 통해 렌더링
        response = client.get('/')
        
        assert response.status_code == 200
        # 템플릿에 데이터가 전달되었는지 확인
        # 실제로는 템플릿에 매장 데이터가 포함되어 있어야 함
        if len(restaurants) > 0:
            # 첫 번째 매장명이 템플릿에 포함되어 있는지 확인
            first_restaurant_name = restaurants[0]['name']
            assert first_restaurant_name.encode('utf-8') in response.data
    
    def test_api_endpoint_data_loader_integration(self, client):
        """API 엔드포인트와 데이터 로더 연동 확인"""
        # 데이터 로더로 직접 로드
        direct_data = load_restaurants_data('data/restaurants.json')
        
        # API를 통해 가져오기
        response = client.get('/api/restaurants')
        api_data = json.loads(response.data)
        
        # 두 데이터가 일치하는지 확인
        assert len(direct_data) == len(api_data)
        if len(direct_data) > 0:
            assert direct_data[0]['name'] == api_data[0]['name']


class TestDataValidationIntegration:
    """데이터 검증 통합 테스트"""
    
    def test_invalid_data_format_handling(self, client):
        """잘못된 데이터 형식 처리 확인"""
        # RED 단계: 잘못된 데이터 형식에 대한 처리가 아직 구현되지 않음
        # 이 테스트는 RED 단계에서 실패해야 함
        
        # 잘못된 형식의 데이터 (name 필드 없음)
        invalid_data = [
            {
                "address": "주소만 있음"
                # name 필드 없음
            }
        ]
        
        # 현재 구현은 검증을 하지만, 에러 처리가 명확하지 않음
        # RED 단계: 이 테스트는 실패해야 함
        assert False, "잘못된 데이터 형식 처리 테스트는 아직 구현되지 않았습니다"
    
    def test_data_validation_failure_error_handling(self):
        """데이터 검증 실패 시 에러 처리 확인"""
        # RED 단계: 검증 실패 시 에러 처리가 아직 구현되지 않음
        
        invalid_restaurant = {
            # name 필드 없음
            "address": "주소"
        }
        
        # 검증 실패 확인
        is_valid = validate_restaurant_data(invalid_restaurant)
        assert is_valid is False
        
        # RED 단계: 검증 실패 시 적절한 에러 처리가 필요함
        # 현재는 단순히 False만 반환
        # 향후 예외 발생 또는 로깅 등이 필요할 수 있음
        assert False, "데이터 검증 실패 시 에러 처리 테스트는 아직 구현되지 않았습니다"

