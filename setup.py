from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fft-analysis',
    version='0.1.0',
    author='姜翼顥',
    author_email='example@email.com',
    description='FFT 分析與梅爾頻譜處理工具包',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Hank-Jiang40815/fft-analysis',
    project_urls={
        'Bug Tracker': 'https://github.com/Hank-Jiang40815/fft-analysis/issues',
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.24.3',
        'matplotlib>=3.7.2',
        'markdown>=3.4.3',
        'librosa>=0.10.1',
        'scipy>=1.10.0'
    ],
)
