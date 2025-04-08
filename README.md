# FFT 分析套件

這是一個用於頻譜分析的 Python 套件，包含 FFT（快速傅立葉轉換）、iFFT（逆快速傅立葉轉換）和梅爾頻譜分析功能。

## 套件功能

### FFT 分析
- 生成測試信號並進行 FFT 分析
- 使用 iFFT 重建信號
- 自動生成實驗報告和數據檔案

### 梅爾頻譜分析
- 支援音訊信號的梅爾頻譜轉換
- 可自訂梅爾濾波器數量和頻率範圍
- 自動生成頻譜圖和數據檔案

## 安裝方式

### 使用 pip 安裝

```bash
# 從專案根目錄安裝
pip install -e .
```

### 使用 Docker

```bash
docker build -t fft-analysis .
docker run -it fft-analysis
```

## 使用方式

### FFT 分析
```python
from fft_analysis import FFTAnalyzer

# 創建分析器實例
analyzer = FFTAnalyzer(experiment_id=1)

# 生成信號並分析
t, signal, target_freqs = analyzer.generate_signal()
freq, magnitude = analyzer.perform_fft(signal, sampling_rate=1000)
```

### 梅爾頻譜分析
```python
from fft_analysis import MelSpectrogramAnalyzer

# 創建分析器實例
analyzer = MelSpectrogramAnalyzer(
    n_mels=128,
    fmin=0.0,
    fmax=8000.0,
    experiment_id=1
)

# 計算梅爾頻譜
mel_spectrogram = analyzer.compute_melspectrogram(signal, sr=22050)
```

## 開發指南

1. 安裝開發環境
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
pip install -e .
```

2. 執行測試
```bash
python -m pytest tests/
```

3. 執行示例
```bash
python examples/fft_example.py
python examples/mel_spectrogram_example.py
```

## 輸出檔案

- `FFT_Example_Exp{ID}_{DATE}_plot_results.png`: FFT 分析結果圖
- `FFT_Data_Exp{ID}_{DATE}_save_data.json`: FFT 分析數據
- `Mel_Spectrogram_Exp{ID}_{DATE}.png`: 梅爾頻譜圖
- `Mel_Data_Exp{ID}_{DATE}.json`: 梅爾頻譜數據
- `REPORT.md`: 實驗報告彙整
