# 数据采集调度系统

## 📋 概述

本目录包含山脚下项目的数据采集调度系统，使用 APScheduler 实现自动化定时采集。

## 🗂️ 文件结构

```
data_collection/
├── scheduler_main.py          # 主调度程序（日线、周线、月线）
├── scheduler_financial.py     # 财务数据调度程序（独立运行）
├── data_cleaning.py           # 数据清洗工具
└── README.md                  # 本文档
```

## 🚀 使用方法

### 1. 主调度程序 (scheduler_main.py)

负责调度日线、周线、月线数据采集任务。

**启动方式：**
```bash
cd /home/engine/project/projects/山脚下/scripts/data_collection
python3 scheduler_main.py
```

**调度任务：**
- **日线和分钟线数据**：每日 09:00（周二至周日）
- **周线数据**：每周二 16:00
- **月线数据**：每月1日 16:00（遇周一顺延）

**避开周一逻辑：**
- 所有任务自动避开周一执行
- 月线数据如遇周一则自动顺延到周二

### 2. 财务调度程序 (scheduler_financial.py)

独立调度财务和基本面数据采集，每季度连续运行7天。

**启动方式：**
```bash
cd /home/engine/project/projects/山脚下/scripts/data_collection
python3 scheduler_financial.py
```

**调度逻辑：**
- **启动时间**：每季度第二天 11:30（1月2日、4月2日、7月2日、10月2日）
- **运行周期**：连续7天，每天 11:30 执行一次
- **避开周一**：如果季度第二天是周一，则顺延到周二；7天内遇到周一则跳过

**进度跟踪：**
- 自动记录采集进度（N/7天）
- 日志文件记录详细执行情况

## 📁 路径配置

所有路径配置统一管理在 `config/path_config.py`：

```python
from config import path_config

# 采集程序路径
path_config.COLLECT_DAILY_MINUTE_PY   # 日线和分钟线
path_config.COLLECT_WEEKLY_PY         # 周线
path_config.COLLECT_MONTHLY_PY        # 月线
path_config.COLLECT_FINANCIAL_PY      # 财务

# 数据输出路径
path_config.DAILY_DATA_DIR            # daily_minute_data/
path_config.WEEKLY_DATA_DIR           # weekly_data/
path_config.MONTHLY_DATA_DIR          # monthly_data/
path_config.FINANCIAL_DATA_DIR        # financial_data/

# 日志路径
path_config.SCHEDULER_MAIN_LOG        # logs/scheduler_main.log
path_config.SCHEDULER_FINANCIAL_LOG   # logs/scheduler_financial.log
```

## 📊 日志文件

### scheduler_main.log
主调度程序的执行日志，包含：
- 任务启动/完成时间
- 执行状态（成功/失败）
- 耗时统计
- 错误信息

### scheduler_financial.log
财务调度程序的执行日志，包含：
- 7天采集计划
- 每日执行进度
- 采集完成汇总

**日志格式示例：**
```
[2025-12-22 09:00:15] INFO: ============================================================
[2025-12-22 09:00:15] INFO: 开始执行任务: 日线和分钟线数据采集
[2025-12-22 09:00:15] INFO: 程序路径: /home/engine/project/日线和分钟线数据获取.py
[2025-12-22 09:05:30] INFO: ✅ SUCCESS: 日线和分钟线数据采集 执行成功
[2025-12-22 09:05:30] INFO: ⏱️  耗时: 315.23 秒
[2025-12-22 09:05:30] INFO: ============================================================
```

## ⚠️ 注意事项

1. **避开周一规则**
   - 所有采集任务自动避开周一执行
   - 确保数据采集在交易日进行

2. **独立运行**
   - `scheduler_main.py` 和 `scheduler_financial.py` 独立运行
   - 互不干扰，可同时启动

3. **异常处理**
   - 采集失败会记录到日志
   - 程序不会因单次失败而停止
   - 超时时间：日线/周线/月线 1小时，财务 2小时

4. **路径验证**
   - 启动时自动验证所有必需路径
   - 缺失目录会自动创建
   - 缺失采集程序会报错退出

## 🔧 依赖包

```bash
pip install APScheduler>=3.10.0
```

## 📝 维护建议

1. **定期检查日志**
   - 每周检查 `logs/` 目录下的日志文件
   - 关注错误和警告信息

2. **监控磁盘空间**
   - 数据文件存储在项目根目录
   - 定期清理历史数据

3. **更新采集程序**
   - 修改采集程序后无需重启调度器
   - 调度器会调用最新版本的采集程序

## 🐛 故障排查

**问题：调度器无法启动**
- 检查 APScheduler 是否已安装
- 验证 `config/path_config.py` 是否正确

**问题：任务未执行**
- 检查当前日期是否为周一
- 查看日志文件了解详细信息

**问题：采集程序报错**
- 检查采集程序是否存在
- 验证数据输出目录是否有写权限
- 查看对应的日志文件获取错误详情

## 📞 联系方式

如有问题，请查看项目文档或提交 Issue。
