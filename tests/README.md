# 테스트 가이드

## 테스트 실행 방법

### 전체 테스트 실행
```bash
# 가상 환경 활성화 후
pytest

# 또는 상세 출력
pytest -v

# 커버리지 포함
pytest --cov=. --cov-report=term-missing
```

### 특정 테스트 실행
```bash
# 특정 테스트 파일
pytest tests/test_app.py

# 특정 테스트 클래스
pytest tests/test_app.py::TestMainPageRoute

# 특정 테스트 함수
pytest tests/test_app.py::TestMainPageRoute::test_index_returns_200
```

## 테스트 구조

- `tests/conftest.py`: pytest 설정 및 픽스처 정의
- `tests/test_app.py`: Flask 애플리케이션 테스트
- `pytest.ini`: pytest 설정 파일

## TDD RED 단계 상태

**현재 상태**: RED 단계 완료 ✅

- **총 테스트**: 10개
- **통과**: 9개
- **실패**: 1개 (의도적 - 500 에러 페이지 테스트)
- **커버리지**: 63%

### 실패하는 테스트 (RED 단계 목표 달성)
- `test_500_error_page`: 500 에러 페이지 테스트 (아직 구현되지 않음)

## 다음 단계

1. **GREEN 단계**: 실패하는 테스트를 통과시키는 최소한의 코드 작성
2. **REFACTOR 단계**: 코드 개선 및 리팩토링

