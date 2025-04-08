# FFT 分析專案

這是一個用於頻譜分析的 Python 專案，包含 FFT（快速傅立葉轉換）、iFFT（逆快速傅立葉轉換）和梅爾頻譜分析功能。

## 功能特點

### FFT 分析
- 生成測試信號並進行 FFT 分析
- 使用 iFFT 重建信號
- 自動生成實驗報告和數據檔案

### 梅爾頻譜分析
- 支援音訊信號的梅爾頻譜轉換
- 可自訂梅爾濾波器數量和頻率範圍
- 自動生成頻譜圖和數據檔案
- 提供頻率到梅爾刻度的轉換功能

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

### FFT 分析
```bash
python fft_example.py
```

### 梅爾頻譜分析
```bash
python mel_spectrogram.py
```

## 輸出檔案

- `FFT_Example_Exp{ID}_{DATE}_plot_results.png`: FFT 分析結果圖
- `FFT_Data_Exp{ID}_{DATE}_save_data.json`: FFT 分析數據
- `Mel_Spectrogram_Exp{ID}_{DATE}.png`: 梅爾頻譜圖
- `Mel_Data_Exp{ID}_{DATE}.json`: 梅爾頻譜數據
- `REPORT.md`: 實驗報告彙整

## 技術文件

新增的主要功能類別：
- `MelSpectrogramAnalyzer`: 提供梅爾頻譜分析相關功能
  - `compute_melspectrogram()`: 計算梅爾頻譜
  - `plot_melspectrogram()`: 繪製梅爾頻譜圖
  - `save_data()`: 保存分析數據
  - `update_report()`: 更新實驗報告