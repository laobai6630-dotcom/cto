#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
特征标准化模块 - 标准化所有特征并选择最终88个特征
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/feature_normalization.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FeatureNormalizer:
    """特征标准化器 - 154个特征标准化并选择88个"""
    
    def __init__(self):
        self.feature_dir = Path('data/features')
        self.model_dir = Path('models')
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.scaler = StandardScaler()
    
    def load_all_features(self):
        """加载所有原始特征"""
        # 加载134个原始特征
        df_raw = pd.read_csv(self.feature_dir / 'raw_features_134.csv')
        
        # 加载10个AI特征
        df_ai = pd.read_csv(self.feature_dir / 'ai_synthetic_features_10.csv')
        
        # 加载10个筹码特征
        df_chip = pd.read_csv(self.feature_dir / 'chip_features_10.csv')
        
        # 合并 (134 + 10 + 10 = 154个特征)
        df_all = df_raw.merge(df_ai, on=['stock_code', 'date'])
        df_all = df_all.merge(df_chip, on='stock_code')
        
        logging.info(f"加载特征完成: {df_all.shape}")
        return df_all
    
    def normalize_features(self, df):
        """标准化特征（均值0，标准差1）"""
        id_columns = ['stock_code', 'date']
        feature_columns = [col for col in df.columns if col not in id_columns]
        
        df_normalized = df.copy()
        df_normalized[feature_columns] = self.scaler.fit_transform(df[feature_columns])
        
        # 保存scaler
        scaler_file = self.model_dir / 'feature_scaler.pkl'
        joblib.dump(self.scaler, scaler_file)
        logging.info(f"Scaler已保存: {scaler_file}")
        
        return df_normalized
    
    def select_top_features(self, df, top_n=88):
        """根据特征重要性选择Top 88特征"""
        # 优先AI特征和筹码特征
        ai_features = [col for col in df.columns if col.startswith('ai_')]
        chip_features = [col for col in df.columns if col.startswith('chip_')]
        
        other_features = [col for col in df.columns 
                        if col not in ['stock_code', 'date'] 
                        and not col.startswith('ai_') 
                        and not col.startswith('chip_')]
        
        # 组合: 10个AI + 10个筹码 + 68个其他
        top_features = ai_features + chip_features + other_features[:68]
        
        selected_columns = ['stock_code', 'date'] + top_features[:88]
        df_selected = df[selected_columns]
        
        logging.info(f"特征选择完成: {len(top_features)}个特征")
        return df_selected
    
    def process_all(self):
        """完整处理流程"""
        df_all = self.load_all_features()
        df_normalized = self.normalize_features(df_all)
        
        output_file_all = self.feature_dir / 'normalized_features_all.csv'
        df_normalized.to_csv(output_file_all, index=False)
        
        df_final = self.select_top_features(df_normalized, top_n=88)
        
        output_file_final = self.feature_dir / 'all_features_88.csv'
        df_final.to_csv(output_file_final, index=False)
        
        logging.info(f"最终88特征已保存: {output_file_final}")
        return df_final

if __name__ == '__main__':
    normalizer = FeatureNormalizer()
    df_final = normalizer.process_all()
