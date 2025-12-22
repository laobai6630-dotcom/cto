# feature_window.py
# STEP1 REAL LOGIC
# 给定 code + pullup_date，返回 pullup_date 前 20 个交易日窗口

import os
import pandas as pd
from typing import Dict

def _load_daily_data(data_dir: str) -> pd.DataFrame:
    files = sorted([f for f in os.listdir(data_dir) if f.endswith('.csv')])
    dfs = []
    for f in files:
        df = pd.read_csv(os.path.join(data_dir, f))
        dfs.append(df)
    all_data = pd.concat(dfs, ignore_index=True)
    all_data['date'] = pd.to_datetime(all_data['date'])
    return all_data

def get_feature_window(code: str, pullup_date: str, window_size: int = 20, data_dir: str = 'data/daily') -> Dict:
    df = _load_daily_data(data_dir)
    df = df[df['code'] == code].sort_values('date')
    pullup_date = pd.to_datetime(pullup_date)
    df = df[df['date'] < pullup_date]
    if len(df) < window_size:
        raise ValueError('历史数据不足 window_size')
    window_df = df.tail(window_size)
    return {
        'code': code,
        't0': window_df.iloc[-1]['date'].strftime('%Y-%m-%d'),
        'window_df': window_df.reset_index(drop=True)
    }
