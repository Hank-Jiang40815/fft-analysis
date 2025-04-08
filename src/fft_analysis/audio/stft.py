#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal as signal
import datetime
import json

class STFTProcessor:
    """短時傅立葉轉換處理器。

    此類提供音訊信號的 STFT 和 iSTFT 功能，支援多種視窗函數和參數設定。

    Attributes:
        window_size (int): 視窗大小（採樣點數）。
        hop_length (int): 視窗移動步長。
        window_type (str): 視窗函數類型。
        experiment_id (int): 實驗編號。
        date (str): 實驗日期（YYYYMMDD格式）。
    """

    def __init__(self, window_size=2048, hop_length=512, window_type='hann', experiment_id=1):
        """初始化 STFT 處理器。

        Args:
            window_size (int, optional): 視窗大小。預設為2048。
            hop_length (int, optional): 視窗移動步長。預設為512。
            window_type (str, optional): 視窗函數類型。預設為'hann'。
            experiment_id (int, optional): 實驗編號。預設為1。
        """
        self.window_size = window_size
        self.hop_length = hop_length
        self.window_type = window_type
        self.experiment_id = experiment_id
        self.date = datetime.datetime.now().strftime("%Y%m%d")
        
        # 創建視窗函數
        self.window = self._get_window()

    def _get_window(self):
        """獲取指定類型的視窗函數。

        Returns:
            numpy.ndarray: 視窗函數數組。

        Raises:
            ValueError: 當指定的視窗類型不支援時。
        """
        supported_windows = ['hann', 'hamming', 'blackman', 'bartlett']
        if self.window_type not in supported_windows:
            raise ValueError(f"Unsupported window type. Supported types: {supported_windows}")
        
        return signal.get_window(self.window_type, self.window_size)

    def stft(self, audio_signal):
        """執行短時傅立葉轉換。

        Args:
            audio_signal (numpy.ndarray): 輸入的音訊信號。

        Returns:
            numpy.ndarray: STFT 頻譜圖（複數值）。
        """
        # 計算需要的幀數
        num_frames = 1 + (len(audio_signal) - self.window_size) // self.hop_length
        
        # 初始化 STFT 矩陣
        stft_matrix = np.zeros((self.window_size, num_frames), dtype=np.complex128)
        
        # 執行 STFT
        for i in range(num_frames):
            # 提取當前幀
            start = i * self.hop_length
            end = start + self.window_size
            frame = audio_signal[start:end]
            
            # 應用視窗函數並執行 FFT
            windowed_frame = frame * self.window
            stft_matrix[:, i] = np.fft.fft(windowed_frame)
        
        return stft_matrix

    def istft(self, stft_matrix):
        """執行逆短時傅立葉轉換。

        Args:
            stft_matrix (numpy.ndarray): STFT 頻譜圖（複數值）。

        Returns:
            numpy.ndarray: 重構的音訊信號。
        """
        num_frames = stft_matrix.shape[1]
        expected_signal_length = (num_frames - 1) * self.hop_length + self.window_size
        
        # 初始化輸出信號和重疊相加的權重
        output_signal = np.zeros(expected_signal_length)
        window_sum = np.zeros(expected_signal_length)
        
        # 對每一幀執行 iFFT 並重疊相加
        for i in range(num_frames):
            # 執行 iFFT
            frame = np.real(np.fft.ifft(stft_matrix[:, i]))
            
            # 應用視窗函數
            frame = frame * self.window
            
            # 計算當前幀的位置
            start = i * self.hop_length
            end = start + self.window_size
            
            # 重疊相加
            output_signal[start:end] += frame
            window_sum[start:end] += self.window
        
        # 處理重疊部分的權重
        window_sum[window_sum < 1e-6] = 1
        output_signal /= window_sum
        
        return output_signal

    def compute_snr(self, original_signal, reconstructed_signal):
        """計算信噪比（SNR）。

        Args:
            original_signal (numpy.ndarray): 原始信號。
            reconstructed_signal (numpy.ndarray): 重構信號。

        Returns:
            float: 信噪比（dB）。
        """
        # 確保信號長度相同
        min_length = min(len(original_signal), len(reconstructed_signal))
        original_signal = original_signal[:min_length]
        reconstructed_signal = reconstructed_signal[:min_length]
        
        # 計算信噪比
        noise = original_signal - reconstructed_signal
        snr = 10 * np.log10(np.sum(original_signal**2) / np.sum(noise**2))
        
        return snr

    def save_results(self, stft_matrix, snr):
        """保存 STFT 分析結果。

        Args:
            stft_matrix (numpy.ndarray): STFT 頻譜圖。
            snr (float): 信噪比。

        Returns:
            str: 保存的檔案路徑。
        """
        data = {
            "experiment_id": self.experiment_id,
            "date": self.date,
            "window_size": self.window_size,
            "hop_length": self.hop_length,
            "window_type": self.window_type,
            "snr": float(snr),
            "stft_shape": stft_matrix.shape,
            # 儲存複數值的實部和虛部
            "stft_real": stft_matrix.real.tolist(),
            "stft_imag": stft_matrix.imag.tolist()
        }
        
        filename = f'STFT_Data_Exp{self.experiment_id}_{self.date}.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        return filename