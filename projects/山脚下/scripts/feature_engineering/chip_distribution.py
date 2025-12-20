#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
筹码分布模块 - 计算10个筹码特征
权重: 0.2（在相似度筛选中）
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/chip_distribution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ChipDistributionAnalyzer:
    """筹码分布分析器 - 计算10个筹码特征"""
    
    def __init__(self):
        self.feature_dir = Path('data/features')
        self.feature_dir.mkdir(parents=True, exist_ok=True)
    
    def calculate_chip_concentration(self, df_price):
        """计算筹码集中度"""
        df_price['turnover'] = df_price['close'] * df_price['volume']
        total_turnover = df_price['turnover'].sum()
        
        chip_dist = df_price.groupby('close')['turnover'].sum() / total_turnover
        top_20_chips = chip_dist.nlargest(int(len(chip_dist) * 0.2)).sum()
        
        return top_20_chips
    
    def calculate_chip_lock_ratio(self, df_price):
        """计算筹码锁定率"""
        avg_volume = df_price['volume'].mean()
        low_volume_days = df_price[df_price['volume'] < avg_volume * 0.5]
        lock_ratio = len(low_volume_days) / len(df_price)
        
        return lock_ratio
    
    # ... 其他8个筹码特征计算方法
    
    def extract_all_chip_features(self, stock_code, df_price):
        """提取所有10个筹码特征"""
        features = {
            'stock_code': stock_code,
            'chip_concentration': self.calculate_chip_concentration(df_price),
            'chip_lock_ratio': self.calculate_chip_lock_ratio(df_price),
            # ... 其他8个筹码特征
        }
        
        return features

if __name__ == '__main__':
    analyzer = ChipDistributionAnalyzer()
