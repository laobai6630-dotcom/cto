#!/usr/bin/env python3
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
