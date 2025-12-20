#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
识别对照组 - 筛选30个交易日跌幅前20名的股票
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import logging

logging.basicConfig(
    filename='logs/contrast_group.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ContrastGroupIdentifier:
    """对照组识别器 - 识别跌幅前20名"""
    
    def __init__(self, period_days=30, top_n=20):
        self.period_days = period_days  # 30个交易日
        self.top_n = top_n  # 前20名
        self.data_dir = Path('data/processed')
        self.output_dir = Path('data/contrast_group')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_market_data(self):
        """加载市场数据"""
        df = pd.read_csv(self.data_dir / 'daily_data_cleaned.csv')
        return df
    
    def calculate_30d_return(self, df):
        """计算30个交易日涨跌幅"""
        df = df.sort_values(['stock_code', 'date'])
        
        results = []
        for stock_code, group in df.groupby('stock_code'):
            if len(group) >= self.period_days:
                start_price = group.iloc[0]['close']
                end_price = group.iloc[-1]['close']
                return_30d = (end_price - start_price) / start_price
                
                results.append({
                    'stock_code': stock_code,
                    'start_date': group.iloc[0]['date'],
                    'end_date': group.iloc[-1]['date'],
                    'start_price': start_price,
                    'end_price': end_price,
                    'return_30d': return_30d
                })
        
        return pd.DataFrame(results)
    
    def identify_worst_performers(self, df_returns):
        """识别跌幅前20名"""
        df_sorted = df_returns.sort_values('return_30d')
        contrast_group = df_sorted.head(self.top_n)
        
        logging.info(f"识别对照组完成: {len(contrast_group)}只股票")
        return contrast_group
    
    def save_contrast_group(self, contrast_group):
        """保存对照组"""
        output_file = self.output_dir / f'contrast_group_30d_drop_top20_{datetime.now().strftime("%Y%m%d")}.csv'
        contrast_group.to_csv(output_file, index=False)
        logging.info(f"对照组已保存: {output_file}")
        return output_file
    
    def run(self):
        """执行识别流程"""
        df = self.load_market_data()
        df_returns = self.calculate_30d_return(df)
        contrast_group = self.identify_worst_performers(df_returns)
        output_file = self.save_contrast_group(contrast_group)
        
        print(f"✅ 对照组识别完成: {len(contrast_group)}只股票")
        return contrast_group

if __name__ == '__main__':
    identifier = ContrastGroupIdentifier(period_days=30, top_n=20)
    contrast_group = identifier.run()
