#!/bin/bash
# 정적 분석 도구 실행 스크립트

echo "=========================================="
echo "정적 분석 도구 실행"
echo "=========================================="

echo ""
echo "1. mypy 타입 체크"
echo "----------------------------------------"
python -m mypy app.py utils/ --config-file mypy.ini

echo ""
echo "2. flake8 코드 스타일 검사"
echo "----------------------------------------"
python -m flake8 app.py utils/ --config=.flake8

echo ""
echo "3. pylint 코드 품질 검사"
echo "----------------------------------------"
python -m pylint app.py utils/ --rcfile=.pylintrc

echo ""
echo "4. radon 순환 복잡도 분석"
echo "----------------------------------------"
python -m radon cc app.py utils/ --min B

echo ""
echo "=========================================="
echo "정적 분석 완료"
echo "=========================================="

