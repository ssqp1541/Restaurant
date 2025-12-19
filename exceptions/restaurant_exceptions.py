"""
매장 관련 예외 클래스
커스텀 예외를 정의하여 에러 처리를 체계화합니다.
"""


class RestaurantDataError(Exception):
    """
    매장 데이터 관련 에러
    
    데이터 로드, 저장, 처리 중 발생하는 에러를 나타냅니다.
    """
    
    def __init__(self, message: str, error_code: str = "DATA_ERROR", details: dict = None):
        """
        예외 초기화
        
        Args:
            message: 에러 메시지
            error_code: 에러 코드
            details: 추가 상세 정보
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self) -> str:
        """에러 메시지 문자열 표현"""
        return f"[{self.error_code}] {self.message}"


class ValidationError(Exception):
    """
    검증 관련 에러
    
    데이터 검증 실패 시 발생하는 에러를 나타냅니다.
    """
    
    def __init__(self, message: str, field: str = None, error_code: str = "VALIDATION_ERROR"):
        """
        예외 초기화
        
        Args:
            message: 에러 메시지
            field: 검증 실패한 필드명
            error_code: 에러 코드
        """
        super().__init__(message)
        self.message = message
        self.field = field
        self.error_code = error_code
    
    def __str__(self) -> str:
        """에러 메시지 문자열 표현"""
        field_info = f" (field: {self.field})" if self.field else ""
        return f"[{self.error_code}]{field_info} {self.message}"


class FileAccessError(Exception):
    """
    파일 접근 관련 에러
    
    파일 읽기/쓰기 권한 오류, 파일 없음 등의 에러를 나타냅니다.
    """
    
    def __init__(
        self,
        message: str,
        file_path: str = None,
        error_code: str = "FILE_ACCESS_ERROR",
        original_error: Exception = None
    ):
        """
        예외 초기화
        
        Args:
            message: 에러 메시지
            file_path: 문제가 발생한 파일 경로
            error_code: 에러 코드
            original_error: 원본 예외 객체
        """
        super().__init__(message)
        self.message = message
        self.file_path = file_path
        self.error_code = error_code
        self.original_error = original_error
    
    def __str__(self) -> str:
        """에러 메시지 문자열 표현"""
        path_info = f" (path: {self.file_path})" if self.file_path else ""
        return f"[{self.error_code}]{path_info} {self.message}"

