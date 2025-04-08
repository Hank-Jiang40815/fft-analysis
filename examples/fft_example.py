#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fft_analysis import FFTAnalyzer
import numpy as np

def main():
    """FFT 分析示例。"""
    # 創建 FFT 分析器實例
    analyzer = FFTAnalyzer(experiment_id=1)
    
    # 生成測試信號
    t, signal, target_freqs = analyzer.generate_signal(freq=5, duration=1, sampling_rate=1000)
    
    # 執行 FFT
    freq, magnitude = analyzer.perform_fft(signal, sampling_rate=1000)
    
    # 執行 iFFT
    fft_result = np.fft.fft(signal)
    reconstructed_signal = analyzer.perform_ifft(fft_result)
    
    # 計算誤差
    error = np.sqrt(np.mean((signal - reconstructed_signal) ** 2))
    print(f"重構誤差 (RMSE): {error:.10f}")
    
    # 繪製和保存結果
    image_path = analyzer.plot_results(t, signal, reconstructed_signal, freq, magnitude, target_freqs)
    data_path = analyzer.save_data(t, signal, reconstructed_signal, freq, magnitude, target_freqs)
    
    # 更新報告
    analyzer.update_report(image_path, data_path, error)

if __name__ == "__main__":
    main()