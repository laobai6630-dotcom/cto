#!/usr/bin/env python3
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
        
        print("\n✅ 模型训练完成:")
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
