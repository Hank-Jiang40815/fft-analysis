"""FFT Analysis Package.

這個套件提供了快速傅立葉變換(FFT)和梅爾頻譜分析的功能。

Examples:
    基本 FFT 分析：
    >>> from fft_analysis import FFTAnalyzer
    >>> analyzer = FFTAnalyzer()
    >>> signal = analyzer.generate_signal()
    >>> freq, magnitude = analyzer.perform_fft(signal)

    梅爾頻譜分析：
    >>> from fft_analysis import MelSpectrogramAnalyzer
    >>> mel_analyzer = MelSpectrogramAnalyzer()
    >>> mel_spectrogram = mel_analyzer.compute_melspectrogram(signal, sr=22050)
"""

from .fft import FFTAnalyzer
from .mel_spectrogram import MelSpectrogramAnalyzer

__version__ = '0.1.0'
__author__ = '姜翼顥'
__email__ = 'example@email.com'

__all__ = ['FFTAnalyzer', 'MelSpectrogramAnalyzer']
