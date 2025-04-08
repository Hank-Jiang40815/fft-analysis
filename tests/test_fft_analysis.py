#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np
from fft_analysis import FFTAnalyzer, MelSpectrogramAnalyzer

class TestFFTAnalyzer(unittest.TestCase):
    """FFT分析器的單元測試。"""
    
    def setUp(self):
        """測試前的準備工作。"""
        self.analyzer = FFTAnalyzer(experiment_id=999)
    
    def test_signal_generation(self):
        """測試信號生成功能。"""
        t, signal, freqs = self.analyzer.generate_signal()
        self.assertEqual(len(t), 1000)
        self.assertEqual(len(signal), 1000)
        self.assertEqual(freqs, [5, 10, 15])
    
    def test_fft_ifft(self):
        """測試FFT和iFFT功能。"""
        # 生成簡單的測試信號
        t = np.linspace(0, 1, 1000)
        original_signal = np.sin(2 * np.pi * 10 * t)
        
        # 執行FFT
        freq, magnitude = self.analyzer.perform_fft(original_signal, 1000)
        
        # 檢查頻率範圍
        self.assertTrue(np.max(freq) <= 500)  # Nyquist頻率
        
        # 執行完整的FFT用於iFFT
        fft_result = np.fft.fft(original_signal)
        reconstructed = self.analyzer.perform_ifft(fft_result)
        
        # 檢查重構誤差
        error = np.mean(np.abs(original_signal - reconstructed))
        self.assertLess(error, 1e-10)

class TestMelSpectrogramAnalyzer(unittest.TestCase):
    """梅爾頻譜分析器的單元測試。"""
    
    def setUp(self):
        """測試前的準備工作。"""
        self.analyzer = MelSpectrogramAnalyzer(
            n_mels=128,
            fmin=0.0,
            fmax=8000.0,
            experiment_id=999
        )
    
    def test_melspectrogram_computation(self):
        """測試梅爾頻譜計算功能。"""
        # 生成簡單的測試信號
        duration = 1.0
        sr = 22050
        t = np.linspace(0, duration, int(sr * duration))
        signal = np.sin(2 * np.pi * 440 * t)
        
        # 計算梅爾頻譜
        mel_spec = self.analyzer.compute_melspectrogram(signal, sr)
        
        # 檢查輸出形狀
        self.assertEqual(mel_spec.shape[0], 128)  # n_mels
        self.assertTrue(mel_spec.shape[1] > 0)    # 時間幀數

if __name__ == '__main__':
    unittest.main()