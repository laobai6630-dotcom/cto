#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路径配置文件 - 统一管理所有项目路径
"""

import os
from pathlib import Path

# ============ 项目根目录 ============
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # D:\cto\ (Git仓库根目录)
PROJECT_SCRIPTS = PROJECT_ROOT / "projects" / "山脚下" / "scripts"

# ============ 采集程序路径（保留原样） ============
COLLECTION_ROOT = PROJECT_ROOT  # D:\cto\ 根目录
COLLECT_DAILY_MINUTE_PY = COLLECTION_ROOT / "日线和分钟线数据获取.py"
COLLECT_WEEKLY_PY = COLLECTION_ROOT / "周线数据获取.py"
COLLECT_MONTHLY_PY = COLLECTION_ROOT / "月线数据获取.py"
COLLECT_FINANCIAL_PY = COLLECTION_ROOT / "财务和基本面数据获取.py"

# ============ 数据输出路径（原始数据） ============
DATA_ROOT = PROJECT_ROOT  # 所有数据文件夹在 D:\cto\ 根目录
DAILY_DATA_DIR = DATA_ROOT / "daily_minute_data"
WEEKLY_DATA_DIR = DATA_ROOT / "weekly_data"
MONTHLY_DATA_DIR = DATA_ROOT / "monthly_data"
FINANCIAL_DATA_DIR = DATA_ROOT / "financial_data"

# ============ 特征提取程序路径 ============
FEATURE_ENGINEERING_DIR = PROJECT_SCRIPTS / "feature_engineering"
MODEL_DIR = PROJECT_SCRIPTS / "ml_training"
FILTERING_DIR = PROJECT_SCRIPTS / "filtering"
TRACKING_DIR = PROJECT_SCRIPTS / "tracking"

# ============ 日志路径 ============
LOGS_DIR = PROJECT_ROOT / "projects" / "山脚下" / "logs"
SCHEDULER_MAIN_LOG = LOGS_DIR / "scheduler_main.log"
SCHEDULER_FINANCIAL_LOG = LOGS_DIR / "scheduler_financial.log"

# ============ 调度程序路径 ============
SCHEDULER_MAIN_PY = PROJECT_SCRIPTS / "data_collection" / "scheduler_main.py"
SCHEDULER_FINANCIAL_PY = PROJECT_SCRIPTS / "data_collection" / "scheduler_financial.py"

# ============ 验证路径存在 ============
def verify_paths():
    """验证所有必要的路径是否存在"""
    required_dirs = [
        DAILY_DATA_DIR,
        WEEKLY_DATA_DIR,
        MONTHLY_DATA_DIR,
        FINANCIAL_DATA_DIR,
        LOGS_DIR,
        FEATURE_ENGINEERING_DIR,
    ]
    
    required_files = [
        COLLECT_DAILY_MINUTE_PY,
        COLLECT_WEEKLY_PY,
        COLLECT_MONTHLY_PY,
        COLLECT_FINANCIAL_PY,
    ]
    
    missing_dirs = [d for d in required_dirs if not d.exists()]
    missing_files = [f for f in required_files if not f.exists()]
    
    if missing_dirs:
        print(f"⚠️  缺失目录: {[str(d) for d in missing_dirs]}")
        for d in missing_dirs:
            d.mkdir(parents=True, exist_ok=True)
            print(f"✅ 已创建目录: {d}")
    
    if missing_files:
        print(f"❌ 缺失文件: {[str(f) for f in missing_files]}")
        raise FileNotFoundError(f"Missing files: {missing_files}")
    
    print("✅ 所有路径验证通过")

if __name__ == "__main__":
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"日志目录: {LOGS_DIR}")
    print(f"数据目录: {DATA_ROOT}")
    print()
    verify_paths()
