#!/usr/bin/env python3
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
        report.append("# 模型评估报告\n")
        report.append("## 评估指标\n")
        
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
        
        report.append("\n## 结论\n")
        
        best_model = max(metrics.items(), key=lambda x: x[1]['f1_score'])
        report.append(f"最佳模型: **{best_model[1]['model_name']}** (F1 Score: {best_model[1]['f1_score']:.4f})\n")
        
        report_file = self.output_dir / 'evaluation_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        logging.info(f"评估报告已保存: {report_file}")
        
        print("\n✅ 模型评估完成:")
        for model_name, m in metrics.items():
            print(f"  {m['model_name']}: Accuracy={m['accuracy']:.4f}, F1={m['f1_score']:.4f}")

if __name__ == '__main__':
    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate_all_models()
