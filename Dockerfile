# 1. 베이스 이미지 선택
FROM python:3.13-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. requirements.txt를 먼저 복사하고 라이브러리 설치
# (pip가 설치 중 임시 캐시 파일을 저장하지 않도록 하여, 이미지 용량을 줄이고 불필요한 파일 남지 않도록)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 나머지 프로젝트 파일 전체 복사
COPY . .

# 5. 컨테이너가 시작될 때 실행할 명령어 설정
CMD ["python", "main.py"]