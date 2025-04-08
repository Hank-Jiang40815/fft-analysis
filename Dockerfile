FROM python:3.9-slim

WORKDIR /app

# 安裝系統相依套件
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製套件檔案
COPY . .

# 安裝套件相依
RUN pip install --no-cache-dir -r requirements.txt

# 安裝套件本身
RUN pip install -e .

# 設定環境變數
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# 安裝開發相關依賴
RUN pip install --no-cache-dir pytest

# 執行單元測試
RUN pytest tests/

# 預設命令
CMD ["python", "-m", "examples.fft_example"]