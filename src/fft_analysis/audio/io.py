#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import soundfile as sf
import numpy as np

class AudioLoader:
    """音訊檔案讀寫處理器。

    此類提供音訊檔案的讀取和保存功能。

    Attributes:
        supported_formats (list): 支援的音訊格式列表。
    """

    def __init__(self):
        """初始化音訊讀寫器。"""
        self.supported_formats = ['.wav', '.flac', '.ogg']

    def load_audio(self, file_path):
        """讀取音訊檔案。

        Args:
            file_path (str): 音訊檔案路徑。

        Returns:
            tuple: (音訊數據, 取樣率)。

        Raises:
            ValueError: 當檔案格式不支援時。
        """
        # 檢查檔案格式
        if not any(file_path.lower().endswith(fmt) for fmt in self.supported_formats):
            raise ValueError(f"Unsupported audio format. Supported formats: {self.supported_formats}")
        
        # 讀取音訊檔案
        audio_data, sample_rate = sf.read(file_path)
        
        # 確保音訊數據是單聲道
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        return audio_data, sample_rate

    def save_audio(self, file_path, audio_data, sample_rate):
        """保存音訊檔案。

        Args:
            file_path (str): 要保存的檔案路徑。
            audio_data (numpy.ndarray): 音訊數據。
            sample_rate (int): 取樣率。

        Raises:
            ValueError: 當檔案格式不支援時。
        """
        # 檢查檔案格式
        if not any(file_path.lower().endswith(fmt) for fmt in self.supported_formats):
            raise ValueError(f"Unsupported audio format. Supported formats: {self.supported_formats}")
        
        # 正規化音訊數據到 [-1, 1] 範圍
        audio_data = np.clip(audio_data, -1, 1)
        
        # 保存音訊檔案
        sf.write(file_path, audio_data, sample_rate)