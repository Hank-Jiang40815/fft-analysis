#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fft_analysis import MelSpectrogramAnalyzer

def generate_test_signal(duration=1.0, sr=22050):
    """生成測試用的音訊信號。

    Args:
        duration (float, optional): 信號持續時間（秒）。預設為1.0。
        sr (int, optional): 取樣率（Hz）。預設為22050。

    Returns:
        tuple: (信號數據, 取樣率)。
    """
    import numpy as np
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    signal = (np.sin(2 * np.pi * 440 * t) +  # 440 Hz (A4音)
             0.5 * np.sin(2 * np.pi * 880 * t) +  # 880 Hz (A5音)
             0.25 * np.sin(2 * np.pi * 1760 * t))  # 1760 Hz (A6音)
    
    return signal, sr

def main():
    """梅爾頻譜分析示例。"""
    # 創建梅爾頻譜分析器實例
    analyzer = MelSpectrogramAnalyzer(
        n_mels=128,
        fmin=0.0,
        fmax=8000.0,
        experiment_id=1
    )
    
    # 生成測試信號
    signal, sr = generate_test_signal()
    
    # 計算梅爾頻譜
    mel_spectrogram = analyzer.compute_melspectrogram(signal, sr)
    
    # 繪製和保存頻譜圖
    image_path = analyzer.plot_melspectrogram(mel_spectrogram, sr)
    print(f"頻譜圖已保存至: {image_path}")
    
    # 保存數據
    data_path = analyzer.save_data(mel_spectrogram, sr)
    print(f"數據已保存至: {data_path}")
    
    # 更新報告
    analyzer.update_report(image_path, data_path)
    print("報告已更新")

if __name__ == "__main__":
    main()