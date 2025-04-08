#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

class SpectrogramPlotter:
    """時頻譜圖繪製器。

    此類提供 STFT 時頻譜圖的視覺化功能。

    Attributes:
        experiment_id (int): 實驗編號。
        date (str): 實驗日期（YYYYMMDD格式）。
    """

    def __init__(self, experiment_id=1):
        """初始化時頻譜圖繪製器。

        Args:
            experiment_id (int, optional): 實驗編號。預設為1。
        """
        self.experiment_id = experiment_id
        self.date = datetime.datetime.now().strftime("%Y%m%d")

    def plot_spectrogram(self, stft_matrix, sample_rate, hop_length):
        """繪製時頻譜圖。

        Args:
            stft_matrix (numpy.ndarray): STFT 頻譜圖。
            sample_rate (int): 取樣率。
            hop_length (int): STFT 的視窗移動步長。

        Returns:
            str: 保存的圖片檔案路徑。
        """
        # 計算時間和頻率軸
        time = np.arange(stft_matrix.shape[1]) * hop_length / sample_rate
        freq = np.fft.fftfreq(stft_matrix.shape[0], 1/sample_rate)
        
        # 轉換為分貝刻度
        magnitude_db = 20 * np.log10(np.abs(stft_matrix) + 1e-10)
        
        # 繪製時頻譜圖
        plt.figure(figsize=(12, 8))
        plt.imshow(
            magnitude_db,
            aspect='auto',
            origin='lower',
            extent=[time[0], time[-1], freq[0], freq[-1]]
        )
        
        plt.colorbar(label='Magnitude (dB)')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title(f'STFT Spectrogram - Exp#{self.experiment_id}_{self.date}')
        
        # 保存圖片
        filename = f'STFT_Spectrogram_Exp{self.experiment_id}_{self.date}.png'
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        
        return filename