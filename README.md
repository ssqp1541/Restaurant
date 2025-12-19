# 천안시 맛집 안내 웹페이지

2025년 충청남도 천안시의 맛집을 소개하는 웹사이트입니다.

## 📌 프로젝트 개요

천안시의 추천 맛집 정보를 제공하며, 각 매장의 대표 메뉴, Naver 블로그 리뷰, 고객 후기를 한눈에 볼 수 있습니다.

## 🚀 시작하기

### 필수 요구사항
- Python 3.8 이상 (권장: Python 3.10 이상)
- pip (Python 패키지 관리자)
- Git (선택사항, 프로젝트 클론 시 필요)

### 설치 방법

1. **프로젝트 클론 또는 다운로드**
   ```bash
   # Git을 사용하는 경우
   git clone https://github.com/ssqp1541/Restaurant.git
   cd Restaurant
   
   # 또는 ZIP 파일 다운로드 후 압축 해제
   ```

2. **가상 환경 생성 (권장)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **필요한 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **Flask 서버 실행**
   ```bash
   python app.py
   ```

5. **웹 브라우저에서 접속**
   - http://localhost:5000 으로 접속
   - 서버가 정상적으로 실행되면 콘솔에 다음 메시지가 표시됩니다:
     ```
     ==================================================
     천안시 맛집 안내 웹사이트
     ==================================================
     서버 시작: http://localhost:5000
     종료하려면 Ctrl+C를 누르세요.
     ==================================================
     ```

### 실행 방법 상세

#### 개발 서버 실행
```bash
# 기본 실행 (개발 모드)
python app.py

# 또는 Flask 명령어 사용
flask run

# 특정 포트로 실행
flask run --port 8080

# 외부 접속 허용
flask run --host 0.0.0.0
```

#### 테스트 실행

**전체 테스트 실행**
```bash
# 기본 실행
pytest

# 상세 출력
pytest -v

# 특정 테스트 파일 실행
pytest tests/test_app.py
pytest tests/test_data_loader.py
pytest tests/test_integration.py

# 특정 테스트 클래스 실행
pytest tests/test_app.py::TestMainPageRoute

# 특정 테스트 함수 실행
pytest tests/test_app.py::TestMainPageRoute::test_index_returns_200
```

**커버리지 포함 테스트 실행**
```bash
# 터미널에 커버리지 출력
pytest --cov=. --cov-report=term-missing

# HTML 리포트 생성
pytest --cov=. --cov-report=html

# HTML 리포트 확인 (브라우저에서)
# htmlcov/index.html 파일 열기

# 최소 커버리지 요구사항 설정 (80%)
pytest --cov=. --cov-fail-under=80
```

**빠른 테스트 실행**
```bash
# 간단한 출력
pytest -q

# 실패한 테스트만 재실행
pytest --lf

# 실패한 테스트부터 실행
pytest --ff
```

#### API 엔드포인트 테스트

**메인 페이지**
```bash
# 브라우저에서 접속
http://localhost:5000

# 또는 curl 사용
curl http://localhost:5000
```

**REST API**
```bash
# 매장 데이터 조회
curl http://localhost:5000/api/restaurants

# JSON 형식으로 보기
curl http://localhost:5000/api/restaurants | python -m json.tool
```

**헬스 체크**
```bash
# 시스템 상태 확인
curl http://localhost:5000/health

# JSON 형식으로 보기
curl http://localhost:5000/health | python -m json.tool
```

**메트릭 정보**
```bash
# 메트릭 정보 조회
curl http://localhost:5000/api/metrics

# JSON 형식으로 보기
curl http://localhost:5000/api/metrics | python -m json.tool
```

### 문제 해결

#### 포트가 이미 사용 중인 경우
```bash
# 다른 포트로 실행
python app.py
# 또는 app.py 파일에서 port=5000을 다른 포트로 변경
```

#### 가상 환경 활성화 오류 (Windows)
```bash
# PowerShell 실행 정책 문제인 경우
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 또는 직접 Python 실행
venv\Scripts\python.exe app.py
```

#### 패키지 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 가상 환경 재생성
rm -rf venv  # 또는 Windows: rmdir /s venv
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

#### 테스트 실행 오류
```bash
# pytest가 설치되지 않은 경우
pip install pytest pytest-flask pytest-cov

# 테스트 경로 문제
# 프로젝트 루트 디렉토리에서 실행 확인
cd C:\DEV\Restaurant  # 또는 프로젝트 경로
pytest
```

### 개발 환경 설정

#### IDE 설정 (VS Code)
1. Python 확장 프로그램 설치
2. `.vscode/settings.json` 파일 생성 (선택사항):
   ```json
   {
     "python.testing.pytestEnabled": true,
     "python.testing.unittestEnabled": false,
     "python.linting.enabled": true,
     "python.linting.pylintEnabled": false,
     "python.linting.flake8Enabled": true
   }
   ```

#### 타입 체크 (선택사항)
```bash
# mypy를 사용한 타입 체크
mypy .

# 특정 파일만 체크
mypy app.py utils/data_loader.py
```

### 프로덕션 배포

#### Gunicorn 사용 (Linux/macOS)
```bash
# Gunicorn 설치
pip install gunicorn

# 실행
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 환경 변수 설정
```bash
# .env 파일 생성 (선택사항)
FLASK_ENV=production
FLASK_DEBUG=False
```

### 로그 확인

```bash
# 로그 파일 위치
logs/app.log

# 실시간 로그 확인 (Linux/macOS)
tail -f logs/app.log

# Windows PowerShell
Get-Content logs/app.log -Wait
```

## 📁 프로젝트 구조

```
Restaurant/
├── app.py                    # Flask 메인 애플리케이션
├── requirements.txt          # Python 패키지 의존성
├── .gitignore               # Git 무시 파일 목록
│
├── templates/               # Jinja2 템플릿 폴더
│   ├── index.html           # 메인 HTML 템플릿
│   └── error.html           # 에러 페이지 템플릿
│
├── static/                  # 정적 파일 폴더
│   ├── css/
│   │   └── main.css        # 스타일시트
│   └── js/
│       └── main.js         # JavaScript (모달 기능)
│
├── utils/                   # Python 유틸리티 모듈
│   ├── __init__.py         # 패키지 초기화 파일
│   └── data_loader.py      # 데이터 로딩 및 검증 유틸리티
│
├── data/                    # 데이터 파일 폴더
│   └── restaurants.json    # 매장 데이터 (JSON 형식)
│
├── images/                  # 이미지 파일 폴더
│   └── restaurants/        # 매장별 메뉴 이미지
│       ├── restaurant1/     # 매장1 메뉴 이미지 (menu1.jpg, menu2.jpg, menu3.jpg)
│       ├── restaurant2/     # 매장2 메뉴 이미지
│       └── restaurant3/     # 매장3 메뉴 이미지
│
├── README.md                # 프로젝트 설명서 (현재 파일)
├── PROJECT_GUIDE.md         # 프로젝트 개발 가이드
├── PRD.md                   # 제품 요구사항 문서 (Product Requirements Document)
└── QUICK_START.md           # 빠른 시작 가이드
```

### 주요 디렉토리 설명

#### 백엔드 파일
- **`app.py`**: Flask 웹 애플리케이션의 진입점
  - 메인 페이지 라우트 (`/`)
  - REST API 엔드포인트 (`/api/restaurants`)
  - 이미지 서빙 라우트 (`/images/<filename>`)
  - 에러 핸들러 (404, 500)

#### 템플릿 및 정적 파일
- **`templates/`**: Jinja2 템플릿 파일
  - `index.html`: 메인 페이지 템플릿 (서버 사이드 렌더링)
  - `error.html`: 에러 페이지 템플릿
- **`static/`**: 정적 파일 (Flask가 자동으로 서빙)
  - `css/main.css`: 스타일시트
  - `js/main.js`: 클라이언트 사이드 JavaScript (이미지 라이트박스)

#### 유틸리티 및 데이터
- **`utils/`**: Python 유틸리티 모듈
  - `data_loader.py`: 데이터 로딩, 저장, 검증 함수
  - `__init__.py`: 패키지 초기화 파일
- **`data/`**: JSON 형식의 매장 데이터
  - `restaurants.json`: 모든 매장 정보 저장
- **`images/`**: 매장별 메뉴 이미지
  - `restaurants/[매장명]/`: 매장별 폴더로 구분
  - 각 매장당 3개의 메뉴 이미지 (menu1.jpg, menu2.jpg, menu3.jpg)

#### 문서 파일
- **`README.md`**: 프로젝트 개요 및 설치 가이드
- **`PROJECT_GUIDE.md`**: 단계별 개발 가이드 및 주의사항
- **`PRD.md`**: 제품 요구사항 문서
- **`QUICK_START.md`**: 빠른 시작 가이드

## 📊 데이터 구조

### JSON 스키마

각 매장은 다음 정보를 포함하는 JSON 객체입니다:

```json
{
  "name": "매장명 (필수)",
  "address": "주소 (선택)",
  "phone": "전화번호 (선택)",
  "hours": "영업시간 (선택)",
  "blogLinks": [
    {
      "url": "Naver 블로그 URL",
      "title": "블로그 제목"
    }
  ],
  "menuImages": [
    "images/restaurants/매장명/menu1.jpg",
    "images/restaurants/매장명/menu2.jpg",
    "images/restaurants/매장명/menu3.jpg"
  ],
  "reviews": [
    {
      "text": "고객 후기 텍스트",
      "rating": 5
    }
  ]
}
```

### 필드 설명

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `name` | string | ✅ | 매장명 |
| `address` | string | ❌ | 매장 주소 |
| `phone` | string | ❌ | 전화번호 |
| `hours` | string | ❌ | 영업시간 |
| `blogLinks` | array | ❌ | Naver 블로그 링크 배열 (최대 3개 권장) |
| `blogLinks[].url` | string | ✅ | 블로그 URL |
| `blogLinks[].title` | string | ❌ | 블로그 제목 |
| `menuImages` | array | ❌ | 메뉴 이미지 경로 배열 (3개 권장) |
| `reviews` | array | ❌ | 고객 후기 배열 (3개 권장) |
| `reviews[].text` | string | ✅ | 후기 내용 |
| `reviews[].rating` | number | ❌ | 평점 (1-5) |

### 데이터 위치

- **파일 경로**: `data/restaurants.json`
- **형식**: JSON 배열 (매장 객체들의 리스트)
- **인코딩**: UTF-8
- **유효성 검사**: `utils/data_loader.py`의 `validate_restaurant_data()` 함수 사용

## 📚 프로젝트 문서

프로젝트 관련 상세 문서는 다음을 참고하세요:

- **[PRD.md](./PRD.md)**: 제품 요구사항 문서 (Product Requirements Document)
  - 제품 개요 및 목표
  - 기능 요구사항 및 우선순위
  - 비기능 요구사항 (성능, 호환성, 접근성 등)
  - 사용자 스토리 및 수용 기준
  - 기술 스택 및 제약사항
  - 성공 지표 및 일정

- **[PROJECT_GUIDE.md](./PROJECT_GUIDE.md)**: 프로젝트 개발 가이드
  - 단계별 개발 절차
  - 기술 스택 상세 설명
  - 주의사항 및 베스트 프랙티스

- **[QUICK_START.md](./QUICK_START.md)**: 빠른 시작 가이드
  - 설치 및 실행 방법
  - 문제 해결 가이드

## ✅ To-Do List

프로젝트 진행 상황을 추적하기 위한 체크리스트입니다. 자세한 내용은 [PROJECT_GUIDE.md](./PROJECT_GUIDE.md)를 참고하세요.

### 1단계: 프로젝트 구조 설정 _ 작업완료
- Python 가상 환경 생성
- Flask 및 필요한 패키지 설치
- 프로젝트 폴더 구조 생성 (templates, static, utils 등)
- 이미지 저장 폴더 생성 (`images/`)

### 2단계: 데이터 수집 및 준비
- [ ] 천안시 맛집 리스트 선정
- [ ] 각 매장별 Naver 블로그 3개 수집
- [ ] 대표 메뉴 이미지 3개 수집 (저작권 확인 필수)
- [ ] 고객 후기 3개 수집
- [ ] 데이터를 JSON 형식으로 구조화

### 3단계: 웹페이지 디자인
- [x] 반응형 레이아웃 설계
- [x] 매장 카드 디자인
- [x] 이미지 갤러리 디자인
- [x] 후기 섹션 디자인
- [ ] 네비게이션 메뉴 설계

### 4단계: Flask 애플리케이션 및 템플릿 작성
- [x] Flask 앱 구조 작성 (`app.py`)
- [x] Jinja2 템플릿 작성 (`templates/index.html`)
- [x] 메타 태그 설정 (SEO, 반응형)
- [x] 매장 정보 섹션 구조화
- [x] 블로그 링크, 이미지, 후기 영역 마크업

### 5단계: CSS 스타일링
- [x] 모던한 UI 디자인 적용
- [x] 반응형 디자인 구현 (모바일, 태블릿, 데스크톱)
- [x] 애니메이션 효과 추가
- [x] 색상 테마 설정

### 6단계: Python 백엔드 및 JavaScript 기능 구현
- [x] Python 데이터 로더 유틸리티 작성 (`utils/data_loader.py`)
- [x] Flask 라우트 및 API 엔드포인트 구현
- [x] JavaScript 이미지 갤러리 기능 (라이트박스 등)
- [ ] 필터링/검색 기능 (선택사항)
- [ ] 스크롤 애니메이션

### 7단계: 데이터 통합 및 Python 스크립트 활용
- [ ] JSON 파일에 매장 데이터 입력
- [ ] Python 유틸리티를 사용한 데이터 검증
- [ ] 이미지 파일 경로 연결
- [ ] 블로그 링크 연결
- [ ] 후기 데이터 입력

### TDD 단계: RED (실패하는 테스트 작성)
TDD(Test-Driven Development)의 첫 번째 단계로, 실패하는 테스트를 먼저 작성합니다.

#### 데이터 로더 유틸리티 테스트 (RED) 
- [ ] `load_restaurants_data()` 함수 테스트
  - [ ] 정상적인 JSON 파일 로드 확인
  - [ ] 존재하지 않는 파일 처리 확인
  - [ ] 잘못된 JSON 형식 처리 확인
  - [ ] 빈 파일 처리 확인
- [ ] `save_restaurants_data()` 함수 테스트
  - [ ] 데이터 저장 성공 확인
  - [ ] 저장된 데이터 검증 확인
  - [ ] 권한 오류 처리 확인
- [ ] `validate_restaurant_data()` 함수 테스트
  - [ ] 필수 필드(name) 검증 확인
  - [ ] blogLinks 배열 검증 확인
  - [ ] blogLinks 내부 객체 검증 확인
  - [ ] menuImages 배열 검증 확인
  - [ ] reviews 배열 검증 확인
  - [ ] reviews 내부 객체 검증 확인
- [ ] `add_restaurant()` 함수 테스트
  - [ ] 유효한 데이터 추가 확인
  - [ ] 무효한 데이터 추가 실패 확인
  - [ ] 중복 매장명 처리 확인
- [ ] `get_restaurant_by_name()` 함수 테스트
  - [ ] 존재하는 매장 검색 확인
  - [ ] 존재하지 않는 매장 검색 확인 (None 반환)
  - [ ] 대소문자 구분 확인

#### 통합 테스트 (RED)
- [ ] Flask 앱과 데이터 로더 통합 테스트
  - [ ] 데이터 로드 후 템플릿 렌더링 확인
  - [ ] API 엔드포인트와 데이터 로더 연동 확인
- [ ] 데이터 검증 통합 테스트
  - [ ] 잘못된 데이터 형식 처리 확인
  - [ ] 데이터 검증 실패 시 에러 처리 확인

#### 데이터 로더 유틸리티 테스트 (RED)
- [x] `load_restaurants_data()` 함수 테스트
  - [x] 정상적인 JSON 파일 로드 확인
  - [x] 존재하지 않는 파일 처리 확인
  - [x] 잘못된 JSON 형식 처리 확인
  - [x] 빈 파일 처리 확인
- [x] `save_restaurants_data()` 함수 테스트
  - [x] 데이터 저장 성공 확인
  - [x] 저장된 데이터 검증 확인
  - [x] 권한 오류 처리 확인 (RED: 실패하는 테스트 작성 완료)
- [x] `validate_restaurant_data()` 함수 테스트
  - [x] 필수 필드(name) 검증 확인
  - [x] blogLinks 배열 검증 확인
  - [x] blogLinks 내부 객체 검증 확인
  - [x] menuImages 배열 검증 확인
  - [x] reviews 배열 검증 확인
  - [x] reviews 내부 객체 검증 확인
- [x] `add_restaurant()` 함수 테스트
  - [x] 유효한 데이터 추가 확인
  - [x] 무효한 데이터 추가 실패 확인
  - [x] 중복 매장명 처리 확인
- [x] `get_restaurant_by_name()` 함수 테스트
  - [x] 존재하는 매장 검색 확인
  - [x] 존재하지 않는 매장 검색 확인 (None 반환)
  - [x] 대소문자 구분 확인

#### 통합 테스트 (RED)
- [x] Flask 앱과 데이터 로더 통합 테스트
  - [x] 데이터 로드 후 템플릿 렌더링 확인
  - [x] API 엔드포인트와 데이터 로더 연동 확인
- [x] 데이터 검증 통합 테스트
  - [x] 잘못된 데이터 형식 처리 확인 (RED: 실패하는 테스트 작성 완료)
  - [x] 데이터 검증 실패 시 에러 처리 확인 (RED: 실패하는 테스트 작성 완료)

#### 테스트 실행 및 확인 (RED)
- [x] 모든 테스트 실행 (`pytest` 또는 `python -m pytest`)
- [x] 모든 테스트가 실패하는지 확인 (RED 단계 목표) - 일부 테스트 실패 확인됨
- [x] 테스트 커버리지 확인 도구 설정 (pytest-cov)
- [x] 테스트 실행 결과 문서화

### TDD 단계: GREEN (실패하는 테스트를 통과시키는 코드 작성)
TDD(Test-Driven Development)의 두 번째 단계로, RED 단계에서 작성한 실패하는 테스트를 통과시키는 최소한의 코드를 작성합니다.

자세한 내용은 [IMPLEMENTATION_ROADMAP.md](./Report/IMPLEMENTATION_ROADMAP.md)를 참고하세요.

#### 🔴 우선순위 1 (Critical - 즉시 구현 필요)

##### 기능 요구사항

- [x] **F1. 에러 핸들러 개선** (예상 작업 시간: 2-3시간) ✅ 완료
  - [x] F1.1: 500 에러 페이지 테스트 통과
    - [x] 500 에러를 발생시키는 테스트 라우트 추가 (`/test-error-500`)
    - [x] 에러 핸들러 내부 로직 테스트 커버리지 향상
    - [x] 관련 테스트: `test_500_error_page` ✅ 통과
    - [x] 목표 커버리지: 100% (현재 77% - app.py)
  - [ ] F1.2: 에러 핸들러 상세 테스트
    - [ ] 다양한 에러 시나리오 테스트
    - [ ] 에러 메시지 검증

- [x] **F2. 데이터 저장 권한 오류 처리** (예상 작업 시간: 3-4시간) ✅ 완료
  - [x] F2.1: 권한 오류 예외 처리 구현
    - [x] `PermissionError` 예외 처리
    - [x] 사용자 친화적 에러 메시지 제공
    - [x] 관련 테스트: `test_save_permission_error` ✅ 통과
    - [x] 목표 커버리지: 100% (현재 69% - data_loader.py)
  - [ ] F2.2: 저장 함수 예외 처리 강화
    - [x] 다양한 파일 시스템 오류 처리 (OSError 추가)
    - [ ] 디스크 공간 부족 처리

- [x] **F3. 데이터 검증 에러 처리** (예상 작업 시간: 4-5시간) ✅ 완료
  - [x] F3.1: 잘못된 데이터 형식 처리
    - [x] 잘못된 JSON 구조 감지
    - [x] 필수 필드 누락 감지
    - [x] 타입 불일치 감지
    - [x] 명확한 에러 메시지 반환
    - [x] 관련 테스트: `test_invalid_data_format_handling` ✅ 통과
    - [x] 목표 커버리지: 100% (현재 69% - data_loader.py)
  - [x] F3.2: 데이터 검증 실패 시 에러 처리
    - [x] 검증 실패 시 상세한 에러 정보 제공
    - [ ] 로깅 기능 추가 (향후 구현)
    - [x] 사용자에게 명확한 피드백 제공
    - [x] 관련 테스트: `test_data_validation_failure_error_handling` ✅ 통과
    - [x] 목표 커버리지: 100% (현재 69% - data_loader.py)

##### 비기능 요구사항

- [x] **N1. 테스트 커버리지 향상** (예상 작업 시간: 8-10시간) ✅ 부분 완료
  - [x] N1.1: 전체 커버리지 63% → 80%+ ✅ **88% 달성!**
  - [ ] N1.2: 데이터 로더 커버리지 23% → 80%+ (현재 71%)
  - [ ] N1.3: Flask 앱 커버리지 71% → 85%+ (현재 72%)
  - [x] N1.4: 커버리지 측정 자동화 ✅ 완료
    - [x] pytest.ini에 커버리지 설정 추가 (임계값 80%)
    - [x] GitHub Actions 워크플로우 추가 (CI/CD 파이프라인)

- [x] **N2. 에러 처리 및 로깅** (예상 작업 시간: 4-5시간) ✅ 완료
  - [x] N2.1: 로깅 시스템 구축 ✅ 완료
    - [x] Python logging 모듈 활용 (`utils/logger.py`)
    - [x] 로그 레벨 설정 (DEBUG, INFO, WARNING, ERROR)
    - [x] 로그 파일 저장 (`logs/app.log`)
  - [x] N2.2: 에러 메시지 표준화 ✅ 완료
    - [x] 일관된 에러 메시지 형식 (로거 포맷터 사용)
    - [x] 사용자 친화적 메시지 (콘솔 출력)
    - [x] 개발자용 상세 정보 (exc_info=True로 스택 트레이스 포함)
  - [x] N2.3: 예외 처리 일관성 ✅ 완료
    - [x] 모든 함수에서 일관된 예외 처리 (로거 사용)
    - [x] 예외 체인 유지 (exc_info=True)
    - [x] 컨텍스트 정보 포함 (파일 경로, 함수명 등)

#### 🟠 우선순위 2 (High - 단기 구현 필요)

##### 기능 요구사항

- [x] **F4. 데이터 로더 예외 처리 강화** (예상 작업 시간: 6-8시간) ✅ 완료
  - [x] F4.1: 파일 존재하지 않을 때 처리 ✅ 완료
    - [x] 명확한 에러 메시지 (로깅)
    - [x] 로깅 추가
    - [x] 목표 커버리지: 100% (현재 75% - data_loader.py)
  - [x] F4.2: JSON 디코딩 에러 처리 ✅ 완료
    - [x] JSON 구문 오류 감지
    - [x] 부분적 JSON 파싱 오류 처리
    - [x] 상세한 에러 정보 제공 (로깅)
    - [x] 목표 커버리지: 100% (현재 75% - data_loader.py)
  - [x] F4.3: 검증 함수 다양한 검증 경로 ✅ 완료
    - [x] 모든 검증 경로 테스트 (빈 배열, 비배열 타입 등)
    - [x] 엣지 케이스 처리
    - [x] 목표 커버리지: 100% (현재 75% - data_loader.py)
  - [x] F4.4: add_restaurant 검증 실패 경로 ✅ 완료
    - [x] 검증 실패 시 상세 정보 제공 (로깅)
    - [x] 빈 이름, None 이름 처리 테스트
    - [x] 목표 커버리지: 100% (현재 75% - data_loader.py)
  - [x] F4.5: get_restaurant_by_name 검색 로직 ✅ 완료
    - [x] 다양한 검색 시나리오 테스트 (빈 이름, 특수 문자, 유니코드)
    - [x] 목표 커버리지: 100% (현재 75% - data_loader.py)

- [x] **F5. 엣지 케이스 처리** (예상 작업 시간: 4-5시간) ✅ 완료
  - [x] F5.1: 빈 데이터 처리 ✅ 완료
    - [x] 빈 JSON 파일 처리
    - [x] 빈 배열 처리
    - [x] 빈 객체 처리
  - [x] F5.2: 매우 큰 데이터 처리 ✅ 완료
    - [x] 대용량 JSON 파일 처리 (1000개 매장 테스트)
    - [x] 메모리 최적화 (기본 Python json 모듈 사용)
    - [ ] 스트리밍 파싱 고려 (향후 구현)
  - [x] F5.3: 특수 문자 처리 ✅ 완료
    - [x] 유니코드 문자 처리 (이모지 포함)
    - [x] 이스케이프 문자 처리 (\n, \t 등)
    - [x] 경로 특수 문자 처리 (&, -, (, ), ', ", /, \ 등)
  - [x] F5.4: 중복 매장명 처리 ✅ 완료
    - [x] 중복 감지 기능 (`allow_duplicate` 옵션)
    - [x] 중복 처리 정책 정의 (기본: 허용, 옵션: 방지)
    - [x] 사용자 알림 (로깅)

##### 비기능 요구사항

- [x] **N3. 코드 품질 개선** (예상 작업 시간: 6-8시간) ✅ 완료
  - [x] N3.1: 코드 리팩토링 ✅ 완료
    - [x] 중복 코드 제거 (검증 함수 공통 로직 분리)
    - [x] 함수 분리 및 모듈화 (헬퍼 함수 추가: `_validate_blog_links`, `_validate_menu_images`, `_validate_reviews`)
    - [x] 명확한 네이밍 (함수명 및 변수명 개선)
  - [x] N3.2: 타입 힌팅 강화 ✅ 완료
    - [x] 모든 함수에 타입 힌팅 추가 (`get_restaurant_by_name`, Flask 라우트 함수들)
    - [x] mypy 설정 파일 추가 (`mypy.ini`)
  - [x] N3.3: 문서화 개선 ✅ 완료
    - [x] Docstring 보완 (모듈 레벨, 함수 레벨 문서화)
    - [x] 인라인 주석 추가 (주요 로직 설명)
    - [ ] API 문서화 (향후 구현)

- [x] **N4. 성능 최적화** (예상 작업 시간: 4-6시간) ✅ 부분 완료
  - [x] N4.1: 데이터 로딩 최적화 ✅ 완료
    - [x] 캐싱 메커니즘 구현 (전역 캐시 변수 사용)
    - [x] 지연 로딩 고려 (캐시가 비어있을 때만 로드)
    - [x] 메모리 사용 최적화 (단일 인스턴스 캐시)
  - [x] N4.2: 테스트 실행 시간 최적화 ✅ 완료
    - [x] 현재: 0.50초 (이전 0.68초에서 개선)
    - [x] 목표: 0.1초 이하 유지 (가장 느린 테스트: 0.10초)
  - [ ] N4.3: 대용량 데이터 처리 (부분 완료)
    - [ ] 스트리밍 파싱 (향후 구현)
    - [ ] 배치 처리 (향후 구현)
    - [x] 메모리 효율성 (기본 Python json 모듈 사용, 1000개 매장 테스트 통과)

##### 비기능 요구사항

- [ ] **N5. 보안 강화** (예상 작업 시간: 5-6시간)
  - [ ] N5.1: 입력 검증 강화
    - [ ] SQL Injection 방지 (현재는 JSON이지만 미래 대비)
    - [ ] XSS 방지
    - [ ] 경로 탐색 공격 방지
  - [ ] N5.2: 파일 접근 보안
    - [ ] 파일 경로 검증
    - [ ] 권한 체크
    - [ ] 안전한 파일 처리

- [ ] **N6. 모니터링 및 관찰성** (예상 작업 시간: 4-5시간)
  - [ ] N6.1: 메트릭 수집
    - [ ] 요청 수
    - [ ] 응답 시간
    - [ ] 에러율
  - [ ] N6.2: 헬스 체크 엔드포인트
    - [ ] `/health` 엔드포인트
    - [ ] 데이터베이스 연결 상태
    - [ ] 파일 시스템 접근 가능 여부    - [ ] `/health` 엔드포인트
    - [ ] 데이터베이스 연결 상태
    - [ ] 파일 시스템 접근 가능 여부    - [x] API 문서 작성 (`docs/API.md`)
    - [x] API 사용 예제 (cURL, Python, JavaScript)
    - [ ] Swagger/OpenAPI 문서 (향후 구현)

##### 비기능 요구사항

- [x] **N5. 보안 강화** (예상 작업 시간: 5-6시간) ✅ 완료
  - [x] N5.1: 입력 검증 강화 ✅ 완료
    - [x] SQL Injection 방지 (현재는 JSON이지만 미래 대비 - 입력 검증 강화)
    - [x] XSS 방지 (Jinja2 템플릿 자동 이스케이프 + 문자열 정리 함수)
    - [x] 경로 탐색 공격 방지 (경로 정규화 및 검증 함수)
  - [x] N5.2: 파일 접근 보안 ✅ 완료
    - [x] 파일 경로 검증 (`sanitize_path`, `validate_file_path` 함수)
    - [x] 권한 체크 (경로 탐색 공격 방지)
    - [x] 안전한 파일 처리 (이미지 파일 확장자 검증, 기준 디렉토리 밖 접근 차단)

- [x] **N6. 모니터링 및 관찰성** (예상 작업 시간: 4-5시간) ✅ 완료
  - [x] N6.1: 메트릭 수집 ✅ 완료
    - [x] 요청 수 (`/api/metrics` 엔드포인트)
    - [x] 응답 시간 (평균, 최소, 최대)
    - [x] 에러율 (에러 수 / 요청 수)
  - [x] N6.2: 헬스 체크 엔드포인트 ✅ 완료
    - [x] `/health` 엔드포인트
    - [x] 파일 시스템 접근 가능 여부 확인
    - [x] 데이터 로드 가능 여부 확인
    - [ ] 데이터베이스 연결 상태 (현재는 JSON 파일 사용으로 불필요)

#### GREEN 단계 성공 기준
- [x] 모든 RED 단계 실패 테스트 통과 ✅
  - [x] `test_500_error_page` - 500 에러 페이지 테스트 통과
  - [x] `test_save_permission_error` - 권한 오류 처리 테스트 통과
  - [x] `test_invalid_data_format_handling` - 잘못된 데이터 형식 처리 테스트 통과
  - [x] `test_data_validation_failure_error_handling` - 데이터 검증 실패 시 에러 처리 테스트 통과
- [x] 전체 커버리지 75% 이상 ✅
  - 최신 측정: **92.29%** ✅ (목표 달성)
- [x] 데이터 로더 커버리지 60% 이상 ✅
  - 최신 측정: **75%** ✅ (목표 달성)
- [x] Flask 앱 커버리지 80% 이상 ✅
  - 최신 측정: **85%** ✅ (목표 달성)

### TDD 단계: REFACTOR (코드 개선 및 리팩토링)
TDD(Test-Driven Development)의 세 번째 단계로, 테스트를 통과시키는 코드를 개선하고 리팩토링합니다.

자세한 내용은 [REFACTOR_GUIDE.md](./Report/REFACTOR_GUIDE.md)를 참고하세요.

#### 1단계: 코드스멜 분석 및 정적 분석

##### 1.1 코드스멜 분석
- [x] **전역 변수 제거** ✅ 완료
  - [x] `_restaurants_cache` 전역 변수를 `RestaurantCache` 클래스로 리팩토링 (싱글톤 패턴)
  - [x] `_metrics` 전역 변수를 `MetricsCollector` 클래스로 캡슐화 (싱글톤 패턴)
  - [x] 전역 상태 의존성 제거 (`utils/cache.py`, `utils/metrics.py` 생성)

- [x] **중복 코드 제거** ✅ 완료
  - [x] `load_restaurants_data`와 `save_restaurants_data`의 경로 검증 로직 통합 (`utils/file_utils.py`의 `validate_and_normalize_path` 함수)
  - [x] 검증 함수들의 중복 로직 추출 (이미 `_validate_blog_links`, `_validate_reviews` 등으로 분리됨)
  - [x] 에러 응답 생성 로직 통합 (`_create_error_response` 함수 사용)

- [x] **긴 함수 분리** ✅ 완료
  - [x] `health_check` 함수 분리 (`_check_filesystem_health`, `_check_data_load_health` 헬퍼 함수 추가)
  - [x] `validate_restaurant_data_with_error` 함수 분리 (이미 각 필드별 검증 함수로 분리됨)
  - [x] `api_restaurants` 함수의 예외 처리 로직 분리 (`_create_error_response` 사용)

- [x] **매직 넘버/문자열 제거** ✅ 완료
  - [x] 하드코딩된 숫자 상수화 (`100` → `MAX_RESPONSE_TIMES` in `utils/constants.py`)
  - [x] 하드코딩된 문자열 상수화 (`'data/restaurants.json'` → `DEFAULT_DATA_PATH` in `utils/constants.py`)
  - [x] 에러 메시지 상수화 (`ERROR_MESSAGES`, `ERROR_CODES` in `utils/constants.py`)

- [x] **네이밍 개선** ✅ 완료
  - [x] 일관된 네이밍 컨벤션 적용 (클래스명: PascalCase, 함수명: snake_case)
  - [x] 모호한 변수명 개선 (`_restaurants_cache` → `cache`, `_metrics` → `metrics`)
  - [x] 함수명과 역할 일치 확인 (모든 함수명이 역할을 명확히 표현)

##### 1.2 정적 분석 도구 실행
- [x] **mypy 타입 체크** ✅ 완료
  - [x] 모든 타입 힌팅 검증 (데코레이터, 함수 파라미터, 반환 타입)
  - [x] 타입 오류 수정 (`Optional[str]`, `list[dict[str, Any]]` 등)
  - [x] `mypy.ini` 설정 최적화 (`show_error_codes`, `show_column_numbers` 추가)

- [x] **pylint/flake8 코드 품질 검사** ✅ 완료
  - [x] 코드 스타일 검사 (`.flake8`, `.pylintrc` 설정 파일 생성)
  - [x] 복잡도 분석 (max-complexity=10 설정)
  - [x] 코드 품질 점수 향상 (정적 분석 도구 설정 완료)

- [x] **순환 복잡도 분석** ✅ 완료
  - [x] 복잡도가 높은 함수 식별 (radon 도구 설정)
  - [x] 복잡한 조건문 단순화 (함수 분리로 해결)
  - [x] 중첩 루프 최소화 (기존 코드에서 중첩 루프 없음 확인)

#### 2단계: SOLID 원칙 적용

##### 2.1 Single Responsibility Principle (단일 책임 원칙)
- [ ] **클래스/함수 책임 분리**
  - [ ] `app.py`의 라우트 핸들러와 비즈니스 로직 분리
  - [ ] 데이터 로딩과 검증 로직 분리
  - [ ] 메트릭 수집과 응답 생성 분리

- [ ] **서비스 레이어 도입**
  - [ ] `RestaurantService` 클래스 생성 (비즈니스 로직)
  - [ ] `MetricsService` 클래스 생성 (메트릭 관리)
  - [ ] `HealthCheckService` 클래스 생성 (헬스 체크 로직)

##### 2.2 Open/Closed Principle (개방-폐쇄 원칙)
- [ ] **확장 가능한 구조 설계**
  - [ ] 인터페이스/추상 클래스 도입 (데이터 소스 추상화)
  - [ ] 플러그인 방식으로 검증 규칙 추가 가능하도록 설계
  - [ ] 전략 패턴 적용 (검증 전략, 저장 전략)

##### 2.3 Liskov Substitution Principle (리스코프 치환 원칙)
- [ ] **인터페이스 구현 일관성**
  - [ ] 추상 클래스/인터페이스 정의
  - [ ] 구현 클래스들이 인터페이스 계약 준수 확인

##### 2.4 Interface Segregation Principle (인터페이스 분리 원칙)
- [ ] **인터페이스 세분화**
  - [ ] 큰 인터페이스를 작은 단위로 분리
  - [ ] 클라이언트가 사용하지 않는 메서드 제거

##### 2.5 Dependency Inversion Principle (의존성 역전 원칙)
- [ ] **의존성 주입 도입**
  - [ ] 전역 변수 의존성 제거
  - [ ] 생성자 주입 또는 의존성 주입 프레임워크 사용
  - [ ] 테스트 가능한 구조로 개선

#### 3단계: 아키텍처 개선

##### 3.1 레이어 분리
- [ ] **프레젠테이션 레이어** (라우트 핸들러)
  - [ ] Flask 라우트만 담당하도록 단순화
  - [ ] 요청/응답 변환 로직 분리

- [ ] **비즈니스 로직 레이어** (서비스)
  - [ ] `RestaurantService`: 매장 데이터 관리
  - [ ] `MetricsService`: 메트릭 수집 및 관리
  - [ ] `HealthCheckService`: 헬스 체크 로직

- [ ] **데이터 접근 레이어** (리포지토리)
  - [ ] `RestaurantRepository`: 데이터 로드/저장
  - [ ] 파일 시스템 추상화
  - [ ] 향후 데이터베이스 전환 용이하도록 설계

##### 3.2 설계 패턴 적용
- [ ] **Repository 패턴**
  - [ ] 데이터 접근 로직 캡슐화
  - [ ] 테스트 용이성 향상

- [ ] **Factory 패턴**
  - [ ] 서비스 객체 생성 팩토리
  - [ ] 설정 기반 객체 생성

- [ ] **Strategy 패턴**
  - [ ] 검증 전략 분리
  - [ ] 저장 전략 분리

- [ ] **Singleton 패턴** (필요시)
  - [ ] 캐시 관리자 싱글톤
  - [ ] 메트릭 수집기 싱글톤

#### 4단계: 코드 품질 향상

##### 4.1 타입 안정성 강화
- [ ] **타입 힌팅 완성**
  - [ ] 모든 함수에 완전한 타입 힌팅 추가
  - [ ] 제네릭 타입 활용
  - [ ] `TypedDict` 활용 (JSON 스키마 정의)

- [ ] **타입 체크 통과**
  - [ ] `mypy --strict` 모드 통과
  - [ ] 타입 관련 경고 제거

##### 4.2 에러 처리 개선
- [ ] **커스텀 예외 클래스 도입**
  - [ ] `RestaurantDataError`: 데이터 관련 에러
  - [ ] `ValidationError`: 검증 관련 에러
  - [ ] `FileAccessError`: 파일 접근 관련 에러

- [ ] **에러 처리 일관성**
  - [ ] 모든 예외 처리에서 로깅 포함
  - [ ] 사용자 친화적 에러 메시지
  - [ ] 에러 코드 체계화

##### 4.3 로깅 개선
- [ ] **구조화된 로깅**
  - [ ] JSON 형식 로그 출력 (선택사항)
  - [ ] 컨텍스트 정보 포함
  - [ ] 로그 레벨 최적화

##### 4.4 문서화 개선
- [ ] **Docstring 표준화**
  - [ ] Google/NumPy 스타일 Docstring 적용
  - [ ] 모든 공개 함수에 예제 추가
  - [ ] 타입 정보 명시

- [ ] **인라인 주석 정리**
  - [ ] 불필요한 주석 제거
  - [ ] 복잡한 로직에 설명 추가
  - [ ] TODO/FIXME 주석 정리

#### 5단계: 성능 최적화

##### 5.1 캐싱 개선
- [ ] **캐시 전략 개선**
  - [ ] 파일 변경 감지 (mtime 기반)
  - [ ] TTL(Time To Live) 기반 캐시 무효화
  - [ ] LRU 캐시 적용 (선택사항)

##### 5.2 메모리 최적화
- [ ] **메모리 사용량 분석**
  - [ ] 프로파일링 도구 사용
  - [ ] 메모리 누수 확인
  - [ ] 대용량 데이터 처리 최적화

##### 5.3 응답 시간 최적화
- [ ] **지연 로딩 최적화**
  - [ ] 필요한 데이터만 로드
  - [ ] 배치 처리 최적화

#### 6단계: 테스트 개선

##### 6.1 테스트 구조 개선
- [ ] **테스트 픽스처 개선**
  - [ ] 공통 테스트 데이터 팩토리
  - [ ] Mock 객체 활용
  - [ ] 테스트 격리 강화

##### 6.2 테스트 커버리지 유지
- [ ] **리팩토링 후 커버리지 확인**
  - [ ] 커버리지 90% 이상 유지
  - [ ] 새로운 코드 경로 테스트 추가

##### 6.3 통합 테스트 강화
- [ ] **E2E 테스트 추가**
  - [ ] 전체 워크플로우 테스트
  - [ ] 실제 데이터 파일 사용 테스트

#### 7단계: 리팩토링 검증

##### 7.1 리팩토링 후 테스트
- [ ] **모든 테스트 통과 확인**
  - [ ] 기존 테스트 모두 통과
  - [ ] 새로운 테스트 추가 (필요시)

##### 7.2 성능 벤치마크
- [ ] **성능 비교**
  - [ ] 리팩토링 전/후 응답 시간 비교
  - [ ] 메모리 사용량 비교
  - [ ] 성능 저하 없는지 확인

##### 7.3 코드 리뷰
- [ ] **코드 리뷰 체크리스트**
  - [ ] SOLID 원칙 준수 확인
  - [ ] 코드스멜 제거 확인
  - [ ] 테스트 커버리지 확인
  - [ ] 문서화 완성도 확인

#### REFACTOR 단계 성공 기준
- [ ] 코드스멜 제거 완료
- [ ] SOLID 원칙 준수 (각 원칙별 체크리스트 통과)
- [ ] 정적 분석 도구 경고 0개
- [ ] 타입 체크 통과 (`mypy --strict`)
- [ ] 테스트 커버리지 90% 이상 유지
- [ ] 성능 저하 없음 (응답 시간 ±10% 이내)
- [ ] 코드 복잡도 감소 (평균 순환 복잡도 5 이하)

### 8단계: 테스트 및 최적화
- [ ] Flask 서버 실행 및 테스트
- [ ] 크로스 브라우저 테스트
- [ ] 모바일 반응형 테스트
- [ ] 이미지 최적화 (용량, 로딩 속도)
- [ ] Python 코드 최적화
- [ ] 성능 최적화

### 9단계: 배포 준비
- [x] 최종 검토
- [x] README 파일 작성 (Python 설치 및 실행 방법 포함)
- [x] requirements.txt 확인
- [ ] 배포 환경 설정 (예: Heroku, AWS, PythonAnywhere 등)

## ⚠️ 주의사항

자세한 주의사항은 `PROJECT_GUIDE.md` 파일을 참고하세요.

주요 주의사항:
- 이미지 저작권 확인 필수
- 개인정보 보호법 준수
- 반응형 디자인 구현
- 이미지 최적화

## 📝 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 제작되었습니다.

## 👤 작성자

2025년 천안시 맛집 프로젝트

