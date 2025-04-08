FROM python:3.9-slim

WORKDIR /app

# 安裝系統相依套件
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製必要檔案
COPY requirements.txt .
COPY fft_example.py .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 設定環境變數
ENV PYTHONUNBUFFERED=1

# 執行程式
CMD ["python", "fft_example.py"]