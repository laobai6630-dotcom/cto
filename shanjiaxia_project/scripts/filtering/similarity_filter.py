#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
相似度筛选主程序
权重: ML模型(0.6) + 筹码分布(0.2) + 消息面(0.2)
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/filtering.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SimilarityFilter:
    """相似度筛选器"""
    
    def __init__(self):
        self.model_dir = Path('models')
        self.feature_dir = Path('data/features')
        self.config_dir = Path('config')
        self.output_dir = Path('data/candidates')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.weights = self.load_weights()
    
    def load_weights(self):
        """加载权重配置"""
        weights_file = self.config_dir / 'weights.json'
        if weights_file.exists():
            with open(weights_file, 'r') as f:
                return json.load(f)
        else:
            return {
                'ml_model': 0.6,
                'chip_distribution': 0.2,
                'news_sentiment': 0.2
            }
    
    def load_candidates(self):
        """加载候选股票"""
        df = pd.read_csv(self.feature_dir / 'all_features_88.csv')
        return df
    
    def calculate_ml_similarity(self, df):
        """计算ML模型相似度"""
        model = joblib.load(self.model_dir / 'model_ensemble.pkl')
        
        X = df.drop(['stock_code', 'date'], axis=1)
        similarity = model.predict_proba(X)
        
        return similarity
    
    def calculate_chip_similarity(self, df):
        """计算筹码分布相似度"""
        chip_features = [col for col in df.columns if col.startswith('chip_')]
        
        if len(chip_features) == 0:
            return np.ones(len(df))
        
        chip_scores = df[chip_features].mean(axis=1).values
        chip_scores = (chip_scores - chip_scores.min()) / (chip_scores.max() - chip_scores.min() + 1e-10)
        
        return chip_scores
    
    def calculate_news_similarity(self, df):
        """计算消息面相似度（由消息面分析员提供）"""
        # TODO: 从消息面分析模块获取评分
        return np.ones(len(df)) * 0.5
    
    def calculate_combined_similarity(self, df):
        """计算综合相似度"""
        ml_sim = self.calculate_ml_similarity(df)
        chip_sim = self.calculate_chip_similarity(df)
        news_sim = self.calculate_news_similarity(df)
        
        combined_sim = (
            ml_sim * self.weights['ml_model'] +
            chip_sim * self.weights['chip_distribution'] +
            news_sim * self.weights['news_sentiment']
        )
        
        return combined_sim, ml_sim, chip_sim, news_sim
    
    def filter_candidates(self, threshold=0.5):
        """根据阈值筛选候选股票"""
        df = self.load_candidates()
        
        combined_sim, ml_sim, chip_sim, news_sim = self.calculate_combined_similarity(df)
        
        df['ml_similarity'] = ml_sim
        df['chip_similarity'] = chip_sim
        df['news_similarity'] = news_sim
        df['combined_similarity'] = combined_sim
        
        df_filtered = df[df['combined_similarity'] >= threshold].copy()
        df_filtered = df_filtered.sort_values('combined_similarity', ascending=False)
        
        logging.info(f"筛选完成: 阈值={threshold}, 候选数={len(df_filtered)}")
        
        return df_filtered
    
    def filter_with_multiple_thresholds(self, thresholds=[0.5, 0.4, 0.3]):
        """使用多个阈值筛选"""
        results = {}
        
        for threshold in thresholds:
            df_filtered = self.filter_candidates(threshold)
            
            output_file = self.output_dir / f'candidates_{int(threshold*100)}pct.csv'
            df_filtered.to_csv(output_file, index=False)
            
            results[f'{int(threshold*100)}%'] = {
                'threshold': threshold,
                'count': len(df_filtered),
                'file': str(output_file)
            }
            
            logging.info(f"阈值{threshold}: {len(df_filtered)}只候选股票")
        
        summary_file = self.output_dir / 'filtering_summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("\n✅ 相似度筛选完成:")
        for key, value in results.items():
            print(f"  {key} 阈值: {value['count']}只股票")
        
        return results

if __name__ == '__main__':
    filter = SimilarityFilter()
    results = filter.filter_with_multiple_thresholds([0.5, 0.4, 0.3])
