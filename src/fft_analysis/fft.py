#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import json

class FFTAnalyzer:
    """FFT分析器類別。

    此類別提供快速傅立葉變換(FFT)和逆變換(iFFT)的功能。

    Attributes:
        experiment_id (int): 實驗編號。
        date (str): 實驗日期（YYYYMMDD格式）。
    """

    def __init__(self, experiment_id=1):
        """初始化FFT分析器。

        Args:
            experiment_id (int, optional): 實驗編號。預設為1。
        """
        self.experiment_id = experiment_id
        self.date = datetime.datetime.now().strftime("%Y%m%d")

    def generate_signal(self, freq=5, duration=1, sampling_rate=1000):
        """生成包含多個頻率組件的測試信號。

        Args:
            freq (int, optional): 基礎頻率，單位Hz。預設為5。
            duration (int, optional): 信號持續時間，單位秒。預設為1。
            sampling_rate (int, optional): 採樣率，單位Hz。預設為1000。

        Returns:
            tuple: 包含時間序列向量、信號向量和頻率向量的元組。
        """
        t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
        signal = (np.sin(2 * np.pi * freq * t) + 
                0.5 * np.sin(2 * np.pi * 2 * freq * t) + 
                0.25 * np.sin(2 * np.pi * 3 * freq * t))
        
        return t, signal, [freq, 2*freq, 3*freq]

    def perform_fft(self, signal, sampling_rate):
        """執行快速傅立葉變換(FFT)。

        Args:
            signal (numpy.ndarray): 輸入信號數據。
            sampling_rate (int): 信號的採樣率，單位Hz。

        Returns:
            tuple: 包含頻率向量和對應幅值的元組。
        """
        n = len(signal)
        fft_result = np.fft.fft(signal)
        freq = np.fft.fftfreq(n, 1/sampling_rate)
        magnitude = np.abs(fft_result) / n * 2
        
        positive_freq_mask = freq >= 0
        return freq[positive_freq_mask], magnitude[positive_freq_mask]

    def perform_ifft(self, fft_result):
        """執行逆快速傅立葉變換(iFFT)。

        Args:
            fft_result (numpy.ndarray): FFT變換後的複數結果。

        Returns:
            numpy.ndarray: 重構後的時域信號。
        """
        return np.fft.ifft(fft_result).real

    def plot_results(self, t, original_signal, reconstructed_signal, freq, magnitude, target_freqs):
        """繪製原始信號、FFT頻譜和重構信號的圖表。

        Args:
            t (numpy.ndarray): 時間序列。
            original_signal (numpy.ndarray): 原始信號數據。
            reconstructed_signal (numpy.ndarray): 通過iFFT重構的信號數據。
            freq (numpy.ndarray): 頻率向量。
            magnitude (numpy.ndarray): 對應的幅值向量。
            target_freqs (list): 輸入信號的目標頻率列表。

        Returns:
            str: 保存的圖表文件路徑。
        """
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        ax1.plot(t, original_signal)
        ax1.set_title('原始信號 (Original Signal)')
        ax1.set_xlabel('時間 (s)')
        ax1.set_ylabel('振幅')
        ax1.grid(True)
        
        ax2.stem(freq, magnitude)
        ax2.set_title('FFT 頻譜 (FFT Spectrum)')
        ax2.set_xlabel('頻率 (Hz)')
        ax2.set_ylabel('幅值')
        for f in target_freqs:
            ax2.axvline(x=f, color='r', linestyle='--', alpha=0.3)
        ax2.grid(True)
        ax2.set_xlim(0, max(target_freqs) * 2)
        
        ax3.plot(t, reconstructed_signal)
        ax3.set_title('重構信號 (Reconstructed Signal via iFFT)')
        ax3.set_xlabel('時間 (s)')
        ax3.set_ylabel('振幅')
        ax3.grid(True)
        
        fig.suptitle(f'FFT 與 iFFT 範例 - 實驗#{self.experiment_id}_{self.date}_plot_results', 
                    fontsize=16)
        
        filename = f'FFT_Example_Exp{self.experiment_id}_{self.date}_plot_results.png'
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        
        return filename

    def save_data(self, t, original_signal, reconstructed_signal, freq, magnitude, target_freqs):
        """保存實驗數據到JSON檔案。

        Args:
            t (numpy.ndarray): 時間序列。
            original_signal (numpy.ndarray): 原始信號數據。
            reconstructed_signal (numpy.ndarray): 通過iFFT重構的信號數據。
            freq (numpy.ndarray): 頻率向量。
            magnitude (numpy.ndarray): 對應的幅值向量。
            target_freqs (list): 輸入信號的目標頻率列表。

        Returns:
            str: 保存的數據檔案路徑。
        """
        data = {
            "experiment_id": self.experiment_id,
            "date": self.date,
            "target_frequencies": target_freqs,
            "time_series": t.tolist(),
            "original_signal": original_signal.tolist(),
            "reconstructed_signal": reconstructed_signal.tolist(),
            "fft_frequencies": freq.tolist(),
            "fft_magnitude": magnitude.tolist()
        }
        
        filename = f'FFT_Data_Exp{self.experiment_id}_{self.date}_save_data.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        return filename

    def update_report(self, image_path, data_path, error_metric):
        """更新實驗報告。

        Args:
            image_path (str): 圖表文件路徑。
            data_path (str): 數據檔案路徑。
            error_metric (float): 原始信號和重構信號之間的誤差度量。
        """
        report_path = "REPORT.md"
        
        if not os.path.exists(report_path):
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("# FFT 實驗報告\n\n")
        
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = "# FFT 實驗報告\n\n"
        
        new_entry = f"""
## 實驗 #{self.experiment_id} - {self.date}

### FFT 和 iFFT 執行結果

- **執行時間**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **重構誤差**: {error_metric:.6f}

![FFT結果](./{image_path})

數據檔案: [{data_path}](./{data_path})

---
"""
        
        updated_content = content + new_entry
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
