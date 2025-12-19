# REFACTOR 단계 가이드

**작성일**: 2025년 12월 19일  
**단계**: TDD REFACTOR (코드 개선 및 리팩토링)

---

## 📋 개요

REFACTOR 단계는 GREEN 단계에서 작성한 코드를 개선하고 리팩토링하는 단계입니다. 테스트는 모두 통과하지만, 코드 품질, 유지보수성, 확장성을 향상시키는 것이 목표입니다.

---

## 🔍 현재 코드 분석

### 발견된 코드스멜

#### 1. 전역 변수 사용
- **위치**: `app.py`
- **문제**: `_restaurants_cache`, `_metrics` 전역 변수 사용
- **영향**: 테스트 어려움, 상태 관리 복잡도 증가
- **해결**: 클래스 기반 구조 또는 의존성 주입

#### 2. 중복 코드
- **위치**: `utils/data_loader.py`
- **문제**: `load_restaurants_data`와 `save_restaurants_data`에서 경로 검증 로직 중복
- **영향**: 유지보수 어려움, 버그 발생 가능성
- **해결**: 공통 함수 추출

#### 3. 긴 함수
- **위치**: `app.py::health_check`, `utils/data_loader.py::validate_restaurant_data_with_error`
- **문제**: 함수가 여러 책임을 가짐
- **영향**: 가독성 저하, 테스트 어려움
- **해결**: 함수 분리

#### 4. 매직 넘버/문자열
- **위치**: 여러 파일
- **문제**: 하드코딩된 값들 (`100`, `'data/restaurants.json'` 등)
- **영향**: 변경 어려움, 오류 발생 가능성
- **해결**: 상수 정의

### SOLID 원칙 위반 사항

#### Single Responsibility Principle (SRP)
- `health_check` 함수가 파일 시스템 체크, 데이터 로드 체크, 메트릭 추가를 모두 수행
- `validate_restaurant_data_with_error` 함수가 모든 필드 검증을 수행

#### Dependency Inversion Principle (DIP)
- 전역 변수에 직접 의존
- 하드코딩된 파일 경로 의존

---

## 🎯 리팩토링 전략

### 단계별 접근

1. **코드스멜 제거** (낮은 위험)
2. **SOLID 원칙 적용** (중간 위험)
3. **아키텍처 개선** (높은 위험)
4. **성능 최적화** (검증 필요)

### 리팩토링 원칙

1. **작은 단계로 진행**: 한 번에 하나씩 리팩토링
2. **테스트 유지**: 각 단계마다 테스트 통과 확인
3. **기능 보존**: 동작 변경 없이 구조만 개선
4. **점진적 개선**: 완벽을 추구하지 않고 점진적으로 개선

---

## 📚 참고 자료

### 코드스멜 패턴
- Long Method (긴 메서드)
- Large Class (큰 클래스)
- Duplicate Code (중복 코드)
- Feature Envy (기능 질투)
- Data Clumps (데이터 덩어리)

### SOLID 원칙
- **S**ingle Responsibility: 단일 책임 원칙
- **O**pen/Closed: 개방-폐쇄 원칙
- **L**iskov Substitution: 리스코프 치환 원칙
- **I**nterface Segregation: 인터페이스 분리 원칙
- **D**ependency Inversion: 의존성 역전 원칙

### 리팩토링 기법
- Extract Method (메서드 추출)
- Extract Class (클래스 추출)
- Move Method (메서드 이동)
- Replace Temp with Query (임시 변수를 쿼리로 교체)
- Introduce Parameter Object (매개변수 객체 도입)

---

## 🛠️ 도구

### 정적 분석 도구
- **mypy**: 타입 체크
- **pylint**: 코드 품질 검사
- **flake8**: 스타일 가이드 검사
- **black**: 코드 포맷팅

### 프로파일링 도구
- **cProfile**: 성능 프로파일링
- **memory_profiler**: 메모리 사용량 분석

---

## ✅ 체크리스트

각 리팩토링 작업 후 확인:

- [ ] 모든 테스트 통과
- [ ] 커버리지 유지 (90% 이상)
- [ ] 타입 체크 통과
- [ ] 정적 분석 경고 없음
- [ ] 성능 저하 없음
- [ ] 문서 업데이트

---

**작성자**: AI Assistant  
**최종 업데이트**: 2025년 12월 19일

