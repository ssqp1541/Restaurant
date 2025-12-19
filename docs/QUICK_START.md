# 빠른 시작 가이드

## Python Flask 환경에서 실행하기

### 1. 필수 요구사항 확인
- Python 3.8 이상 설치 확인
  ```bash
  python --version
  ```

### 2. 가상 환경 생성 및 활성화

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 서버 실행
```bash
python app.py
```

### 5. 웹 브라우저에서 접속
- http://localhost:5000

## 데이터 수정하기

### 매장 데이터 추가/수정
1. `data/restaurants.json` 파일을 열기
2. JSON 형식에 맞춰 매장 정보 입력
3. 서버 재시작 (자동 리로드가 활성화되어 있으면 자동 반영)

### 이미지 추가하기
1. `images/restaurants/[매장명]/` 폴더에 메뉴 이미지 3개 추가
2. `restaurants.json`에서 이미지 경로 확인
3. 경로 형식: `restaurants/[매장명]/menu1.jpg`

## 문제 해결

### 포트가 이미 사용 중인 경우
```bash
# app.py 파일에서 port 번호 변경
app.run(debug=True, host='0.0.0.0', port=5001)
```

### 모듈을 찾을 수 없는 경우
```bash
# 현재 디렉토리에서 실행하는지 확인
# 프로젝트 루트 디렉토리에서 실행해야 합니다
```

### 이미지가 표시되지 않는 경우
- 이미지 파일 경로 확인
- `images/` 폴더 구조 확인
- 파일명과 JSON의 경로가 일치하는지 확인

