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
├── app.py                 # Flask 메인 애플리케이션
├── requirements.txt       # Python 패키지 의존성
├── templates/
│   ├── index.html        # 메인 HTML 템플릿
│   └── error.html        # 에러 페이지 템플릿
├── static/
│   ├── css/
│   │   └── main.css      # 스타일시트
│   └── js/
│       └── main.js       # JavaScript (모달 기능)
├── utils/
│   └── data_loader.py    # 데이터 로딩 유틸리티
├── data/
│   └── restaurants.json  # 매장 데이터
├── images/               # 이미지 파일들
├── README.md             # 프로젝트 설명서
├── PROJECT_GUIDE.md      # 프로젝트 가이드
└── PRD.md                # 제품 요구사항 문서 (Product Requirements Document)
```

## 📊 데이터 구조

각 매장은 다음 정보를 포함합니다:
- 매장명
- 주소
- 전화번호
- 영업시간
- Naver 블로그 링크 (3개)
- 대표 메뉴 이미지 (3개)
- 고객 후기 (3개)

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

### 1단계: 프로젝트 구조 설정
- [x] Python 가상 환경 생성
- [x] Flask 및 필요한 패키지 설치
- [x] 프로젝트 폴더 구조 생성 (templates, static, utils 등)
- [x] 이미지 저장 폴더 생성 (`images/`)

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

