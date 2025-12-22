# upgrade_step1_real_features.py
# Step 1 修复版：真实 20 日窗口特征升级

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FEATURE_DIR = BASE_DIR / "features"

def upgrade_feature_window():
    path = FEATURE_DIR / "feature_window.py"
    code = (
        "# feature_window.py\n"
        "# STEP1 REAL LOGIC\n"
        "# 给定 code + pullup_date，返回 pullup_date 前 20 个交易日窗口\n\n"
        "import os\n"
        "import pandas as pd\n"
        "from typing import Dict\n\n"
        "def _load_daily_data(data_dir: str) -> pd.DataFrame:\n"
        "    files = sorted([f for f in os.listdir(data_dir) if f.endswith('.csv')])\n"
        "    dfs = []\n"
        "    for f in files:\n"
        "        df = pd.read_csv(os.path.join(data_dir, f))\n"
        "        dfs.append(df)\n"
        "    all_data = pd.concat(dfs, ignore_index=True)\n"
        "    all_data['date'] = pd.to_datetime(all_data['date'])\n"
        "    return all_data\n\n"
        "def get_feature_window(code: str, pullup_date: str, window_size: int = 20, data_dir: str = 'data/daily') -> Dict:\n"
        "    df = _load_daily_data(data_dir)\n"
        "    df = df[df['code'] == code].sort_values('date')\n"
        "    pullup_date = pd.to_datetime(pullup_date)\n"
        "    df = df[df['date'] < pullup_date]\n"
        "    if len(df) < window_size:\n"
        "        raise ValueError('历史数据不足 window_size')\n"
        "    window_df = df.tail(window_size)\n"
        "    return {\n"
        "        'code': code,\n"
        "        't0': window_df.iloc[-1]['date'].strftime('%Y-%m-%d'),\n"
        "        'window_df': window_df.reset_index(drop=True)\n"
        "    }\n"
    )
    path.write_text(code, encoding='utf-8')
    print(f' 已升级: {path}')

def upgrade_raw_feature_extractor():
    path = FEATURE_DIR / "raw_feature_extractor.py"
    code = (
        "# raw_feature_extractor.py\n"
        "# STEP1 REAL LOGIC\n"
        "# 20 日窗口原始特征提取\n\n"
        "import numpy as np\n"
        "from feature_window import get_feature_window\n\n"
        "def extract_raw_features(code: str, pullup_date: str, data_dir: str = 'data/daily', window_size: int = 20) -> dict:\n"
        "    info = get_feature_window(code, pullup_date, window_size, data_dir)\n"
        "    df = info['window_df']\n"
        "    close = df['close']\n"
        "    volume = df['volume']\n"
        "    features = {}\n"
        "    features['price_mean_20d'] = close.mean()\n"
        "    features['price_std_20d'] = close.std()\n"
        "    features['price_max_20d'] = close.max()\n"
        "    features['price_min_20d'] = close.min()\n"
        "    features['price_return_20d'] = close.iloc[-1] / close.iloc[0] - 1\n"
        "    features['volume_mean_20d'] = volume.mean()\n"
        "    features['volume_std_20d'] = volume.std()\n"
        "    features['volume_ratio_last'] = volume.iloc[-1] / volume.mean()\n"
        "    features['price_position'] = (close.iloc[-1] - close.min()) / (close.max() - close.min() + 1e-6)\n"
        "    features['t0'] = info['t0']\n"
        "    features['window_size'] = window_size\n"
        "    return features\n"
    )
    path.write_text(code, encoding='utf-8')
    print(f' 已升级: {path}')

if __name__ == "__main__":
    print(" 开始执行 Step 1：真实特征升级")
    upgrade_feature_window()
    upgrade_raw_feature_extractor()
    print(" Step 1 完成")
