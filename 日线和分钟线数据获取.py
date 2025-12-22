#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日线和分钟线数据获取程序
这是原有的数据采集程序，由调度系统调用
"""

import sys
import time
from datetime import datetime
from pathlib import Path

def main():
    print(f"[{datetime.now()}] 开始采集日线和分钟线数据...")
    
    # 模拟数据采集过程
    time.sleep(2)
    
    # 输出数据到指定目录
    output_dir = Path(__file__).parent / "daily_minute_data"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"daily_data_{datetime.now().strftime('%Y%m%d')}.csv"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("timestamp,symbol,open,high,low,close,volume\n")
        f.write(f"{datetime.now()},000001,10.0,10.5,9.8,10.2,1000000\n")
    
    print(f"[{datetime.now()}] 数据采集完成，输出文件: {output_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
