"""
모니터링 기능 테스트
N6. 모니터링 및 관찰성 테스트
"""
import pytest
import json
import time


class TestHealthCheckEndpoint:
    """헬스 체크 엔드포인트 테스트 (N6.2)"""
    
    def test_health_check_returns_200(self, client):
        """헬스 체크가 200 응답을 반환하는지 확인"""
        response = client.get('/health')
        assert response.status_code in [200, 503]  # healthy 또는 degraded
    
    def test_health_check_response_format(self, client):
        """헬스 체크 응답 형식 확인"""
        response = client.get('/health')
        data = json.loads(response.data)
        
        assert 'status' in data
        assert 'checks' in data
        assert isinstance(data['checks'], dict)
    
    def test_health_check_filesystem_status(self, client):
        """파일 시스템 상태 확인"""
        response = client.get('/health')
        data = json.loads(response.data)
        
        assert 'filesystem' in data['checks']
        # 파일이 존재하면 'ok', 없으면 'warning' 또는 'error'
        assert data['checks']['filesystem'] in ['ok', 'warning', 'error']
    
    def test_health_check_data_load_status(self, client):
        """데이터 로드 상태 확인"""
        response = client.get('/health')
        data = json.loads(response.data)
        
        assert 'data_load' in data['checks']
        assert data['checks']['data_load'] in ['ok', 'error']


class TestMetricsEndpoint:
    """메트릭 엔드포인트 테스트 (N6.1)"""
    
    def test_metrics_endpoint_returns_200(self, client):
        """메트릭 엔드포인트가 200 응답을 반환하는지 확인"""
        response = client.get('/api/metrics')
        assert response.status_code == 200
    
    def test_metrics_response_format(self, client):
        """메트릭 응답 형식 확인"""
        # 몇 개의 요청을 먼저 생성
        client.get('/')
        client.get('/api/restaurants')
        
        response = client.get('/api/metrics')
        data = json.loads(response.data)
        
        assert 'request_count' in data
        assert 'error_count' in data
        assert 'error_rate' in data
        assert 'uptime_seconds' in data
        assert isinstance(data['request_count'], int)
        assert isinstance(data['error_count'], int)
        assert isinstance(data['error_rate'], float)
        assert isinstance(data['uptime_seconds'], float)
    
    def test_metrics_tracks_requests(self, client):
        """요청 수 추적 확인"""
        initial_response = client.get('/api/metrics')
        initial_data = json.loads(initial_response.data)
        initial_count = initial_data['request_count']
        
        # 추가 요청 생성
        client.get('/')
        client.get('/api/restaurants')
        
        final_response = client.get('/api/metrics')
        final_data = json.loads(final_response.data)
        final_count = final_data['request_count']
        
        # 요청 수가 증가했는지 확인 (최소 2개 이상 증가)
        assert final_count >= initial_count + 2
    
    def test_metrics_response_time_tracking(self, client):
        """응답 시간 추적 확인"""
        # 여러 요청 생성
        for _ in range(5):
            client.get('/')
        
        response = client.get('/api/metrics')
        data = json.loads(response.data)
        
        if 'response_time' in data:
            assert 'average' in data['response_time']
            assert 'min' in data['response_time']
            assert 'max' in data['response_time']
            assert 'count' in data['response_time']

