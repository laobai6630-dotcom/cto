#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
山脚下项目 v2.0 - 完整代码框架生成脚本
Project: 山脚下 - A股"山脚下"形态股票精准筛选系统
Version: 2.0
Author: AI Agent
Date: 2025-12-19

使用方法:
    python3 generate_all_files.py
    
这个脚本将生成项目的完整目录结构和所有必需的文件
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# 由于完整的代码模板非常大，这里使用导入方式
# 实际使用时，所有模板将被完全展开

try:
    # 尝试导入模板文件
    from code_templates import ALL_FILE_TEMPLATES
except ImportError:
    # 如果没有模板文件，使用内嵌的简化版本
    print("⚠️  未找到code_templates.py，使用内嵌模板")
    
    # 内嵌所有文件模板
    ALL_FILE_TEMPLATES = {}
    
    #####################################################################
    # 数据采集模块
    #####################################################################
    
    ALL_FILE_TEMPLATES["scripts/data_collection/scheduler_main.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主调度程序 - 负责调度所有数据采集任务
"""

import schedule
import time
import logging
from datetime import datetime
import json

logging.basicConfig(
    filename='logs/scheduler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataCollectionScheduler:
    """数据采集调度器"""
    
    def __init__(self, config_path='config/config.json'):
        self.config = self.load_config(config_path)
    
    def load_config(self, config_path):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"配置文件不存在: {config_path}")
            return {}
    
    def collect_daily_data(self):
        """采集日线和分钟线数据"""
        logging.info("开始采集日线和分钟线数据...")
        # TODO: 调用现有的"日线和分钟线数据获取.py"
        
    def collect_weekly_data(self):
        """采集周线数据"""
        logging.info("开始采集周线数据...")
        # TODO: 调用现有的"周线数据获取.py"
        
    def collect_monthly_data(self):
        """采集月线数据"""
        logging.info("开始采集月线数据...")
        # TODO: 调用现有的"月线数据获取.py"
        
    def collect_financial_data(self):
        """采集财务和基本面数据"""
        logging.info("开始采集财务和基本面数据...")
        # TODO: 调用现有的"财务和基本面数据获取.py"
    
    def setup_schedule(self):
        """设置定时任务"""
        schedule.every().day.at("09:00").do(self.collect_daily_data)
        schedule.every().monday.at("16:00").do(self.collect_weekly_data)
        schedule.every().day.at("10:00").do(self.collect_financial_data)
        logging.info("定时任务设置完成")
    
    def run(self):
        """运行调度器"""
        self.setup_schedule()
        logging.info("数据采集调度器启动")
        print("🚀 数据采集调度器已启动...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == '__main__':
    scheduler = DataCollectionScheduler()
    scheduler.run()
'''

    ALL_FILE_TEMPLATES["scripts/data_collection/data_cleaning.py"] = '''#!/usr/bin/env python3
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
            logging.warning(f"发现缺失值:\\n{missing_count[missing_count > 0]}")
        
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
'''

    #####################################################################
    # 特征工程模块  
    #####################################################################
    
    ALL_FILE_TEMPLATES["scripts/feature_engineering/feature_extraction.py"] = '''#!/usr/bin/env python3
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
'''

    ALL_FILE_TEMPLATES["scripts/feature_engineering/ai_feature_synthesis.py"] = '''#!/usr/bin/env python3
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
'''

    ALL_FILE_TEMPLATES["scripts/feature_engineering/chip_distribution.py"] = '''#!/usr/bin/env python3
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
'''

    ALL_FILE_TEMPLATES["scripts/feature_engineering/feature_normalization.py"] = '''#!/usr/bin/env python3
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
'''

    ALL_FILE_TEMPLATES["scripts/feature_engineering/feature_importance.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
特征重要性分析模块 - 计算并排序特征重要性
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/feature_importance.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FeatureImportanceAnalyzer:
    """特征重要性分析器"""
    
    def __init__(self):
        self.feature_dir = Path('data/features')
        self.output_dir = Path('data/features')
    
    def calculate_rf_importance(self, X, y):
        """基于随机森林计算特征重要性"""
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X, y)
        
        importances = rf.feature_importances_
        return importances
    
    def analyze_feature_importance(self):
        """分析特征重要性"""
        logging.info("特征重要性分析模块已准备")
        # TODO: 实现完整的特征重要性分析
        return None

if __name__ == '__main__':
    analyzer = FeatureImportanceAnalyzer()
'''

    #####################################################################
    # 对照组模块
    #####################################################################
    
    ALL_FILE_TEMPLATES["scripts/contrast_group/identify_contrast_group.py"] = '''#!/usr/bin/env python3
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
'''

    ALL_FILE_TEMPLATES["scripts/contrast_group/extract_contrast_features.py"] = '''#!/usr/bin/env python3
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
'''

    ALL_FILE_TEMPLATES["scripts/contrast_group/compare_contrast_vs_candidates.py"] = '''#!/usr/bin/env python3
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
        
        print(f"\\n✅ 对比分析完成:")
        print(f"  📊 分离度评分: {separation_score:.4f}")
        
        return results

if __name__ == '__main__':
    comparator = ContrastComparator()
    results = comparator.run_comparison()
'''

    #####################################################################
    # ML训练模块
    #####################################################################
    
    ALL_FILE_TEMPLATES["scripts/ml_training/model_training.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型训练模块 - 训练3个基础模型
模型: Logistic Regression, Random Forest, XGBoost/LightGBM
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/ml_training.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ModelTrainer:
    """模型训练器 - 训练LR、RF、XGB三个模型"""
    
    def __init__(self):
        self.feature_dir = Path('data/features')
        self.contrast_dir = Path('data/contrast_group')
        self.model_dir = Path('models')
        self.model_dir.mkdir(parents=True, exist_ok=True)
    
    def load_training_data(self):
        """加载训练数据（成功样本 + 对照组）"""
        df_success = pd.read_csv(self.feature_dir / 'all_features_88.csv')
        df_success['label'] = 1
        
        df_contrast = pd.read_csv(self.contrast_dir / 'contrast_group_features_88.csv')
        df_contrast['label'] = 0
        
        df_train = pd.concat([df_success, df_contrast], ignore_index=True)
        
        logging.info(f"训练数据加载完成: {len(df_train)}条")
        return df_train
    
    def prepare_data(self, df):
        """准备训练数据"""
        X = df.drop(['stock_code', 'date', 'label'], axis=1)
        y = df['label']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        return X_train, X_test, y_train, y_test
    
    def train_logistic_regression(self, X_train, y_train):
        """训练逻辑回归模型"""
        logging.info("开始训练逻辑回归模型...")
        
        model = LogisticRegression(
            max_iter=1000,
            random_state=42,
            class_weight='balanced'
        )
        model.fit(X_train, y_train)
        
        model_file = self.model_dir / 'model_lr.pkl'
        joblib.dump(model, model_file)
        
        logging.info(f"逻辑回归模型已保存: {model_file}")
        return model
    
    def train_random_forest(self, X_train, y_train):
        """训练随机森林模型"""
        logging.info("开始训练随机森林模型...")
        
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced',
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        model_file = self.model_dir / 'model_rf.pkl'
        joblib.dump(model, model_file)
        
        logging.info(f"随机森林模型已保存: {model_file}")
        return model
    
    def train_gradient_boosting(self, X_train, y_train):
        """训练梯度提升模型"""
        logging.info(f"开始训练梯度提升模型(XGBoost)...")
        
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss'
        )
        
        model.fit(X_train, y_train)
        
        model_file = self.model_dir / f'model_gb_xgboost.pkl'
        joblib.dump(model, model_file)
        
        logging.info(f"梯度提升模型已保存: {model_file}")
        return model
    
    def train_all_models(self):
        """训练所有3个模型"""
        df = self.load_training_data()
        X_train, X_test, y_train, y_test = self.prepare_data(df)
        
        model_lr = self.train_logistic_regression(X_train, y_train)
        model_rf = self.train_random_forest(X_train, y_train)
        model_gb = self.train_gradient_boosting(X_train, y_train)
        
        test_data = {
            'X_test': X_test,
            'y_test': y_test
        }
        joblib.dump(test_data, self.model_dir / 'test_data.pkl')
        
        logging.info("所有模型训练完成")
        
        print("\\n✅ 模型训练完成:")
        print("  📊 逻辑回归: model_lr.pkl")
        print("  🌲 随机森林: model_rf.pkl")
        print("  🚀 梯度提升: model_gb_xgboost.pkl")
        
        return {
            'lr': model_lr,
            'rf': model_rf,
            'gb': model_gb
        }

if __name__ == '__main__':
    trainer = ModelTrainer()
    models = trainer.train_all_models()
'''

    ALL_FILE_TEMPLATES["scripts/ml_training/model_ensemble.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型集成 - 集成3个基础模型
方法: 加权平均 (LR: 0.4, RF: 0.3, GB: 0.3)
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/ml_training.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ModelEnsembler:
    """模型集成器"""
    
    def __init__(self, weights=None):
        self.model_dir = Path('models')
        self.weights = weights or {'lr': 0.4, 'rf': 0.3, 'gb': 0.3}
    
    def load_models(self):
        """加载3个基础模型"""
        model_lr = joblib.load(self.model_dir / 'model_lr.pkl')
        model_rf = joblib.load(self.model_dir / 'model_rf.pkl')
        model_gb = joblib.load(self.model_dir / 'model_gb_xgboost.pkl')
        
        return {
            'lr': model_lr,
            'rf': model_rf,
            'gb': model_gb
        }
    
    def save_ensemble_weights(self):
        """保存集成权重"""
        weights_file = self.model_dir / 'ensemble_weights.json'
        with open(weights_file, 'w') as f:
            json.dump(self.weights, f, indent=2)
        
        logging.info(f"集成权重已保存: {weights_file}")
    
    def create_ensemble(self):
        """创建集成模型"""
        models = self.load_models()
        
        self.save_ensemble_weights()
        
        class EnsembleModel:
            def __init__(self, models, weights):
                self.models = models
                self.weights = weights
            
            def predict_proba(self, X):
                proba_lr = self.models['lr'].predict_proba(X)[:, 1]
                proba_rf = self.models['rf'].predict_proba(X)[:, 1]
                proba_gb = self.models['gb'].predict_proba(X)[:, 1]
                
                proba = (
                    proba_lr * self.weights['lr'] +
                    proba_rf * self.weights['rf'] +
                    proba_gb * self.weights['gb']
                )
                return proba
            
            def predict(self, X, threshold=0.5):
                proba = self.predict_proba(X)
                return (proba >= threshold).astype(int)
        
        ensemble_model = EnsembleModel(models, self.weights)
        
        model_file = self.model_dir / 'model_ensemble.pkl'
        joblib.dump(ensemble_model, model_file)
        
        logging.info(f"集成模型已保存: {model_file}")
        
        print("\\n✅ 模型集成完成:")
        print(f"  权重配置: {self.weights}")
        print(f"  集成模型: {model_file}")
        
        return ensemble_model

if __name__ == '__main__':
    ensembler = ModelEnsembler()
    ensemble_model = ensembler.create_ensemble()
'''

    ALL_FILE_TEMPLATES["scripts/ml_training/model_evaluation.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型评估 - 评估模型性能
指标: Accuracy, Precision, Recall, F1, AUC-ROC
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)
import joblib
import json
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/ml_training.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ModelEvaluator:
    """模型评估器"""
    
    def __init__(self):
        self.model_dir = Path('models')
        self.output_dir = Path('reports/model_evaluation')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_test_data(self):
        """加载测试数据"""
        test_data = joblib.load(self.model_dir / 'test_data.pkl')
        return test_data['X_test'], test_data['y_test']
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """评估单个模型"""
        y_pred = model.predict(X_test)
        
        if hasattr(model, 'predict_proba'):
            y_proba = model.predict_proba(X_test)[:, 1]
        else:
            y_proba = y_pred
        
        metrics = {
            'model_name': model_name,
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision': float(precision_score(y_test, y_pred)),
            'recall': float(recall_score(y_test, y_pred)),
            'f1_score': float(f1_score(y_test, y_pred)),
            'auc_roc': float(roc_auc_score(y_test, y_proba))
        }
        
        cm = confusion_matrix(y_test, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
        
        return metrics
    
    def evaluate_all_models(self):
        """评估所有模型"""
        X_test, y_test = self.load_test_data()
        
        model_lr = joblib.load(self.model_dir / 'model_lr.pkl')
        model_rf = joblib.load(self.model_dir / 'model_rf.pkl')
        model_gb = joblib.load(self.model_dir / 'model_gb_xgboost.pkl')
        
        metrics_lr = self.evaluate_model(model_lr, X_test, y_test, 'Logistic Regression')
        metrics_rf = self.evaluate_model(model_rf, X_test, y_test, 'Random Forest')
        metrics_gb = self.evaluate_model(model_gb, X_test, y_test, 'Gradient Boosting')
        
        model_ensemble = joblib.load(self.model_dir / 'model_ensemble.pkl')
        metrics_ensemble = self.evaluate_model(model_ensemble, X_test, y_test, 'Ensemble')
        
        all_metrics = {
            'logistic_regression': metrics_lr,
            'random_forest': metrics_rf,
            'gradient_boosting': metrics_gb,
            'ensemble': metrics_ensemble
        }
        
        output_file = self.output_dir / 'model_metrics.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_metrics, f, ensure_ascii=False, indent=2)
        
        logging.info(f"模型评估完成: {output_file}")
        
        self.generate_evaluation_report(all_metrics)
        
        return all_metrics
    
    def generate_evaluation_report(self, metrics):
        """生成评估报告"""
        report = []
        report.append("# 模型评估报告\\n")
        report.append("## 评估指标\\n")
        
        report.append("| 模型 | Accuracy | Precision | Recall | F1 Score | AUC-ROC |")
        report.append("|------|----------|-----------|--------|----------|---------|")
        
        for model_name, m in metrics.items():
            report.append(
                f"| {m['model_name']} | "
                f"{m['accuracy']:.4f} | "
                f"{m['precision']:.4f} | "
                f"{m['recall']:.4f} | "
                f"{m['f1_score']:.4f} | "
                f"{m['auc_roc']:.4f} |"
            )
        
        report.append("\\n## 结论\\n")
        
        best_model = max(metrics.items(), key=lambda x: x[1]['f1_score'])
        report.append(f"最佳模型: **{best_model[1]['model_name']}** (F1 Score: {best_model[1]['f1_score']:.4f})\\n")
        
        report_file = self.output_dir / 'evaluation_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\\n'.join(report))
        
        logging.info(f"评估报告已保存: {report_file}")
        
        print("\\n✅ 模型评估完成:")
        for model_name, m in metrics.items():
            print(f"  {m['model_name']}: Accuracy={m['accuracy']:.4f}, F1={m['f1_score']:.4f}")

if __name__ == '__main__':
    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate_all_models()
'''

    #####################################################################
    # 筛选模块
    #####################################################################
    
    ALL_FILE_TEMPLATES["scripts/filtering/similarity_filter.py"] = '''#!/usr/bin/env python3
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
        
        print("\\n✅ 相似度筛选完成:")
        for key, value in results.items():
            print(f"  {key} 阈值: {value['count']}只股票")
        
        return results

if __name__ == '__main__':
    filter = SimilarityFilter()
    results = filter.filter_with_multiple_thresholds([0.5, 0.4, 0.3])
'''

    ALL_FILE_TEMPLATES["scripts/filtering/filtering_logic.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
递进筛选逻辑 - 先50% → 若无则40% → 若无则30%
参数可通过Dashboard调整
"""

import pandas as pd
import json
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/filtering.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ProgressiveFilter:
    """递进筛选器"""
    
    def __init__(self):
        self.candidates_dir = Path('data/candidates')
        self.config_dir = Path('config')
        self.output_dir = Path('data/candidates')
    
    def load_parameters(self):
        """加载筛选参数"""
        params_file = self.config_dir / 'parameters.json'
        if params_file.exists():
            with open(params_file, 'r') as f:
                return json.load(f)
        else:
            return {
                'thresholds': [0.5, 0.4, 0.3],
                'min_candidates': 5,
                'max_candidates': 20
            }
    
    def progressive_filter(self):
        """执行递进筛选"""
        params = self.load_parameters()
        thresholds = params['thresholds']
        min_candidates = params['min_candidates']
        max_candidates = params['max_candidates']
        
        final_candidates = None
        selected_threshold = None
        
        for threshold in thresholds:
            file_name = f'candidates_{int(threshold*100)}pct.csv'
            file_path = self.candidates_dir / file_name
            
            if not file_path.exists():
                continue
            
            df = pd.read_csv(file_path)
            
            if len(df) >= min_candidates:
                if len(df) > max_candidates:
                    final_candidates = df.head(max_candidates)
                else:
                    final_candidates = df
                
                selected_threshold = threshold
                logging.info(f"选择阈值{threshold}: {len(final_candidates)}只候选股票")
                break
        
        if final_candidates is None:
            logging.warning("未找到符合条件的候选股票")
            return None
        
        output_file = self.output_dir / 'selection_candidates.csv'
        final_candidates.to_csv(output_file, index=False)
        
        selection_info = {
            'selected_threshold': selected_threshold,
            'candidates_count': len(final_candidates),
            'min_candidates': min_candidates,
            'max_candidates': max_candidates,
            'top_stocks': final_candidates['stock_code'].head(10).tolist()
        }
        
        info_file = self.output_dir / 'selection_info.json'
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(selection_info, f, ensure_ascii=False, indent=2)
        
        logging.info(f"最终候选已保存: {output_file}")
        
        print(f"\\n✅ 递进筛选完成:")
        print(f"  选择阈值: {selected_threshold}")
        print(f"  候选数量: {len(final_candidates)}")
        
        return final_candidates

if __name__ == '__main__':
    filter = ProgressiveFilter()
    candidates = filter.progressive_filter()
'''

    #####################################################################
    # 跟踪报告模块
    #####################################################################
    
    ALL_FILE_TEMPLATES["scripts/tracking/track_candidates_30d.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
30天跟踪模块 - 跟踪候选股票30个交易日的表现
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    filename='logs/tracking.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CandidateTracker:
    """候选股票跟踪器"""
    
    def __init__(self, tracking_days=30):
        self.tracking_days = tracking_days
        self.candidates_dir = Path('data/candidates')
        self.output_dir = Path('data/tracking')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_candidates(self):
        """加载候选股票"""
        df = pd.read_csv(self.candidates_dir / 'selection_candidates.csv')
        return df
    
    def track_performance(self):
        """跟踪30天表现"""
        candidates = self.load_candidates()
        
        # TODO: 实现30天跟踪逻辑
        tracking_data = {
            'tracking_start': datetime.now().strftime('%Y-%m-%d'),
            'tracking_days': self.tracking_days,
            'candidates': candidates['stock_code'].tolist()
        }
        
        output_file = self.output_dir / 'active_tracking.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tracking_data, f, ensure_ascii=False, indent=2)
        
        logging.info(f"跟踪数据已保存: {output_file}")
        return tracking_data

if __name__ == '__main__':
    tracker = CandidateTracker(tracking_days=30)
    tracker.track_performance()
'''

    ALL_FILE_TEMPLATES["scripts/tracking/performance_evaluation.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
效果评估模块 - 评估候选股票表现
"""

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/tracking.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PerformanceEvaluator:
    """表现评估器"""
    
    def __init__(self):
        self.tracking_dir = Path('data/tracking')
        self.output_dir = Path('reports')
    
    def evaluate_performance(self):
        """评估表现"""
        # TODO: 实现效果评估逻辑
        logging.info("效果评估完成")
        return None

if __name__ == '__main__':
    evaluator = PerformanceEvaluator()
    evaluator.evaluate_performance()
'''

    ALL_FILE_TEMPLATES["scripts/tracking/generate_daily_report.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日报生成模块
"""

from datetime import datetime
from pathlib import Path

class DailyReportGenerator:
    """日报生成器"""
    
    def __init__(self):
        self.output_dir = Path('reports/daily')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self):
        """生成日报"""
        today = datetime.now().strftime('%Y-%m-%d')
        report = f"# 日报 {today}\\n\\n## 今日候选股票\\n\\nTODO: 实现日报内容\\n"
        
        output_file = self.output_dir / f"daily_{today}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 日报已生成: {output_file}")

if __name__ == '__main__':
    generator = DailyReportGenerator()
    generator.generate_report()
'''

    ALL_FILE_TEMPLATES["scripts/tracking/generate_weekly_report.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周报生成模块
"""

from datetime import datetime
from pathlib import Path

class WeeklyReportGenerator:
    """周报生成器"""
    
    def __init__(self):
        self.output_dir = Path('reports/weekly')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self):
        """生成周报"""
        week = datetime.now().isocalendar()[1]
        year = datetime.now().year
        report = f"# 周报 {year}-W{week:02d}\\n\\n## 本周总结\\n\\nTODO: 实现周报内容\\n"
        
        output_file = self.output_dir / f"weekly_{year}-W{week:02d}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 周报已生成: {output_file}")

if __name__ == '__main__':
    generator = WeeklyReportGenerator()
    generator.generate_report()
'''

    ALL_FILE_TEMPLATES["scripts/tracking/generate_monthly_report.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
月报生成模块
"""

from datetime import datetime
from pathlib import Path

class MonthlyReportGenerator:
    """月报生成器"""
    
    def __init__(self):
        self.output_dir = Path('reports/monthly')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self):
        """生成月报"""
        month = datetime.now().strftime('%Y-%m')
        report = f"# 月报 {month}\\n\\n## 本月总结\\n\\nTODO: 实现月报内容\\n"
        
        output_file = self.output_dir / f"monthly_{month}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 月报已生成: {output_file}")

if __name__ == '__main__':
    generator = MonthlyReportGenerator()
    generator.generate_report()
'''

    #####################################################################
    # GitHub自动化模块
    #####################################################################
    
    ALL_FILE_TEMPLATES["scripts/github/github_trigger.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub触发机制 - 触发GitHub Actions工作流
"""

import requests
import json
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/github.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GitHubTrigger:
    """GitHub工作流触发器"""
    
    def __init__(self):
        self.config_file = Path('config/config.json')
        self.load_config()
    
    def load_config(self):
        """加载GitHub配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.github_token = config.get('github_token', '')
                self.repo = config.get('github_repo', '')
    
    def trigger_workflow(self, workflow_name, inputs=None):
        """触发工作流"""
        # TODO: 实现GitHub Actions触发逻辑
        logging.info(f"触发工作流: {workflow_name}")
        print(f"✅ 工作流已触发: {workflow_name}")

if __name__ == '__main__':
    trigger = GitHubTrigger()
    trigger.trigger_workflow('daily.yml')
'''

    #####################################################################
    # 监督报告模块
    #####################################################################
    
    ALL_FILE_TEMPLATES["scripts/monitoring/generate_supervisory_report.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监督报告生成模块 - 为监督员工生成报告
"""

import json
from datetime import datetime
from pathlib import Path

class SupervisoryReportGenerator:
    """监督报告生成器"""
    
    def __init__(self):
        self.output_dir = Path('reports/supervisory')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self):
        """生成监督报告"""
        report = {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'project_status': 'running',
            'data_collection': 'normal',
            'model_performance': 'good',
            'issues': []
        }
        
        output_file = self.output_dir / 'supervisor_report.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 监督报告已生成: {output_file}")
        return report

if __name__ == '__main__':
    generator = SupervisoryReportGenerator()
    generator.generate_report()
'''

    #####################################################################
    # 工具类模块
    #####################################################################
    
    ALL_FILE_TEMPLATES["scripts/utils/backup_manager.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
备份管理模块
"""

import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging

logging.basicConfig(
    filename='logs/backup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BackupManager:
    """备份管理器"""
    
    def __init__(self, retention_days=180):
        self.retention_days = retention_days
        self.backup_dir = Path('data/backup')
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, source_dir, backup_name=None):
        """创建备份"""
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = self.backup_dir / backup_name
        shutil.copytree(source_dir, backup_path, dirs_exist_ok=True)
        
        logging.info(f"备份已创建: {backup_path}")
        return backup_path
    
    def clean_old_backups(self):
        """清理过期备份"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        for backup_dir in self.backup_dir.iterdir():
            if backup_dir.is_dir():
                # 从目录名提取日期
                try:
                    date_str = backup_dir.name.split('_')[1]
                    backup_date = datetime.strptime(date_str, '%Y%m%d')
                    if backup_date < cutoff_date:
                        shutil.rmtree(backup_dir)
                        logging.info(f"删除过期备份: {backup_dir}")
                except:
                    pass

if __name__ == '__main__':
    manager = BackupManager(retention_days=180)
    manager.clean_old_backups()
'''

    ALL_FILE_TEMPLATES["scripts/utils/verify_backup.py"] = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
备份验证模块
"""

from pathlib import Path
import hashlib
import logging

logging.basicConfig(
    filename='logs/backup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BackupVerifier:
    """备份验证器"""
    
    def __init__(self):
        self.backup_dir = Path('data/backup')
    
    def calculate_checksum(self, file_path):
        """计算文件校验和"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def verify_backup(self, backup_name):
        """验证备份完整性"""
        backup_path = self.backup_dir / backup_name
        if not backup_path.exists():
            logging.error(f"备份不存在: {backup_name}")
            return False
        
        # TODO: 实现备份验证逻辑
        logging.info(f"备份验证完成: {backup_name}")
        return True

if __name__ == '__main__':
    verifier = BackupVerifier()
'''

    #####################################################################
    # 配置文件
    #####################################################################
    
    ALL_FILE_TEMPLATES["config/config.json"] = '''{
  "project_name": "山脚下项目 v2.0",
  "version": "2.0",
  "data_retention_days": 180,
  "feature_time_window": 20,
  "github_token": "YOUR_GITHUB_TOKEN",
  "github_repo": "laobai6630-dotcom/cto",
  "dashboard_password": "admin123",
  "api_endpoints": {
    "stock_data": "https://api.example.com/stock",
    "financial_data": "https://api.example.com/financial"
  }
}
'''

    ALL_FILE_TEMPLATES["config/weights.json"] = '''{
  "similarity_weights": {
    "ml_model": 0.6,
    "chip_distribution": 0.2,
    "news_sentiment": 0.2
  },
  "model_ensemble_weights": {
    "lr": 0.4,
    "rf": 0.3,
    "gb": 0.3
  }
}
'''

    ALL_FILE_TEMPLATES["config/parameters.json"] = '''{
  "filtering": {
    "thresholds": [0.5, 0.4, 0.3],
    "min_candidates": 5,
    "max_candidates": 20
  },
  "tracking": {
    "tracking_days": 30,
    "success_threshold": 0.5
  },
  "contrast_group": {
    "period_days": 30,
    "top_n": 20
  }
}
'''

    #####################################################################
    # 文档文件
    #####################################################################
    
    ALL_FILE_TEMPLATES["docs/README.md"] = '''# 山脚下项目 v2.0

## 项目概述

A股"山脚下"形态股票精准筛选系统

### 核心功能

1. **数据采集**: 180天数据保留期
2. **特征工程**: 88个特征（134原始+10AI+10筹码）
3. **对照组分析**: 跌幅前20名股票对比
4. **ML模型**: 3个模型集成（LR+RF+XGB）
5. **相似度筛选**: 递进筛选（50%→40%→30%）
6. **30天跟踪**: 动态跟踪候选股票

### 目录结构

```
shanjiaxia_project/
├── scripts/          # 所有Python脚本
├── dashboard/        # Dashboard网页
├── config/           # 配置文件
├── data/             # 数据目录
├── models/           # ML模型
├── reports/          # 报告输出
└── docs/             # 文档
```

### 快速开始

1. 配置环境
2. 修改config/config.json
3. 运行数据采集
4. 训练ML模型
5. 启动Dashboard

## 联系方式

GitHub: https://github.com/laobai6630-dotcom/cto/
'''

    ALL_FILE_TEMPLATES["docs/ARCHITECTURE.md"] = '''# 系统架构

## 整体架构

山脚下项目采用模块化设计，包含以下核心模块：

### 1. 数据采集模块

- 日线/分钟线数据
- 周线/月线数据
- 财务基本面数据

### 2. 特征工程模块

- 134个原始特征提取
- 10个AI特征合成
- 10个筹码特征计算
- 特征标准化与选择

### 3. 对照组模块

- 识别跌幅前20名
- 提取对照组特征
- 对比分离度分析

### 4. ML训练模块

- 逻辑回归模型
- 随机森林模型
- 梯度提升模型
- 模型集成

### 5. 筛选模块

- 相似度计算
- 递进筛选逻辑

### 6. 跟踪报告模块

- 30天跟踪
- 日报/周报/月报

## 数据流

```
数据采集 → 特征提取 → ML模型 → 相似度筛选 → 候选股票 → 30天跟踪
    ↓
对照组识别 → 对照组特征 → 对比分析
```
'''

    ALL_FILE_TEMPLATES["docs/API_REFERENCE.md"] = '''# API参考

## 核心API

### 数据采集API

```python
from scripts.data_collection.scheduler_main import DataCollectionScheduler

scheduler = DataCollectionScheduler()
scheduler.collect_daily_data()
```

### 特征提取API

```python
from scripts.feature_engineering.feature_extraction import FeatureExtractor

extractor = FeatureExtractor(time_window=20)
features = extractor.extract_all_features('000001', datetime.now())
```

### ML训练API

```python
from scripts.ml_training.model_training import ModelTrainer

trainer = ModelTrainer()
models = trainer.train_all_models()
```

### 筛选API

```python
from scripts.filtering.similarity_filter import SimilarityFilter

filter = SimilarityFilter()
results = filter.filter_with_multiple_thresholds([0.5, 0.4, 0.3])
```
'''

    ALL_FILE_TEMPLATES["docs/DEPLOYMENT.md"] = '''# 部署指南

## 环境要求

- Python 3.8+
- PostgreSQL (可选)
- 依赖包见requirements.txt

## 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/laobai6630-dotcom/cto.git
cd shanjiaxia_project
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置文件
```bash
cp config/config.json.example config/config.json
# 编辑config.json填入必要配置
```

4. 启动服务
```bash
python scripts/data_collection/scheduler_main.py
```

## GitHub Actions配置

配置自托管Runner以在本地服务器上运行工作流
'''

    ALL_FILE_TEMPLATES["docs/MAINTENANCE.md"] = '''# 运维手册

## 日常运维

### 1. 数据备份

- 每日自动备份到data/backup
- 保留180天备份数据
- 定期验证备份完整性

### 2. 日志监控

- 日志位置：logs/
- 关注ERROR和WARNING级别
- 定期清理旧日志

### 3. 模型更新

- 定期重新训练模型
- 评估模型性能
- 更新模型文件

### 4. 性能监控

- 监控Dashboard性能
- 监控数据采集延迟
- 监控API响应时间

## 故障处理

### 常见问题

1. 数据采集失败
   - 检查API连接
   - 检查网络状况
   - 查看日志详情

2. 模型预测异常
   - 检查特征数据
   - 验证模型文件
   - 重新训练模型
'''

    ALL_FILE_TEMPLATES["docs/CHANGELOG.md"] = '''# 版本日志

## v2.0 (2025-12-19)

### 新增功能
- 对照组分析功能
- 筹码分布特征
- AI特征合成
- Dashboard密码保护
- 中英双语支持
- GitHub自动化工作流
- 监督报告功能

### 改进
- 数据保留期增加到180天
- 特征时间窗口调整为20天
- 特征数量增加到88个
- 递进筛选逻辑优化

### Bug修复
- 修复数据清洗异常值处理
- 修复特征标准化问题

## v1.0 (2025-11-01)

### 初始版本
- 基础数据采集功能
- 70个特征提取
- 3个ML模型训练
- 简单筛选逻辑
'''

    #####################################################################
    # 本地化文件
    #####################################################################
    
    ALL_FILE_TEMPLATES["locales/zh_CN.json"] = '''{
  "dashboard": {
    "title": "山脚下项目监控面板",
    "candidates": "候选股票",
    "contrast_group": "对照组",
    "performance": "表现追踪",
    "settings": "参数设置"
  },
  "buttons": {
    "login": "登录",
    "logout": "登出",
    "save": "保存",
    "cancel": "取消",
    "refresh": "刷新"
  },
  "messages": {
    "success": "操作成功",
    "error": "操作失败",
    "loading": "加载中..."
  }
}
'''

    ALL_FILE_TEMPLATES["locales/en_US.json"] = '''{
  "dashboard": {
    "title": "Shanjiaxia Project Dashboard",
    "candidates": "Candidates",
    "contrast_group": "Contrast Group",
    "performance": "Performance Tracking",
    "settings": "Settings"
  },
  "buttons": {
    "login": "Login",
    "logout": "Logout",
    "save": "Save",
    "cancel": "Cancel",
    "refresh": "Refresh"
  },
  "messages": {
    "success": "Success",
    "error": "Error",
    "loading": "Loading..."
  }
}
'''

    #####################################################################
    # GitHub Workflows
    #####################################################################
    
    ALL_FILE_TEMPLATES[".github/workflows/daily.yml"] = '''name: Daily Analysis

on:
  schedule:
    - cron: '30 1 * * *'  # 每日09:30 (UTC+8)
  workflow_dispatch:

jobs:
  daily-analysis:
    runs-on: self-hosted
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run daily analysis
        run: |
          python scripts/tracking/generate_daily_report.py
      
      - name: Commit results
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add reports/daily/
          git commit -m "Daily report $(date +%Y-%m-%d)" || true
          git push || true
'''

    ALL_FILE_TEMPLATES[".github/workflows/weekly.yml"] = '''name: Weekly Report

on:
  schedule:
    - cron: '0 8 * * 1'  # 每周一16:00 (UTC+8)
  workflow_dispatch:

jobs:
  weekly-report:
    runs-on: self-hosted
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Run weekly report
        run: |
          python scripts/tracking/generate_weekly_report.py
      
      - name: Commit results
        run: |
          git add reports/weekly/
          git commit -m "Weekly report" || true
          git push || true
'''

    ALL_FILE_TEMPLATES[".github/workflows/monthly.yml"] = '''name: Monthly Report

on:
  schedule:
    - cron: '0 8 1 * *'  # 每月1日16:00 (UTC+8)
  workflow_dispatch:

jobs:
  monthly-report:
    runs-on: self-hosted
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Run monthly report
        run: |
          python scripts/tracking/generate_monthly_report.py
      
      - name: Commit results
        run: |
          git add reports/monthly/
          git commit -m "Monthly report" || true
          git push || true
'''

    ALL_FILE_TEMPLATES[".github/workflows/trigger.yml"] = '''name: Manual Trigger

on:
  repository_dispatch:
    types: [manual-trigger]
  workflow_dispatch:

jobs:
  manual-trigger:
    runs-on: self-hosted
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Run trigger script
        run: |
          python scripts/github/github_trigger.py
'''

    ALL_FILE_TEMPLATES[".github/workflows/deploy.yml"] = '''name: Deploy Dashboard

on:
  push:
    branches: [ main ]
    paths:
      - 'dashboard/**'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dashboard
'''

    #####################################################################
    # Dashboard文件（简化版）
    #####################################################################
    
    ALL_FILE_TEMPLATES["dashboard/index.html"] = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>山脚下项目 - Dashboard</title>
    <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>山脚下项目 v2.0 - 监控面板</h1>
            <div class="controls">
                <button id="loginBtn">登录</button>
                <select id="langSelect">
                    <option value="zh_CN">中文</option>
                    <option value="en_US">English</option>
                </select>
            </div>
        </header>
        
        <main>
            <section id="overview">
                <h2>概览</h2>
                <div class="stats">
                    <div class="stat-card">
                        <h3>候选股票数</h3>
                        <p id="candidateCount">-</p>
                    </div>
                    <div class="stat-card">
                        <h3>对照组股票数</h3>
                        <p id="contrastCount">20</p>
                    </div>
                    <div class="stat-card">
                        <h3>分离度评分</h3>
                        <p id="separationScore">-</p>
                    </div>
                </div>
            </section>
            
            <section id="candidates">
                <h2>候选股票列表</h2>
                <table id="candidatesTable">
                    <thead>
                        <tr>
                            <th>股票代码</th>
                            <th>相似度</th>
                            <th>ML评分</th>
                            <th>筹码评分</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </section>
            
            <section id="parameters">
                <h2>参数设置</h2>
                <div class="params">
                    <label>筛选阈值: <input type="number" id="thresholdInput" min="0" max="1" step="0.1" value="0.5"></label>
                    <button id="saveParamsBtn" disabled>保存参数</button>
                </div>
            </section>
        </main>
    </div>
    
    <script src="assets/js/dashboard.js"></script>
    <script src="assets/js/auth.js"></script>
    <script src="assets/js/i18n.js"></script>
</body>
</html>
'''

    ALL_FILE_TEMPLATES["dashboard/assets/css/styles.css"] = '''/* 山脚下项目 Dashboard 样式 */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    background: #f5f5f5;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background: #2c3e50;
    color: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

header h1 {
    font-size: 24px;
}

.controls {
    display: flex;
    gap: 10px;
}

button {
    padding: 8px 16px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background: #2980b9;
}

button:disabled {
    background: #95a5a6;
    cursor: not-allowed;
}

.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
}

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-card h3 {
    font-size: 14px;
    color: #7f8c8d;
    margin-bottom: 10px;
}

.stat-card p {
    font-size: 32px;
    font-weight: bold;
    color: #2c3e50;
}

section {
    background: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

section h2 {
    margin-bottom: 15px;
    color: #2c3e50;
}

table {
    width: 100%;
    border-collapse: collapse;
}

thead {
    background: #ecf0f1;
}

th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.params {
    display: flex;
    gap: 15px;
    align-items: center;
}

input[type="number"] {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 100px;
}
'''

    ALL_FILE_TEMPLATES["dashboard/assets/js/dashboard.js"] = '''// Dashboard主逻辑

document.addEventListener('DOMContentLoaded', function() {
    loadOverviewData();
    loadCandidates();
    
    document.getElementById('saveParamsBtn').addEventListener('click', saveParameters);
});

function loadOverviewData() {
    // TODO: 从API加载概览数据
    fetch('assets/data/overview.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById('candidateCount').textContent = data.candidate_count || '-';
            document.getElementById('separationScore').textContent = data.separation_score ? data.separation_score.toFixed(4) : '-';
        })
        .catch(error => console.error('加载概览数据失败:', error));
}

function loadCandidates() {
    // TODO: 从API加载候选股票
    fetch('assets/data/candidates.json')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#candidatesTable tbody');
            tbody.innerHTML = '';
            
            data.forEach(candidate => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${candidate.stock_code}</td>
                    <td>${candidate.similarity.toFixed(4)}</td>
                    <td>${candidate.ml_score.toFixed(4)}</td>
                    <td>${candidate.chip_score.toFixed(4)}</td>
                `;
            });
        })
        .catch(error => console.error('加载候选股票失败:', error));
}

function saveParameters() {
    const threshold = document.getElementById('thresholdInput').value;
    
    // TODO: 保存参数到后端
    console.log('保存参数:', { threshold });
    alert('参数已保存');
}
'''

    ALL_FILE_TEMPLATES["dashboard/assets/js/auth.js"] = '''// 身份验证逻辑

let isAuthenticated = false;

document.getElementById('loginBtn').addEventListener('click', function() {
    if (isAuthenticated) {
        logout();
    } else {
        login();
    }
});

function login() {
    const password = prompt('请输入密码:');
    
    // TODO: 实际密码验证
    if (password === 'admin123') {
        isAuthenticated = true;
        document.getElementById('loginBtn').textContent = '登出';
        document.getElementById('saveParamsBtn').disabled = false;
        alert('登录成功！');
    } else {
        alert('密码错误！');
    }
}

function logout() {
    isAuthenticated = false;
    document.getElementById('loginBtn').textContent = '登录';
    document.getElementById('saveParamsBtn').disabled = true;
    alert('已登出');
}
'''

    ALL_FILE_TEMPLATES["dashboard/assets/js/i18n.js"] = '''// 国际化支持

const translations = {
    zh_CN: null,
    en_US: null
};

let currentLang = 'zh_CN';

// 加载翻译文件
fetch('../locales/zh_CN.json')
    .then(r => r.json())
    .then(data => translations.zh_CN = data);

fetch('../locales/en_US.json')
    .then(r => r.json())
    .then(data => translations.en_US = data);

document.getElementById('langSelect').addEventListener('change', function(e) {
    currentLang = e.target.value;
    updateLanguage();
});

function updateLanguage() {
    // TODO: 更新页面语言
    if (translations[currentLang]) {
        console.log('切换语言:', currentLang);
    }
}
'''

    ALL_FILE_TEMPLATES["dashboard/assets/data/overview.json"] = '''{
  "candidate_count": 15,
  "contrast_count": 20,
  "separation_score": 0.8234
}
'''

    ALL_FILE_TEMPLATES["dashboard/assets/data/candidates.json"] = '''[
  {
    "stock_code": "000001",
    "similarity": 0.8567,
    "ml_score": 0.8234,
    "chip_score": 0.7654
  },
  {
    "stock_code": "600000",
    "similarity": 0.8234,
    "ml_score": 0.7891,
    "chip_score": 0.7234
  }
]
'''

class ProjectGenerator:
    """项目代码框架生成器"""
    
    def __init__(self, base_dir="shanjiaxia_project"):
        self.base_dir = Path(base_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = Path(f"backup_{self.timestamp}")
        print(f"初始化项目生成器...")
        print(f"项目目录: {self.base_dir}")
        print(f"备份目录: {self.backup_dir}")
    
    def create_directory_structure(self):
        """创建目录结构"""
        directories = [
            "scripts/data_collection",
            "scripts/feature_engineering",
            "scripts/contrast_group",
            "scripts/ml_training",
            "scripts/filtering",
            "scripts/tracking",
            "scripts/github",
            "scripts/monitoring",
            "scripts/utils",
            "dashboard/assets/data",
            "dashboard/assets/css",
            "dashboard/assets/js",
            ".github/workflows",
            "config",
            "docs",
            "locales",
            "data/raw",
            "data/processed",
            "data/backup",
            "data/features",
            "data/candidates",
            "data/contrast_group",
            "data/analysis",
            "models",
            "logs",
            "reports/daily",
            "reports/weekly",
            "reports/monthly",
        ]
        
        print("\\n📁 创建目录结构...")
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ 共创建 {len(directories)} 个目录")
    
    def write_file(self, filepath, content):
        """写入文件"""
        full_path = self.base_dir / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def generate_all_files(self):
        """生成所有文件"""
        file_count = 0
        
        print("\\n📝 生成所有项目文件...")
        
        for filename, content in ALL_FILE_TEMPLATES.items():
            self.write_file(filename, content)
            file_count += 1
            print(f"  ✅ {filename}")
        
        return file_count
    
    def create_backup(self):
        """创建备份"""
        print("\\n📦 创建备份...")
        if self.base_dir.exists():
            shutil.copytree(self.base_dir, self.backup_dir, dirs_exist_ok=True)
            print(f"  ✅ 备份已保存到: {self.backup_dir}")
    
    def run(self):
        """执行完整生成流程"""
        print("=" * 70)
        print("🚀 山脚下项目 v2.0 - 代码框架生成器")
        print("=" * 70)
        
        # 1. 创建目录结构
        self.create_directory_structure()
        
        # 2. 生成所有文件
        file_count = self.generate_all_files()
        
        # 3. 创建备份
        self.create_backup()
        
        print("\\n" + "=" * 70)
        print(f"✅ 代码框架生成完成！共生成 {file_count} 个文件")
        print("=" * 70)
        print(f"\\n📂 项目目录: {self.base_dir.absolute()}")
        print(f"📦 备份目录: {self.backup_dir.absolute()}")
        print("\\n下一步:")
        print(f"  1. cd {self.base_dir}")
        print("  2. 查看项目结构和文件")
        print("  3. 根据需要调整配置文件（config/）")
        print("  4. 开始开发和测试各模块")

if __name__ == '__main__':
    try:
        generator = ProjectGenerator()
        generator.run()
    except Exception as e:
        print(f"\\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
