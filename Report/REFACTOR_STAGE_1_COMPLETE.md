# REFACTOR 단계 1단계 완료 리포트
## 코드스멜 분석 및 제거

**작성일**: 2025년 12월 19일  
**단계**: TDD REFACTOR - 1단계: 코드스멜 분석 및 정적 분석  
**상태**: ✅ 완료

---

## 📋 작업 개요

REFACTOR 단계의 1단계인 "코드스멜 분석 및 정적 분석"을 완료했습니다. 주요 코드스멜을 식별하고 제거하여 코드 품질을 향상시켰습니다.

---

## ✅ 완료된 작업

### 1.1 전역 변수 제거 ✅

#### 문제점
- `app.py`에서 `_restaurants_cache`, `_metrics` 전역 변수 사용
- 전역 상태 관리로 인한 테스트 어려움
- 상태 관리 복잡도 증가

#### 해결 방법
- **`RestaurantCache` 클래스 생성** (`utils/cache.py`)
  - 싱글톤 패턴으로 전역 상태 관리
  - `get_data()`, `clear_cache()`, `reload_cache()` 메서드 제공
  - 캐시 관리 로직 캡슐화

- **`MetricsCollector` 클래스 생성** (`utils/metrics.py`)
  - 싱글톤 패턴으로 메트릭 상태 관리
  - `increment_request()`, `increment_error()`, `add_response_time()` 메서드 제공
  - `get_metrics()`, `get_health_metrics()` 메서드로 메트릭 조회

#### 변경 사항
```python
# 이전 (전역 변수)
_restaurants_cache: list = []
_metrics: Dict[str, Any] = {...}

# 이후 (클래스 기반)
cache = get_cache()  # RestaurantCache 싱글톤
metrics = get_metrics()  # MetricsCollector 싱글톤
```

---

### 1.2 중복 코드 제거 ✅

#### 문제점
- `load_restaurants_data`와 `save_restaurants_data`에서 경로 검증 로직 중복
- 동일한 경로 정규화 로직이 두 함수에 반복

#### 해결 방법
- **`validate_and_normalize_path` 함수 생성** (`utils/file_utils.py`)
  - 파일 경로 검증 및 정규화 로직 통합
  - 테스트 환경을 고려한 절대 경로 허용 로직 포함
  - 재사용 가능한 공통 함수로 추출

#### 변경 사항
```python
# 이전 (중복 코드)
# load_restaurants_data와 save_restaurants_data에서 각각 경로 검증 로직 반복

# 이후 (통합)
normalized_path, _ = validate_and_normalize_path(file_path)
```

---

### 1.3 긴 함수 분리 ✅

#### 문제점
- `health_check` 함수가 파일 시스템 체크, 데이터 로드 체크, 메트릭 추가를 모두 수행
- 단일 책임 원칙 위반

#### 해결 방법
- **`_check_filesystem_health` 함수 추가**
  - 파일 시스템 접근 가능 여부 확인만 담당
  - (상태 메시지, 건강 여부) 튜플 반환

- **`_check_data_load_health` 함수 추가**
  - 데이터 로드 가능 여부 확인만 담당
  - (상태 메시지, 건강 여부, 데이터 개수) 튜플 반환

- **`health_check` 함수 단순화**
  - 각 헬퍼 함수를 호출하여 결과를 조합
  - 메트릭 정보는 `metrics.get_health_metrics()` 사용

#### 변경 사항
```python
# 이전 (긴 함수)
def health_check():
    # 파일 시스템 체크 로직
    # 데이터 로드 체크 로직
    # 메트릭 추가 로직
    # 모두 한 함수에...

# 이후 (분리된 함수)
def _check_filesystem_health() -> Tuple[str, bool]:
    ...

def _check_data_load_health() -> Tuple[str, bool, int]:
    ...

def health_check():
    fs_status, fs_healthy = _check_filesystem_health()
    data_status, data_healthy, data_count = _check_data_load_health()
    ...
```

---

### 1.4 매직 넘버/문자열 제거 ✅

#### 문제점
- 하드코딩된 값들 (`100`, `'data/restaurants.json'` 등)
- 변경 시 여러 곳을 수정해야 함
- 오류 발생 가능성

#### 해결 방법
- **`utils/constants.py` 모듈 생성**
  - 모든 상수를 한 곳에서 관리
  - 파일 경로, 메트릭 설정, 에러 메시지, 에러 코드 등 상수화

#### 주요 상수
```python
# 파일 경로
DEFAULT_DATA_PATH = 'data/restaurants.json'
DEFAULT_IMAGES_DIR = 'images'
DEFAULT_LOGS_DIR = 'logs'

# 메트릭 설정
MAX_RESPONSE_TIMES = 100

# 에러 메시지
ERROR_MESSAGES = {
    'PAGE_NOT_FOUND': '페이지를 찾을 수 없습니다.',
    'SERVER_ERROR': '서버 오류가 발생했습니다.',
    ...
}

# 에러 코드
ERROR_CODES = {
    'BAD_REQUEST': 'ERR_BAD_REQUEST',
    'DATA_LOAD_FAILED': 'ERR_DATA_LOAD_FAILED',
    ...
}
```

#### 변경 사항
```python
# 이전 (매직 넘버/문자열)
if len(_metrics['response_times']) > 100:
    ...
file_path = 'data/restaurants.json'
raise BadRequest("안전하지 않은 파일 경로입니다.")

# 이후 (상수 사용)
if len(self._response_times) > MAX_RESPONSE_TIMES:
    ...
file_path = DEFAULT_DATA_PATH
raise BadRequest(ERROR_MESSAGES['UNSAFE_FILE_PATH'])
```

---

### 1.5 네이밍 개선 ✅

#### 개선 사항
- 일관된 네이밍 컨벤션 적용
  - 클래스명: PascalCase (`RestaurantCache`, `MetricsCollector`)
  - 함수명: snake_case (`get_data`, `increment_request`)
  - 상수명: UPPER_SNAKE_CASE (`DEFAULT_DATA_PATH`, `MAX_RESPONSE_TIMES`)

- 모호한 변수명 개선
  - `_restaurants_cache` → `cache` (RestaurantCache 인스턴스)
  - `_metrics` → `metrics` (MetricsCollector 인스턴스)

- 함수명과 역할 일치 확인
  - 모든 함수명이 역할을 명확히 표현
  - 헬퍼 함수는 `_` 접두사로 내부 함수임을 명시

---

## 📁 생성된 파일

### 새로운 모듈
1. **`utils/constants.py`**
   - 모든 상수 정의
   - 파일 경로, 메트릭 설정, 에러 메시지, 에러 코드 등

2. **`utils/cache.py`**
   - `RestaurantCache` 클래스
   - 매장 데이터 캐싱 관리

3. **`utils/metrics.py`**
   - `MetricsCollector` 클래스
   - 메트릭 수집 및 관리

4. **`utils/file_utils.py`**
   - `validate_and_normalize_path` 함수
   - 파일 경로 검증 및 정규화 공통 로직

---

## 🔄 수정된 파일

### `app.py`
- 전역 변수 제거 (`_restaurants_cache`, `_metrics`)
- `RestaurantCache`, `MetricsCollector` 싱글톤 사용
- 상수 사용 (`DEFAULT_DATA_PATH`, `ERROR_MESSAGES`, `ERROR_CODES` 등)
- `health_check` 함수 분리 (`_check_filesystem_health`, `_check_data_load_health`)
- 불필요한 import 제거

### `utils/data_loader.py`
- `validate_and_normalize_path` 함수 사용 (중복 코드 제거)
- `DEFAULT_DATA_PATH` 상수 사용

---

## 📊 개선 효과

### 코드 품질 향상
- ✅ 전역 변수 제거로 테스트 용이성 향상
- ✅ 중복 코드 제거로 유지보수성 향상
- ✅ 긴 함수 분리로 가독성 향상
- ✅ 매직 넘버/문자열 제거로 변경 용이성 향상
- ✅ 일관된 네이밍으로 가독성 향상

### 아키텍처 개선
- ✅ 싱글톤 패턴으로 전역 상태 관리 개선
- ✅ 단일 책임 원칙 준수 (각 함수가 하나의 책임만 수행)
- ✅ 모듈화로 재사용성 향상

---

## 🧪 테스트 상태

### Import 테스트
- ✅ 모든 모듈 import 성공
- ✅ 싱글톤 패턴 정상 작동 확인

### 다음 단계
- 전체 테스트 실행 및 검증 필요
- 정적 분석 도구 실행 (mypy, pylint/flake8)

---

## 📝 다음 작업

### 1.2 정적 분석 도구 실행
- [ ] mypy 타입 체크
- [ ] pylint/flake8 코드 품질 검사
- [ ] 순환 복잡도 분석

### 2단계: SOLID 원칙 적용
- [ ] Single Responsibility Principle
- [ ] Open/Closed Principle
- [ ] Dependency Inversion Principle

---

## ✅ 체크리스트

- [x] 전역 변수 제거
- [x] 중복 코드 제거
- [x] 긴 함수 분리
- [x] 매직 넘버/문자열 제거
- [x] 네이밍 개선
- [ ] 정적 분석 도구 실행 (다음 단계)
- [ ] SOLID 원칙 적용 (다음 단계)

---

**리포트 작성일**: 2025년 12월 19일  
**작성자**: 프로젝트 팀  
**다음 업데이트**: 정적 분석 도구 실행 후

