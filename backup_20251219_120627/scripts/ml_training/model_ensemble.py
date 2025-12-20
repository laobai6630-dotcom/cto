#!/usr/bin/env python3
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
        
        print("\n✅ 模型集成完成:")
        print(f"  权重配置: {self.weights}")
        print(f"  集成模型: {model_file}")
        
        return ensemble_model

if __name__ == '__main__':
    ensembler = ModelEnsembler()
    ensemble_model = ensembler.create_ensemble()
