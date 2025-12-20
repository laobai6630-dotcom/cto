# 山脚下项目 v2.0

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
