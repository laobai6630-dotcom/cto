#!/usr/bin/env python3
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
        
        print(f"\n✅ 递进筛选完成:")
        print(f"  选择阈值: {selected_threshold}")
        print(f"  候选数量: {len(final_candidates)}")
        
        return final_candidates

if __name__ == '__main__':
    filter = ProgressiveFilter()
    candidates = filter.progressive_filter()
