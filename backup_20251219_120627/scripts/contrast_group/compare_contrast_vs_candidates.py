#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对比分析 - 对照组特征 vs 候选股票特征对比
输出: 分离度评分（Separation Score）
"""

import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean, cosine
import json
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    filename='logs/contrast_group.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ContrastComparator:
    """对照组对比分析器"""
    
    def __init__(self):
        self.contrast_dir = Path('data/contrast_group')
        self.feature_dir = Path('data/features')
        self.output_dir = Path('data/analysis')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_features(self):
        """加载对照组和候选股票特征"""
        df_contrast = pd.read_csv(self.contrast_dir / 'contrast_group_features_88.csv')
        df_candidates = pd.read_csv(self.feature_dir / 'all_features_88.csv')
        
        return df_contrast, df_candidates
    
    def calculate_feature_separation(self, df_contrast, df_candidates):
        """计算特征分离度"""
        feature_cols = [col for col in df_contrast.columns if col not in ['stock_code', 'date']]
        
        contrast_mean = df_contrast[feature_cols].mean().values
        candidates_mean = df_candidates[feature_cols].mean().values
        
        euclidean_dist = euclidean(contrast_mean, candidates_mean)
        cosine_dist = cosine(contrast_mean, candidates_mean)
        
        return {
            'euclidean_distance': float(euclidean_dist),
            'cosine_distance': float(cosine_dist)
        }
    
    def calculate_separation_score(self, distances):
        """计算综合分离度评分（0-1，越高越好）"""
        euclidean_score = min(distances['euclidean_distance'] / 10, 1.0)
        cosine_score = distances['cosine_distance']
        
        separation_score = euclidean_score * 0.5 + cosine_score * 0.5
        
        return float(separation_score)
    
    def run_comparison(self):
        """执行完整对比分析"""
        df_contrast, df_candidates = self.load_features()
        
        distances = self.calculate_feature_separation(df_contrast, df_candidates)
        separation_score = self.calculate_separation_score(distances)
        
        results = {
            'comparison_date': datetime.now().strftime('%Y-%m-%d'),
            'contrast_group_size': len(df_contrast),
            'candidates_size': len(df_candidates),
            'distances': distances,
            'separation_score': separation_score
        }
        
        output_file = self.output_dir / 'contrast_vs_candidates_comparison.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logging.info(f"对比分析完成: {output_file}")
        logging.info(f"分离度评分: {separation_score:.4f}")
        
        print(f"\n✅ 对比分析完成:")
        print(f"  📊 分离度评分: {separation_score:.4f}")
        
        return results

if __name__ == '__main__':
    comparator = ContrastComparator()
    results = comparator.run_comparison()
