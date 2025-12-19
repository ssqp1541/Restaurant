"""
엣지 케이스 테스트
F5. 엣지 케이스 처리 테스트
"""
import pytest
import json
import tempfile
import os
from utils.data_loader import (
    load_restaurants_data,
    save_restaurants_data,
    validate_restaurant_data,
    add_restaurant,
    get_restaurant_by_name
)


class TestEmptyDataHandling:
    """F5.1: 빈 데이터 처리 테스트"""
    
    def test_load_empty_json_array(self):
        """빈 JSON 배열 처리"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_path = f.name
        
        try:
            result = load_restaurants_data(temp_path)
            assert result == []
            assert isinstance(result, list)
        finally:
            os.unlink(temp_path)
    
    def test_load_empty_json_object(self):
        """빈 JSON 객체 처리 (리스트가 아님)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({}, f)
            temp_path = f.name
        
        try:
            result = load_restaurants_data(temp_path)
            # 객체는 리스트가 아니므로 빈 리스트 반환
            assert result == []
        finally:
            os.unlink(temp_path)
    
    def test_save_empty_array(self):
        """빈 배열 저장"""
        empty_data = []
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            result = save_restaurants_data(empty_data, temp_path)
            assert result is True
            
            # 저장된 데이터 확인
            loaded = load_restaurants_data(temp_path)
            assert loaded == []
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_validate_empty_restaurant_object(self):
        """빈 매장 객체 처리"""
        empty_restaurant = {}
        result = validate_restaurant_data(empty_restaurant)
        # name 필드가 없으므로 False
        assert result is False


class TestLargeDataHandling:
    """F5.2: 매우 큰 데이터 처리 테스트"""
    
    def test_load_large_json_file(self):
        """대용량 JSON 파일 처리"""
        # 1000개의 매장 데이터 생성
        large_data = [
            {
                "name": f"매장{i}",
                "address": f"주소{i}" * 10,  # 긴 주소
                "blogLinks": [{"url": f"https://example.com/{i}", "title": f"제목{i}"}],
                "menuImages": [f"image{i}.jpg"],
                "reviews": [{"text": f"후기{i}" * 20, "rating": 5}]
            }
            for i in range(1000)
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(large_data, f)
            temp_path = f.name
        
        try:
            result = load_restaurants_data(temp_path)
            assert len(result) == 1000
            assert result[0]['name'] == "매장0"
            assert result[999]['name'] == "매장999"
        finally:
            os.unlink(temp_path)
    
    def test_save_large_data(self):
        """대용량 데이터 저장"""
        large_data = [{"name": f"매장{i}"} for i in range(500)]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            result = save_restaurants_data(large_data, temp_path)
            assert result is True
            
            # 저장된 데이터 확인
            loaded = load_restaurants_data(temp_path)
            assert len(loaded) == 500
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestSpecialCharactersHandling:
    """F5.3: 특수 문자 처리 테스트"""
    
    def test_load_json_with_unicode(self):
        """유니코드 문자가 포함된 JSON 파일"""
        unicode_data = [
            {
                "name": "맛집 🍕",
                "address": "서울시 강남구 🏙️",
                "blogLinks": [{"url": "https://example.com", "title": "제목 🎉"}],
                "reviews": [{"text": "좋아요! 👍", "rating": 5}]
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(unicode_data, f, ensure_ascii=False)
            temp_path = f.name
        
        try:
            result = load_restaurants_data(temp_path)
            assert len(result) == 1
            assert result[0]['name'] == "맛집 🍕"
            assert "🍕" in result[0]['name']
        finally:
            os.unlink(temp_path)
    
    def test_save_json_with_unicode(self):
        """유니코드 문자가 포함된 데이터 저장"""
        unicode_data = [
            {
                "name": "레스토랑 🍔",
                "address": "부산시 해운대구 🌊"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            result = save_restaurants_data(unicode_data, temp_path)
            assert result is True
            
            # 저장된 데이터 확인
            loaded = load_restaurants_data(temp_path)
            assert loaded[0]['name'] == "레스토랑 🍔"
            assert "🍔" in loaded[0]['name']
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_special_characters_in_name(self):
        """이름에 특수 문자 포함"""
        special_names = [
            "맛집&카페",
            "레스토랑-서울",
            "식당(본점)",
            "카페'스타일'",
            '레스토랑"프리미엄"',
            "식당/분점",
            "카페\\백슬래시"
        ]
        
        for name in special_names:
            restaurant = {"name": name}
            assert validate_restaurant_data(restaurant) is True
    
    def test_escape_characters_in_data(self):
        """이스케이프 문자가 포함된 데이터"""
        escape_data = {
            "name": "테스트\n매장",
            "address": "주소\t탭",
            "blogLinks": [{"url": "https://example.com", "title": "제목\"따옴표\""}]
        }
        
        assert validate_restaurant_data(escape_data) is True
        
        # 저장 및 로드 테스트
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            save_restaurants_data([escape_data], temp_path)
            loaded = load_restaurants_data(temp_path)
            assert loaded[0]['name'] == "테스트\n매장"
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestDuplicateNameHandling:
    """F5.4: 중복 매장명 처리 테스트"""
    
    def test_detect_duplicate_names(self):
        """중복 매장명 감지"""
        data = [
            {"name": "기존 매장"},
            {"name": "다른 매장"}
        ]
        
        # 중복 추가 시도
        duplicate = {"name": "기존 매장"}
        result = add_restaurant(data, duplicate)
        
        # 현재 구현은 중복을 허용함
        assert result is True
        assert len(data) == 3
        
        # 중복 확인
        names = [r['name'] for r in data]
        assert names.count("기존 매장") == 2
    
    def test_multiple_duplicates(self):
        """여러 개의 중복 추가"""
        data = [{"name": "원본 매장"}]
        
        for i in range(5):
            duplicate = {"name": "원본 매장"}
            add_restaurant(data, duplicate)
        
        # 총 6개 (원본 1개 + 중복 5개)
        assert len(data) == 6
        names = [r['name'] for r in data]
        assert all(name == "원본 매장" for name in names)
    
    def test_get_restaurant_with_duplicates(self):
        """중복이 있을 때 검색"""
        data = [
            {"name": "중복 매장", "id": 1},
            {"name": "다른 매장"},
            {"name": "중복 매장", "id": 2}
        ]
        
        # 첫 번째 매칭되는 항목 반환
        result = get_restaurant_by_name(data, "중복 매장")
        assert result is not None
        assert result['name'] == "중복 매장"
        # 첫 번째 항목의 id 반환
        assert result['id'] == 1

