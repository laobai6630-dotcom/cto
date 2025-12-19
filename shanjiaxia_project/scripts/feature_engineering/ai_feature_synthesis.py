#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI特征合成模块 - 合成10个AI特征
权重: 最高优先级（1.5倍）
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/ai_feature_synthesis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AIFeatureSynthesizer:
    """AI特征合成器 - 合成10个高级特征"""
    
    def __init__(self):
        self.feature_dir = Path('data/features')
        self.feature_dir.mkdir(parents=True, exist_ok=True)
    
    def synthesize_capital_flow_score(self, df_raw):
        """合成资金流向评分"""
        score = (
            df_raw['volume_mean'] * 0.3 +
            df_raw['volume_change_mean'] * 0.4 +
            df_raw['volume_price_corr'] * 0.3
        )
        return score
    
    def synthesize_technical_pattern_score(self, df_raw):
        """合成技术形态评分"""
        score = (
            df_raw['macd_hist'] * 0.3 +
            df_raw['rsi_12'] / 100 * 0.3 +
            df_raw['kdj_j'] / 100 * 0.4
        )
        return score
    
    def synthesize_market_sentiment_score(self, df_raw):
        """合成市场情绪评分"""
        score = (
            df_raw['positive_days'] / 20 * 0.5 +
            df_raw['cumulative_return'] * 0.5
        )
        return score
    
    # ... 其他7个AI特征合成方法
    
    def synthesize_all_ai_features(self, df_raw):
        """合成所有10个AI特征"""
        df_ai = pd.DataFrame()
        
        df_ai['stock_code'] = df_raw['stock_code']
        df_ai['date'] = df_raw['date']
        
        # 10个AI合成特征
        df_ai['ai_capital_flow'] = self.synthesize_capital_flow_score(df_raw)
        df_ai['ai_technical_pattern'] = self.synthesize_technical_pattern_score(df_raw)
        df_ai['ai_market_sentiment'] = self.synthesize_market_sentiment_score(df_raw)
        # ... 其他7个特征
        
        # 标准化到[0, 1]范围
        for col in df_ai.columns[2:]:
            df_ai[col] = (df_ai[col] - df_ai[col].min()) / (df_ai[col].max() - df_ai[col].min() + 1e-10)
        
        # 保存
        output_file = self.feature_dir / 'ai_synthetic_features_10.csv'
        df_ai.to_csv(output_file, index=False)
        
        logging.info(f"AI特征合成完成: {len(df_ai)}条记录")
        return df_ai

if __name__ == '__main__':
    synthesizer = AIFeatureSynthesizer()
