#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from fft_analysis.audio import STFTProcessor, AudioLoader
from fft_analysis.visualization import SpectrogramPlotter
import os

def generate_test_signal(duration=1.0, sample_rate=44100):
    """生成測試用的音訊信號。

    Args:
        duration (float, optional): 信號持續時間（秒）。預設為1.0。
        sample_rate (int, optional): 取樣率。預設為44100Hz。

    Returns:
        tuple: (信號數據, 取樣率)。
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    # 生成一個包含多個頻率的信號
    signal = (np.sin(2 * np.pi * 440 * t) +  # A4 音 (440 Hz)
              0.5 * np.sin(2 * np.pi * 880 * t) +  # A5 音 (880 Hz)
              0.3 * np.sin(2 * np.pi * 1760 * t))  # A6 音 (1760 Hz)
    
    return signal, sample_rate

def main():
    """執行 STFT/iSTFT 分析示例。"""
    # 初始化處理器
    processor = STFTProcessor(
        window_size=2048,
        hop_length=512,
        window_type='hann',
        experiment_id=1
    )
    
    audio_loader = AudioLoader()
    plotter = SpectrogramPlotter(experiment_id=1)
    
    # 生成測試信號
    signal, sample_rate = generate_test_signal()
    
    # 先儲存原始音訊
    audio_loader.save_audio('original_audio.wav', signal, sample_rate)
    print("原始音訊已儲存為 original_audio.wav")
    
    # 執行 STFT
    stft_matrix = processor.stft(signal)
    print("STFT 轉換完成")
    
    # 繪製時頻譜圖
    spectrogram_path = plotter.plot_spectrogram(stft_matrix, sample_rate, processor.hop_length)
    print(f"時頻譜圖已儲存為: {spectrogram_path}")
    
    # 執行 iSTFT
    reconstructed_signal = processor.istft(stft_matrix)
    print("iSTFT 重構完成")
    
    # 計算信噪比
    snr = processor.compute_snr(signal, reconstructed_signal)
    print(f"重構信噪比 (SNR): {snr:.2f} dB")
    
    # 儲存重構的音訊
    audio_loader.save_audio('reconstructed_audio.wav', reconstructed_signal, sample_rate)
    print("重構音訊已儲存為 reconstructed_audio.wav")
    
    # 儲存分析結果
    data_path = processor.save_results(stft_matrix, snr)
    print(f"分析結果已儲存為: {data_path}")
    
    # 更新報告
    update_report(spectrogram_path, data_path, snr)
    print("報告已更新")

def update_report(spectrogram_path, data_path, snr):
    """更新實驗報告。

    Args:
        spectrogram_path (str): 時頻譜圖的檔案路徑。
        data_path (str): 數據檔案的路徑。
        snr (float): 信噪比。
    """
    report_path = "REPORT.md"
    
    if not os.path.exists(report_path):
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 音訊處理實驗報告\n\n")
    
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = "# 音訊處理實驗報告\n\n"
    
    import datetime
    new_entry = f"""
## STFT/iSTFT 分析 - {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

### 實驗結果
- 重構信噪比 (SNR): {snr:.2f} dB

### 時頻譜圖
![時頻譜圖](./{spectrogram_path})

### 相關檔案
- 原始音訊: [original_audio.wav](./original_audio.wav)
- 重構音訊: [reconstructed_audio.wav](./reconstructed_audio.wav)
- 分析數據: [{data_path}](./{data_path})

---
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content + new_entry)

if __name__ == "__main__":
    main()