#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import librosa
import matplotlib.pyplot as plt
import datetime
import json
import os

class MelSpectrogramAnalyzer:
    """梅爾頻譜分析器類別。

    此類別提供計算和視覺化梅爾頻譜的功能，適用於音訊信號分析。

    Attributes:
        n_mels (int): 梅爾濾波器的數量。
        fmin (float): 最小頻率（Hz）。
        fmax (float): 最大頻率（Hz）。
        experiment_id (int): 實驗編號。
        date (str): 實驗日期（YYYYMMDD格式）。
    """

    def __init__(self, n_mels=128, fmin=0.0, fmax=8000.0, experiment_id=1):
        """初始化梅爾頻譜分析器。

        Args:
            n_mels (int, optional): 梅爾濾波器的數量。預設為128。
            fmin (float, optional): 最小頻率（Hz）。預設為0.0。
            fmax (float, optional): 最大頻率（Hz）。預設為8000.0。
            experiment_id (int, optional): 實驗編號。預設為1。
        """
        self.n_mels = n_mels
        self.fmin = fmin
        self.fmax = fmax
        self.experiment_id = experiment_id
        self.date = datetime.datetime.now().strftime("%Y%m%d")

    def compute_melspectrogram(self, signal, sr):
        """計算輸入信號的梅爾頻譜。

        Args:
            signal (numpy.ndarray): 輸入的音訊信號。
            sr (int): 取樣率（Hz）。

        Returns:
            numpy.ndarray: 梅爾頻譜。
        """
        mel_spectrogram = librosa.feature.melspectrogram(
            y=signal, 
            sr=sr,
            n_mels=self.n_mels,
            fmin=self.fmin,
            fmax=self.fmax
        )
        
        # 轉換為分貝刻度
        mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
        return mel_spectrogram_db

    def plot_melspectrogram(self, mel_spectrogram, sr):
        """繪製梅爾頻譜圖。

        Args:
            mel_spectrogram (numpy.ndarray): 梅爾頻譜數據。
            sr (int): 取樣率（Hz）。

        Returns:
            str: 保存的圖片檔案路徑。
        """
        plt.figure(figsize=(12, 8))
        librosa.display.specshow(
            mel_spectrogram, 
            sr=sr,
            fmin=self.fmin,
            fmax=self.fmax,
            x_axis='time',
            y_axis='mel'
        )
        plt.colorbar(format='%+2.0f dB')
        plt.title(f'梅爾頻譜圖 - 實驗#{self.experiment_id}_{self.date}')
        
        filename = f'Mel_Spectrogram_Exp{self.experiment_id}_{self.date}.png'
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        
        return filename

    def save_data(self, mel_spectrogram, sr):
        """保存梅爾頻譜數據到JSON檔案。

        Args:
            mel_spectrogram (numpy.ndarray): 梅爾頻譜數據。
            sr (int): 取樣率（Hz）。

        Returns:
            str: 保存的數據檔案路徑。
        """
        data = {
            "experiment_id": self.experiment_id,
            "date": self.date,
            "n_mels": self.n_mels,
            "fmin": self.fmin,
            "fmax": self.fmax,
            "sampling_rate": sr,
            "mel_spectrogram": mel_spectrogram.tolist()
        }
        
        filename = f'Mel_Data_Exp{self.experiment_id}_{self.date}.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        return filename

    def update_report(self, image_path, data_path):
        """更新實驗報告。

        Args:
            image_path (str): 梅爾頻譜圖的檔案路徑。
            data_path (str): 數據檔案的路徑。
        """
        report_path = "REPORT.md"
        
        if not os.path.exists(report_path):
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("# 頻譜分析實驗報告\n\n")
        
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = "# 頻譜分析實驗報告\n\n"
        
        new_entry = f"""
## 梅爾頻譜分析 - 實驗 #{self.experiment_id} - {self.date}

### 實驗參數
- 梅爾濾波器數量: {self.n_mels}
- 頻率範圍: {self.fmin}Hz - {self.fmax}Hz
- 執行時間: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

![梅爾頻譜圖](./{image_path})

數據檔案: [{data_path}](./{data_path})

---
"""
        
        updated_content = content + new_entry
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
