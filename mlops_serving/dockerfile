# 1. 베이스 이미지 설정 (가벼운 파이썬 버전)
FROM python:3.13-slim

# 2. 작업 디렉토리 설정
WORKDIR /root/mlops_serving

# 3. 필수 라이브러리 설치
# Scikit-learn 버전은 학습 때와 동일하게 맞추는 것이 좋습니다.
# 사실 이부분은 이렇게 하는것보다 requirement 파일 만들어서 하는게 더 좋긴합니다 ㅎㅎ..
RUN pip install --no-cache-dir fastapi uvicorn scikit-learn joblib python-multipart

# 4. 모델 파일과 API 코드를 컨테이너 안으로 복사
COPY main.py .
COPY model.joblib .

# 5. 서버 실행 명령 (8000 포트)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
