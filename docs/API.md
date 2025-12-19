# API 문서

## 개요

천안시 맛집 안내 웹사이트의 REST API 문서입니다.

**Base URL**: `http://localhost:5000`

## 엔드포인트

### GET /api/restaurants

매장 데이터 목록을 반환합니다.

#### 요청

```http
GET /api/restaurants HTTP/1.1
Host: localhost:5000
```

#### 성공 응답 (200 OK)

```json
{
  "success": true,
  "data": [
    {
      "name": "예시 맛집 1",
      "address": "충청남도 천안시 동남구 예시로 123",
      "phone": "041-123-4567",
      "hours": "11:00 - 22:00",
      "blogLinks": [
        {
          "url": "https://blog.naver.com/example1",
          "title": "맛집 탐방기 1"
        }
      ],
      "menuImages": [
        "images/restaurants/restaurant1/menu1.jpg"
      ],
      "reviews": [
        {
          "text": "정말 맛있었어요!",
          "rating": 5
        }
      ]
    }
  ],
  "count": 3
}
```

#### 에러 응답 (500 Internal Server Error)

```json
{
  "success": false,
  "error": {
    "message": "데이터를 불러올 수 없습니다.",
    "code": "ERR_DATA_LOAD_FAILED",
    "status": 500
  }
}
```

#### 응답 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `success` | boolean | 요청 성공 여부 |
| `data` | array | 매장 데이터 배열 |
| `count` | number | 매장 개수 |
| `error` | object | 에러 정보 (에러 발생 시) |
| `error.message` | string | 에러 메시지 |
| `error.code` | string | 에러 코드 |
| `error.status` | number | HTTP 상태 코드 |

## 에러 응답 형식

모든 API 에러 응답은 다음 형식을 따릅니다:

```json
{
  "success": false,
  "error": {
    "message": "에러 메시지",
    "code": "ERR_CODE",
    "status": 400
  }
}
```

### HTTP 상태 코드

| 상태 코드 | 설명 |
|-----------|------|
| 200 | 성공 |
| 400 | 잘못된 요청 |
| 404 | 리소스를 찾을 수 없음 |
| 500 | 서버 내부 오류 |

### 에러 코드

| 에러 코드 | 설명 |
|-----------|------|
| `ERR_400` | 잘못된 요청 |
| `ERR_404` | 리소스를 찾을 수 없음 |
| `ERR_500` | 서버 내부 오류 |
| `ERR_DATA_LOAD_FAILED` | 데이터 로드 실패 |

## 사용 예제

### cURL

```bash
# 매장 목록 조회
curl http://localhost:5000/api/restaurants
```

### Python

```python
import requests

# 매장 목록 조회
response = requests.get('http://localhost:5000/api/restaurants')
data = response.json()

if data['success']:
    restaurants = data['data']
    print(f"총 {data['count']}개 매장")
    for restaurant in restaurants:
        print(f"- {restaurant['name']}")
else:
    print(f"에러: {data['error']['message']}")
```

### JavaScript (Fetch API)

```javascript
// 매장 목록 조회
fetch('http://localhost:5000/api/restaurants')
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log(`총 ${data.count}개 매장`);
      data.data.forEach(restaurant => {
        console.log(`- ${restaurant.name}`);
      });
    } else {
      console.error(`에러: ${data.error.message}`);
    }
  });
```

## 버전 정보

- **API 버전**: 1.0.0
- **최종 업데이트**: 2025년 12월 19일

