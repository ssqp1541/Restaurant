# 정적 분석 도구 실행 스크립트 (PowerShell)

Write-Host "=========================================="
Write-Host "정적 분석 도구 실행"
Write-Host "=========================================="

Write-Host ""
Write-Host "1. mypy 타입 체크"
Write-Host "----------------------------------------"
python -m mypy app.py utils/ --config-file mypy.ini

Write-Host ""
Write-Host "2. flake8 코드 스타일 검사"
Write-Host "----------------------------------------"
python -m flake8 app.py utils/ --config=.flake8

Write-Host ""
Write-Host "3. pylint 코드 품질 검사"
Write-Host "----------------------------------------"
python -m pylint app.py utils/ --rcfile=.pylintrc

Write-Host ""
Write-Host "4. radon 순환 복잡도 분석"
Write-Host "----------------------------------------"
python -m radon cc app.py utils/ --min B

Write-Host ""
Write-Host "=========================================="
Write-Host "정적 분석 완료"
Write-Host "=========================================="

