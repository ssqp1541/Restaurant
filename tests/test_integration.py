"""
통합 테스트
F6. 통합 테스트 강화
"""
import pytest
import json
import os
import tempfile
from pathlib import Path
from utils.data_loader import (
    load_restaurants_data,
    validate_restaurant_data,
    validate_restaurants_data_list,
    save_restaurants_data
)


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
    
    def test_data_load_failure_scenario(self, client):
        """F6.2: 데이터 로드 실패 시나리오 테스트"""
        # 존재하지 않는 파일 경로로 데이터 로드 시도
        restaurants = load_restaurants_data('data/nonexistent.json')
        
        # 빈 리스트 반환 확인
        assert restaurants == []
        
        # Flask 앱에서도 빈 데이터 처리 확인
        response = client.get('/')
        assert response.status_code == 200
    
    def test_data_validation_failure_scenario(self, client):
        """F6.2: 데이터 검증 실패 시나리오 테스트"""
        # 잘못된 형식의 데이터
        invalid_data = [
            {"address": "주소만 있음"},  # name 필드 없음
            {"name": "유효한 매장"}  # 유효한 데이터
        ]
        
        # 검증 수행
        is_valid, errors = validate_restaurants_data_list(invalid_data)
        assert is_valid is False
        assert len(errors) > 0


class TestRealDataFileIntegration:
    """F6.1: 실제 데이터 파일을 사용한 통합 테스트"""
    
    def test_real_data_file_structure(self):
        """실제 restaurants.json 파일 구조 확인"""
        restaurants = load_restaurants_data('data/restaurants.json')
        
        # 파일이 존재하고 로드 가능한지 확인
        assert isinstance(restaurants, list)
        
        if len(restaurants) > 0:
            # 첫 번째 매장의 구조 확인
            first_restaurant = restaurants[0]
            assert 'name' in first_restaurant
            assert isinstance(first_restaurant.get('blogLinks', []), list)
            assert isinstance(first_restaurant.get('menuImages', []), list)
            assert isinstance(first_restaurant.get('reviews', []), list)
    
    def test_real_data_file_validation(self):
        """실제 데이터 파일의 모든 매장 검증"""
        restaurants = load_restaurants_data('data/restaurants.json')
        
        # 모든 매장이 유효한지 확인
        for restaurant in restaurants:
            assert validate_restaurant_data(restaurant), f"매장 '{restaurant.get('name', 'Unknown')}' 검증 실패"
    
    def test_real_data_file_with_flask_app(self, client):
        """실제 데이터 파일과 Flask 앱 연동 테스트"""
        # 실제 데이터 로드
        restaurants = load_restaurants_data('data/restaurants.json')
        
        # Flask 앱을 통해 API 호출
        response = client.get('/api/restaurants')
        assert response.status_code == 200
        
        api_data = json.loads(response.data)
        
        # 데이터 일치 확인
        assert len(restaurants) == len(api_data)
        
        # 각 매장의 이름이 일치하는지 확인
        restaurant_names = [r['name'] for r in restaurants]
        api_names = [r['name'] for r in api_data]
        assert restaurant_names == api_names
    
    def test_real_data_file_save_and_load_cycle(self):
        """실제 데이터 파일 저장 및 로드 사이클 테스트"""
        # 원본 데이터 로드
        original_data = load_restaurants_data('data/restaurants.json')
        
        # 임시 파일에 저장
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            # 저장
            save_result = save_restaurants_data(original_data, temp_path)
            assert save_result is True
            
            # 다시 로드
            loaded_data = load_restaurants_data(temp_path)
            
            # 데이터 일치 확인
            assert len(original_data) == len(loaded_data)
            if len(original_data) > 0:
                assert original_data[0]['name'] == loaded_data[0]['name']
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


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

