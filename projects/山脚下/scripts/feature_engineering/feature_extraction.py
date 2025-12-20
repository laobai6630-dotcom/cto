#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
特征提取模块 - 提取134个原始特征
时间窗口: 从拉升日前一天向前推进20个交易日
"""

import pandas as pd
import numpy as np
import talib
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/feature_extraction.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FeatureExtractor:
    """特征提取器 - 提取134个原始特征"""
    
    def __init__(self, time_window=20):
        self.time_window = time_window  # 20个交易日
        self.data_dir = Path('data/processed')
        self.output_dir = Path('data/features')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_data(self, stock_code, end_date):
        """加载股票数据（20个交易日）"""
        # TODO: 从processed数据和backup中加载20个交易日的数据
        pass
    
    def extract_price_features(self, df):
        """提取价格特征（约30个）"""
        features = {}
        
        # 基础价格统计
        features['price_mean'] = df['close'].mean()
        features['price_std'] = df['close'].std()
        features['price_max'] = df['close'].max()
        features['price_min'] = df['close'].min()
        features['price_range'] = features['price_max'] - features['price_min']
        
        # 涨跌幅统计
        df['pct_change'] = df['close'].pct_change()
        features['return_mean'] = df['pct_change'].mean()
        features['return_std'] = df['pct_change'].std()
        features['return_max'] = df['pct_change'].max()
        features['return_min'] = df['pct_change'].min()
        features['positive_days'] = (df['pct_change'] > 0).sum()
        features['negative_days'] = (df['pct_change'] < 0).sum()
        
        # 更多价格特征...
        features['cumulative_return'] = (df['close'].iloc[-1] / df['close'].iloc[0]) - 1
        
        return features
    
    def extract_volume_features(self, df):
        """提取成交量特征（约25个）"""
        features = {}
        
        features['volume_mean'] = df['volume'].mean()
        features['volume_std'] = df['volume'].std()
        features['volume_max'] = df['volume'].max()
        features['volume_min'] = df['volume'].min()
        
        df['volume_change'] = df['volume'].pct_change()
        features['volume_change_mean'] = df['volume_change'].mean()
        features['volume_price_corr'] = df['volume'].corr(df['close'])
        
        return features
    
    def extract_technical_indicators(self, df):
        """提取技术指标特征（约50个）"""
        features = {}
        
        close = df['close'].values
        high = df['high'].values
        low = df['low'].values
        volume = df['volume'].values
        
        try:
            # 移动平均线
            features['ma5'] = talib.MA(close, timeperiod=5)[-1]
            features['ma10'] = talib.MA(close, timeperiod=10)[-1]
            features['ma20'] = talib.MA(close, timeperiod=20)[-1]
            
            # MACD
            macd, signal, hist = talib.MACD(close)
            features['macd'] = macd[-1] if len(macd) > 0 else 0
            features['macd_signal'] = signal[-1] if len(signal) > 0 else 0
            features['macd_hist'] = hist[-1] if len(hist) > 0 else 0
            
            # RSI
            features['rsi_6'] = talib.RSI(close, timeperiod=6)[-1]
            features['rsi_12'] = talib.RSI(close, timeperiod=12)[-1]
            
            # KDJ
            k, d = talib.STOCH(high, low, close)
            features['kdj_k'] = k[-1] if len(k) > 0 else 0
            features['kdj_d'] = d[-1] if len(d) > 0 else 0
            features['kdj_j'] = 3 * features['kdj_k'] - 2 * features['kdj_d']
            
            # 更多技术指标...
            
        except Exception as e:
            logging.error(f"技术指标计算失败: {str(e)}")
            for key in features:
                if pd.isna(features[key]):
                    features[key] = 0
        
        return features
    
    def extract_all_features(self, stock_code, end_date):
        """提取所有134个原始特征"""
        try:
            df = self.load_data(stock_code, end_date)
            
            features = {'stock_code': stock_code, 'date': end_date}
            
            features.update(self.extract_price_features(df))
            features.update(self.extract_volume_features(df))
            features.update(self.extract_technical_indicators(df))
            
            logging.info(f"特征提取完成: {stock_code}, 共{len(features)}个特征")
            return features
        
        except Exception as e:
            logging.error(f"特征提取失败 {stock_code}: {str(e)}")
            return None

if __name__ == '__main__':
    extractor = FeatureExtractor(time_window=20)
    # extractor.extract_all_features('000001', datetime.now())
