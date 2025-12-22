# raw_feature_extractor.py
# STEP1 REAL LOGIC
# 20 日窗口原始特征提取

import numpy as np
from feature_window import get_feature_window

def extract_raw_features(code: str, pullup_date: str, data_dir: str = 'data/daily', window_size: int = 20) -> dict:
    info = get_feature_window(code, pullup_date, window_size, data_dir)
    df = info['window_df']
    close = df['close']
    volume = df['volume']
    features = {}
    features['price_mean_20d'] = close.mean()
    features['price_std_20d'] = close.std()
    features['price_max_20d'] = close.max()
    features['price_min_20d'] = close.min()
    features['price_return_20d'] = close.iloc[-1] / close.iloc[0] - 1
    features['volume_mean_20d'] = volume.mean()
    features['volume_std_20d'] = volume.std()
    features['volume_ratio_last'] = volume.iloc[-1] / volume.mean()
    features['price_position'] = (close.iloc[-1] - close.min()) / (close.max() - close.min() + 1e-6)
    features['t0'] = info['t0']
    features['window_size'] = window_size
    return features
