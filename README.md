# 천안시 맛집 안내 웹페이지

2025년 충청남도 천안시의 맛집을 소개하는 웹사이트입니다.

## 📌 프로젝트 개요

천안시의 추천 맛집 정보를 제공하며, 각 매장의 대표 메뉴, Naver 블로그 리뷰, 고객 후기를 한눈에 볼 수 있습니다.

## 🚀 시작하기

### 필수 요구사항
- Python 3.8 이상
- pip (Python 패키지 관리자)

### 설치 방법

1. **프로젝트 클론 또는 다운로드**

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

#### 테스트 환경 설정
- [ ] 테스트 프레임워크 설치 (pytest, pytest-flask 등)
- [ ] 테스트 디렉토리 구조 생성 (`tests/` 폴더)
- [ ] 테스트 설정 파일 작성 (`pytest.ini` 또는 `conftest.py`)
- [ ] requirements.txt에 테스트 의존성 추가

#### Flask 애플리케이션 테스트 (RED)
- [ ] 메인 페이지 라우트 테스트 (`/`)
  - [ ] 정상 응답 코드 (200) 확인
  - [ ] 템플릿 렌더링 확인
  - [ ] 매장 데이터 전달 확인
- [ ] API 엔드포인트 테스트 (`/api/restaurants`)
  - [ ] JSON 응답 형식 확인
  - [ ] 매장 데이터 반환 확인
  - [ ] 빈 데이터 처리 확인
- [ ] 이미지 서빙 라우트 테스트 (`/images/<filename>`)
  - [ ] 존재하는 이미지 파일 서빙 확인
  - [ ] 존재하지 않는 이미지 404 처리 확인
- [ ] 에러 핸들러 테스트
  - [ ] 404 에러 페이지 테스트
  - [ ] 500 에러 페이지 테스트

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

#### 테스트 실행 및 확인 (RED)
- [ ] 모든 테스트 실행 (`pytest` 또는 `python -m pytest`)
- [ ] 모든 테스트가 실패하는지 확인 (RED 단계 목표)
- [ ] 테스트 커버리지 확인 도구 설정 (pytest-cov)
- [ ] 테스트 실행 결과 문서화

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

