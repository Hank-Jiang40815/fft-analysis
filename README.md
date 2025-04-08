# FFT 分析專案

這是一個用於展示 FFT（快速傅立葉轉換）和 iFFT（逆快速傅立葉轉換）的 Python 專案。

## 功能特點

- 生成測試信號並進行 FFT 分析
- 使用 iFFT 重建信號
- 自動生成實驗報告和數據檔案
- 支援 Docker 容器化部署

## 安裝方式

### 使用 Python 虛擬環境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 使用 Docker

```bash
docker build -t fft-analysis .
docker run -it fft-analysis
```

## 使用方式

直接執行主程式：

```bash
python fft_example.py
```

## 輸出檔案

- `FFT_Example_Exp{ID}_{DATE}_plot_results.png`: FFT 分析結果圖
- `FFT_Data_Exp{ID}_{DATE}_save_data.json`: 實驗數據
- `REPORT.md`: 實驗報告彙整
