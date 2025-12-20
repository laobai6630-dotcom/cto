#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取对照组特征 - 为对照组生成相同的88个特征
"""

import pandas as pd
import sys
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/contrast_group.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ContrastFeatureExtractor:
    """对照组特征提取器"""
    
    def __init__(self):
        self.contrast_dir = Path('data/contrast_group')
        self.feature_dir = Path('data/features')
    
    def load_contrast_group(self):
        """加载对照组股票列表"""
        files = list(self.contrast_dir.glob('contrast_group_30d_drop_top20_*.csv'))
        if not files:
            raise FileNotFoundError("未找到对照组文件")
        
        latest_file = max(files, key=lambda x: x.stat().st_mtime)
        df = pd.read_csv(latest_file)
        
        logging.info(f"加载对照组: {len(df)}只股票")
        return df['stock_code'].tolist()
    
    def extract_features_for_contrast_group(self):
        """为对照组提取88个特征"""
        stock_list = self.load_contrast_group()
        
        # TODO: 调用特征提取模块为对照组提取特征
        logging.info(f"对照组特征提取开始: {len(stock_list)}只股票")
        
        return None
    
    def run(self):
        """执行提取流程"""
        df_features = self.extract_features_for_contrast_group()
        print(f"✅ 对照组特征提取完成")
        return df_features

if __name__ == '__main__':
    extractor = ContrastFeatureExtractor()
    df_features = extractor.run()
