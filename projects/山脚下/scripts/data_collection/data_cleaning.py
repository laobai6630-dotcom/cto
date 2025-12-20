#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据清洗模块 - 负责数据验证、异常值处理、字段标准化
数据保留期: 180个交易日
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from datetime import datetime, timedelta

logging.basicConfig(
    filename='logs/data_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataCleaner:
    """数据清洗器"""
    
    def __init__(self, data_retention_days=180):
        self.data_retention_days = data_retention_days  # 180交易日
        self.raw_data_dir = Path('data/raw')
        self.processed_data_dir = Path('data/processed')
        self.backup_dir = Path('data/backup')
        
        for directory in [self.raw_data_dir, self.processed_data_dir, self.backup_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def validate_data(self, df, required_columns):
        """验证数据完整性"""
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"缺少必需的列: {missing_cols}")
        
        missing_count = df.isnull().sum()
        if missing_count.any():
            logging.warning(f"发现缺失值:\n{missing_count[missing_count > 0]}")
        
        return True
    
    def handle_missing_values(self, df):
        """处理缺失值"""
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].ffill()
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
        return df
    
    def remove_outliers(self, df, columns, n_std=3):
        """移除异常值"""
        for col in columns:
            if col in df.columns and df[col].dtype in [np.float64, np.int64]:
                mean = df[col].mean()
                std = df[col].std()
                df = df[abs(df[col] - mean) <= n_std * std]
        return df
    
    def standardize_fields(self, df):
        """字段标准化"""
        if 'stock_code' in df.columns:
            df['stock_code'] = df['stock_code'].astype(str).str.zfill(6)
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        price_columns = ['open', 'high', 'low', 'close', 'adj_close']
        for col in price_columns:
            if col in df.columns:
                df[col] = df[col].round(2)
        
        return df
    
    def clean_daily_data(self, input_file='daily_data.csv'):
        """清洗日线数据"""
        try:
            df = pd.read_csv(self.raw_data_dir / input_file)
            
            required_columns = ['stock_code', 'date', 'open', 'high', 'low', 'close', 'volume']
            self.validate_data(df, required_columns)
            
            df = self.handle_missing_values(df)
            df = self.remove_outliers(df, ['open', 'high', 'low', 'close', 'volume'])
            df = self.standardize_fields(df)
            
            output_file = self.processed_data_dir / f"daily_data_cleaned_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(output_file, index=False)
            
            logging.info(f"日线数据清洗完成: {output_file}")
            return df
        
        except Exception as e:
            logging.error(f"日线数据清洗失败: {str(e)}")
            raise
    
    def backup_historical_data(self):
        """备份历史数据（保留180个交易日）"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            for data_file in self.processed_data_dir.glob('daily_data_cleaned_*.csv'):
                backup_file = self.backup_dir / f"daily_data_backup_{today}.csv"
                df = pd.read_csv(data_file)
                df.to_csv(backup_file, index=False)
                logging.info(f"创建备份: {backup_file}")
            
            cutoff_date = datetime.now() - timedelta(days=self.data_retention_days)
            for backup_file in self.backup_dir.glob('daily_data_backup_*.csv'):
                file_date_str = backup_file.stem.split('_')[-1]
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
                if file_date < cutoff_date:
                    backup_file.unlink()
                    logging.info(f"删除过期备份: {backup_file}")
        
        except Exception as e:
            logging.error(f"备份失败: {str(e)}")

if __name__ == '__main__':
    cleaner = DataCleaner(data_retention_days=180)
    cleaner.clean_daily_data()
    cleaner.backup_historical_data()
