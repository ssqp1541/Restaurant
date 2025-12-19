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
        from utils.data_loader import validate_restaurants_data_list
        
        # 잘못된 형식의 데이터 (name 필드 없음)
        invalid_data = [
            {
                "address": "주소만 있음"
                # name 필드 없음
            }
        ]
        
        # 데이터 검증 수행
        is_valid, errors = validate_restaurants_data_list(invalid_data)
        
        # 검증 실패 확인
        assert is_valid is False
        assert len(errors) > 0
        # 에러 메시지에 필수 필드 누락 정보가 포함되어야 함
        assert any('name' in error.lower() or '필수' in error for error in errors)
    
    def test_data_validation_failure_error_handling(self):
        """데이터 검증 실패 시 에러 처리 확인"""
        from utils.data_loader import validate_restaurant_data_with_error
        
        invalid_restaurant = {
            # name 필드 없음
            "address": "주소"
        }
        
        # 검증 실패 확인
        is_valid = validate_restaurant_data(invalid_restaurant)
        assert is_valid is False
        
        # 상세한 에러 메시지 확인
        is_valid_with_error, error_msg = validate_restaurant_data_with_error(invalid_restaurant)
        assert is_valid_with_error is False
        assert error_msg is not None
        assert len(error_msg) > 0
        # 에러 메시지에 필수 필드 정보가 포함되어야 함
        assert 'name' in error_msg.lower() or '필수' in error_msg

