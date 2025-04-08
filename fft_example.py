#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import json

# 用於自動生成實驗數據的全局變數
EXPERIMENT_ID = 1
EXPERIMENT_DATE = datetime.datetime.now().strftime("%Y%m%d")
REPORT_PATH = "REPORT.md"
SHOW_PLOTS = True  # 新增參數來控制是否顯示圖形

def generate_signal(freq=5, duration=1, sampling_rate=1000):
    """生成包含多個頻率組件的測試信號。

    Args:
        freq (int, optional): 基礎頻率，單位Hz。預設為5。
        duration (int, optional): 信號持續時間，單位秒。預設為1。
        sampling_rate (int, optional): 採樣率，單位Hz。預設為1000。

    Returns:
        tuple: 包含時間序列向量、信號向量和頻率向量的元組。
    """
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    # 生成包含多個頻率成分的信號
    signal = (np.sin(2 * np.pi * freq * t) + 
              0.5 * np.sin(2 * np.pi * 2 * freq * t) + 
              0.25 * np.sin(2 * np.pi * 3 * freq * t))
    
    return t, signal, [freq, 2*freq, 3*freq]

def perform_fft(signal, sampling_rate):
    """執行快速傅立葉變換(FFT)。

    Args:
        signal (numpy.ndarray): 輸入信號數據。
        sampling_rate (int): 信號的採樣率，單位Hz。

    Returns:
        tuple: 包含頻率向量和對應幅值的元組。
    """
    n = len(signal)
    # 執行FFT
    fft_result = np.fft.fft(signal)
    # 計算頻率向量
    freq = np.fft.fftfreq(n, 1/sampling_rate)
    # 計算正規化的幅值譜
    magnitude = np.abs(fft_result) / n * 2
    
    # 只返回正半部分頻率
    positive_freq_mask = freq >= 0
    return freq[positive_freq_mask], magnitude[positive_freq_mask]

def perform_ifft(fft_result):
    """執行逆快速傅立葉變換(iFFT)。

    Args:
        fft_result (numpy.ndarray): FFT變換後的複數結果。

    Returns:
        numpy.ndarray: 重構後的時域信號。
    """
    # 執行iFFT
    reconstructed_signal = np.fft.ifft(fft_result).real
    return reconstructed_signal

def plot_results(t, original_signal, reconstructed_signal, freq, magnitude, target_freqs):
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
    
    # 繪製原始信號
    ax1.plot(t, original_signal)
    ax1.set_title('原始信號 (Original Signal)')
    ax1.set_xlabel('時間 (s)')
    ax1.set_ylabel('振幅')
    ax1.grid(True)
    
    # 繪製頻譜 - 修正 stem 函數參數
    ax2.stem(freq, magnitude)  # 移除 use_line_collection 參數
    ax2.set_title('FFT 頻譜 (FFT Spectrum)')
    ax2.set_xlabel('頻率 (Hz)')
    ax2.set_ylabel('幅值')
    # 添加垂直線標示預期的頻率成分
    for f in target_freqs:
        ax2.axvline(x=f, color='r', linestyle='--', alpha=0.3)
    ax2.grid(True)
    # 顯示30Hz以內的頻率
    ax2.set_xlim(0, max(target_freqs) * 2)
    
    # 繪製重構信號
    ax3.plot(t, reconstructed_signal)
    ax3.set_title('重構信號 (Reconstructed Signal via iFFT)')
    ax3.set_xlabel('時間 (s)')
    ax3.set_ylabel('振幅')
    ax3.grid(True)
    
    # 設置圖表的總標題，包含實驗ID和日期
    fig.suptitle(f'FFT 與 iFFT 範例 - 實驗#{EXPERIMENT_ID}_{EXPERIMENT_DATE}_plot_results', 
                fontsize=16)
    
    # 保存圖片，檔名包含實驗ID和日期
    filename = f'FFT_Example_Exp{EXPERIMENT_ID}_{EXPERIMENT_DATE}_plot_results.png'
    plt.tight_layout()
    plt.savefig(filename)
    print(f"圖表已保存至: {filename}")
    
    # 顯示圖形 (新增)
    if SHOW_PLOTS:
        print("正在顯示圖表，請關閉視窗以繼續...")
        plt.show()
    else:
        plt.close()
    
    return filename

def save_data(t, original_signal, reconstructed_signal, freq, magnitude, target_freqs):
    """保存實驗數據到JSON文件。

    Args:
        t (numpy.ndarray): 時間序列。
        original_signal (numpy.ndarray): 原始信號數據。
        reconstructed_signal (numpy.ndarray): 通過iFFT重構的信號數據。
        freq (numpy.ndarray): 頻率向量。
        magnitude (numpy.ndarray): 對應的幅值向量。
        target_freqs (list): 輸入信號的目標頻率列表。

    Returns:
        str: 保存的數據文件路徑。
    """
    data = {
        "experiment_id": EXPERIMENT_ID,
        "date": EXPERIMENT_DATE,
        "target_frequencies": target_freqs,
        "time_series": t.tolist(),
        "original_signal": original_signal.tolist(),
        "reconstructed_signal": reconstructed_signal.tolist(),
        "fft_frequencies": freq.tolist(),
        "fft_magnitude": magnitude.tolist()
    }
    
    # 保存為JSON，檔名包含實驗ID和日期
    filename = f'FFT_Data_Exp{EXPERIMENT_ID}_{EXPERIMENT_DATE}_save_data.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    return filename

def update_report(image_path, data_path, error_metric):
    """更新中央報告文件。

    Args:
        image_path (str): 圖表文件路徑。
        data_path (str): 數據文件路徑。
        error_metric (float): 原始信號和重構信號之間的誤差度量。

    Returns:
        None
    """
    # 檢查報告文件是否存在
    if not os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write("# FFT 實驗報告\n\n")
    
    # 讀取現有報告內容
    try:
        with open(REPORT_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = "# FFT 實驗報告\n\n"
    
    # 准備新的報告內容
    new_entry = f"""
## 實驗 #{EXPERIMENT_ID} - {EXPERIMENT_DATE}

### FFT 和 iFFT 執行結果

- **執行時間**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **重構誤差**: {error_metric:.6f}

![FFT結果](./{image_path})

數據文件: [{data_path}](./{data_path})

---
"""
    
    # 添加新的實驗結果
    updated_content = content + new_entry
    
    # 寫回報告文件
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def explain_fft_ifft():
    """提供有關FFT和iFFT的簡要解釋。
    
    Returns:
        None
    """
    print("\n====== FFT 與 iFFT 簡介 ======")
    print("快速傅立葉變換 (FFT) 是一種高效計算離散傅立葉變換的算法。")
    print("它可以將時域信號轉換為頻域表示，揭示信號中的頻率成分。")
    print("\n關鍵概念:")
    print("1. FFT: 將時域信號轉換為頻域")
    print("2. iFFT: 將頻域信號轉換回時域")
    print("3. 頻譜分析: 識別信號中的頻率成分")
    print("4. 理想情況下，重構信號應與原始信號非常接近，誤差極小")
    print("\n本範例中:")
    print("- 我們生成了一個包含3個頻率成分的測試信號")
    print("- 使用FFT分析這個信號，顯示其頻譜")
    print("- 使用iFFT將頻域表示轉換回時域信號")
    print("- 比較原始信號和重構信號以評估準確性")
    print("============================\n")

def main():
    """主函數：執行FFT和iFFT示範並記錄結果。"""
    print(f"執行 FFT/iFFT 範例 - 實驗 #{EXPERIMENT_ID} - {EXPERIMENT_DATE}")
    
    # 提供簡要的FFT和iFFT解釋
    explain_fft_ifft()
    
    # 1. 生成測試信號
    sampling_rate = 1000  # Hz
    t, signal, target_freqs = generate_signal(freq=5, duration=1, sampling_rate=sampling_rate)
    
    # 2. 執行FFT
    freq, magnitude = perform_fft(signal, sampling_rate)
    
    # 3. 執行完整的FFT (包括正負頻率)以便於之後的iFFT
    n = len(signal)
    fft_result = np.fft.fft(signal)
    
    # 4. 執行iFFT重構信號
    reconstructed_signal = perform_ifft(fft_result)
    
    # 5. 計算誤差 (重構信號和原始信號之間的均方根誤差)
    error = np.sqrt(np.mean((signal - reconstructed_signal) ** 2))
    print(f"重構誤差 (RMSE): {error:.10f}")
    
    # 6. 繪製結果
    image_path = plot_results(t, signal, reconstructed_signal, freq, magnitude, target_freqs)
    
    # 7. 保存數據
    data_path = save_data(t, signal, reconstructed_signal, freq, magnitude, target_freqs)
    print(f"數據已保存至: {data_path}")
    
    # 8. 更新報告
    update_report(image_path, data_path, error)
    print(f"已更新報告: {REPORT_PATH}")

if __name__ == "__main__":
    main()