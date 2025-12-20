# 山脚下项目 v2.0 - 完整代码框架

## 📊 项目概述

A股"山脚下"形态股票精准筛选系统 - 完整的Python项目框架

本项目基于山脚下项目计划v2.0（`projects/山脚下/项目计划.md`）自动生成，包含所有必需的Python脚本、Dashboard网页、配置文件、文档和GitHub工作流。

## ✨ 核心功能

1. **数据采集**: 180天数据保留期，支持日线/周线/月线/财务数据
2. **特征工程**: 88个特征（134原始+10AI+10筹码）
3. **对照组分析**: 跌幅前20名股票对比，分离度评分
4. **ML模型**: 3个模型集成（Logistic Regression + Random Forest + XGBoost）
5. **相似度筛选**: 递进筛选（50%→40%→30%）
6. **30天跟踪**: 动态跟踪候选股票表现
7. **Dashboard**: 中英双语监控面板，密码保护
8. **GitHub Workflows**: 自动化日报/周报/月报生成

## 📂 项目结构

```
shanjiaxia_project/
├── scripts/                    # Python脚本模块
│   ├── data_collection/       # 数据采集
│   ├── feature_engineering/    # 特征工程
│   ├── contrast_group/        # 对照组分析
│   ├── ml_training/           # ML模型训练
│   ├── filtering/             # 相似度筛选
│   ├── tracking/              # 跟踪报告
│   ├── github/                # GitHub自动化
│   ├── monitoring/            # 监督报告
│   └── utils/                 # 工具类
├── dashboard/                  # Dashboard网页
│   ├── index.html             # 主页面
│   ├── assets/
│   │   ├── css/               # 样式文件
│   │   ├── js/                # JavaScript逻辑
│   │   └── data/              # 数据文件
├── .github/workflows/          # GitHub Actions工作流
│   ├── daily.yml              # 日分析
│   ├── weekly.yml             # 周报告
│   ├── monthly.yml            # 月报告
│   ├── trigger.yml            # 手动触发
│   └── deploy.yml             # Dashboard部署
├── config/                     # 配置文件
│   ├── config.json            # 主配置
│   ├── weights.json           # 权重配置
│   └── parameters.json        # 参数配置
├── docs/                       # 文档
│   ├── README.md              # 项目说明
│   ├── ARCHITECTURE.md        # 系统架构
│   ├── API_REFERENCE.md       # API参考
│   ├── DEPLOYMENT.md          # 部署指南
│   ├── MAINTENANCE.md         # 运维手册
│   └── CHANGELOG.md           # 版本日志
├── locales/                    # 国际化
│   ├── zh_CN.json             # 中文翻译
│   └── en_US.json             # 英文翻译
├── data/                       # 数据目录
│   ├── raw/                   # 原始数据
│   ├── processed/             # 处理后数据
│   ├── backup/                # 备份数据
│   ├── features/              # 特征数据
│   ├── candidates/            # 候选股票
│   ├── contrast_group/        # 对照组
│   └── analysis/              # 分析结果
├── models/                     # ML模型文件
├── logs/                       # 日志文件
└── reports/                    # 报告输出
    ├── daily/                 # 日报
    ├── weekly/                # 周报
    └── monthly/               # 月报
```

## 📝 生成的文件清单

### Python脚本 (24个)

**数据采集模块** (2个):
- `scripts/data_collection/scheduler_main.py` - 主调度程序
- `scripts/data_collection/data_cleaning.py` - 数据清洗

**特征工程模块** (5个):
- `scripts/feature_engineering/feature_extraction.py` - 134原始特征提取
- `scripts/feature_engineering/ai_feature_synthesis.py` - 10个AI特征合成
- `scripts/feature_engineering/chip_distribution.py` - 10个筹码特征计算
- `scripts/feature_engineering/feature_normalization.py` - 特征标准化
- `scripts/feature_engineering/feature_importance.py` - 特征重要性分析

**对照组模块** (3个):
- `scripts/contrast_group/identify_contrast_group.py` - 识别对照组
- `scripts/contrast_group/extract_contrast_features.py` - 提取对照组特征
- `scripts/contrast_group/compare_contrast_vs_candidates.py` - 对比分析

**ML训练模块** (3个):
- `scripts/ml_training/model_training.py` - 训练3个基础模型
- `scripts/ml_training/model_ensemble.py` - 模型集成
- `scripts/ml_training/model_evaluation.py` - 模型评估

**筛选模块** (2个):
- `scripts/filtering/similarity_filter.py` - 相似度筛选
- `scripts/filtering/filtering_logic.py` - 递进筛选逻辑

**跟踪报告模块** (5个):
- `scripts/tracking/track_candidates_30d.py` - 30天跟踪
- `scripts/tracking/performance_evaluation.py` - 效果评估
- `scripts/tracking/generate_daily_report.py` - 日报生成
- `scripts/tracking/generate_weekly_report.py` - 周报生成
- `scripts/tracking/generate_monthly_report.py` - 月报生成

**GitHub自动化模块** (1个):
- `scripts/github/github_trigger.py` - GitHub触发机制

**监督报告模块** (1个):
- `scripts/monitoring/generate_supervisory_report.py` - 监督报告生成

**工具类模块** (2个):
- `scripts/utils/backup_manager.py` - 备份管理
- `scripts/utils/verify_backup.py` - 备份验证

### Dashboard文件 (7个)

- `dashboard/index.html` - 主页面
- `dashboard/assets/css/styles.css` - 样式文件
- `dashboard/assets/js/dashboard.js` - Dashboard逻辑
- `dashboard/assets/js/auth.js` - 身份验证
- `dashboard/assets/js/i18n.js` - 国际化支持
- `dashboard/assets/data/overview.json` - 概览数据
- `dashboard/assets/data/candidates.json` - 候选数据

### GitHub Workflows (5个)

- `.github/workflows/daily.yml` - 日分析工作流
- `.github/workflows/weekly.yml` - 周报告工作流
- `.github/workflows/monthly.yml` - 月报告工作流
- `.github/workflows/trigger.yml` - 手动触发工作流
- `.github/workflows/deploy.yml` - Dashboard部署工作流

### 配置文件 (3个)

- `config/config.json` - 主配置文件
- `config/weights.json` - 权重配置
- `config/parameters.json` - 参数配置

### 文档文件 (6个)

- `docs/README.md` - 项目总览
- `docs/ARCHITECTURE.md` - 系统架构
- `docs/API_REFERENCE.md` - API参考
- `docs/DEPLOYMENT.md` - 部署指南
- `docs/MAINTENANCE.md` - 运维手册
- `docs/CHANGELOG.md` - 版本日志

### 本地化文件 (2个)

- `locales/zh_CN.json` - 中文翻译
- `locales/en_US.json` - 英文翻译

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖包：
- `pandas` - 数据处理
- `numpy` - 数值计算
- `scikit-learn` - 机器学习
- `xgboost` - 梯度提升
- `lightgbm` - 轻量级梯度提升
- `schedule` - 任务调度
- `ta-lib` - 技术分析
- `scipy` - 科学计算

### 2. 配置项目

编辑 `config/config.json`:

```json
{
  "project_name": "山脚下项目 v2.0",
  "data_retention_days": 180,
  "feature_time_window": 20,
  "github_token": "YOUR_GITHUB_TOKEN",
  "github_repo": "laobai6630-dotcom/cto",
  "dashboard_password": "admin123"
}
```

### 3. 运行模块

**数据采集**:
```bash
python scripts/data_collection/scheduler_main.py
```

**特征提取**:
```bash
python scripts/feature_engineering/feature_extraction.py
```

**模型训练**:
```bash
python scripts/ml_training/model_training.py
python scripts/ml_training/model_ensemble.py
python scripts/ml_training/model_evaluation.py
```

**生成报告**:
```bash
python scripts/tracking/generate_daily_report.py
python scripts/tracking/generate_weekly_report.py
python scripts/tracking/generate_monthly_report.py
```

### 4. 启动Dashboard

打开 `dashboard/index.html` 在浏览器中查看监控面板。

默认密码: `admin123` (可在 `config/config.json` 中修改)

## 📊 核心流程

### 1. 数据采集流程

```
日线数据采集 → 数据清洗 → 数据标准化 → 历史备份（180天）
```

### 2. 特征工程流程

```
原始数据 → 134原始特征 → 10 AI特征 → 10筹码特征 → 标准化 → 选择Top 88特征
```

### 3. 对照组分析流程

```
识别跌幅前20名 → 提取对照组特征 → 对比分离度分析 → 验证特征有效性
```

### 4. ML模型训练流程

```
成功样本 + 对照组 → 训练LR/RF/XGB → 模型集成 → 模型评估 → 保存模型
```

### 5. 筛选流程

```
候选股票 → 相似度计算 → 递进筛选(50%→40%→30%) → 最终候选 → 30天跟踪
```

## 🔑 核心参数

### 数据参数
- **数据保留期**: 180个交易日
- **特征时间窗口**: 20个交易日
- **对照组规模**: 20只股票

### 特征参数
- **原始特征**: 134个
- **AI特征**: 10个（权重1.5倍）
- **筹码特征**: 10个
- **最终特征**: 88个

### 模型参数
- **模型数量**: 3个（LR + RF + XGB）
- **集成权重**: LR(0.4) + RF(0.3) + GB(0.3)
- **目标精度**: ≥0.85

### 筛选参数
- **相似度权重**: ML(0.6) + 筹码(0.2) + 消息面(0.2)
- **筛选阈值**: 50% → 40% → 30%
- **候选范围**: 5-20只股票

### 跟踪参数
- **跟踪周期**: 30个交易日
- **成功阈值**: 涨幅>50%

## 💡 使用说明

### Dashboard使用

1. **无密码模式**: 可以浏览所有数据，但不能修改参数
2. **登录模式**: 输入密码后可以修改筛选参数
3. **语言切换**: 支持中文/英文切换
4. **实时刷新**: 自动加载最新的候选股票和对照组数据

### GitHub Workflows使用

1. **自动触发**: 根据cron表达式自动运行
2. **手动触发**: 在GitHub Actions页面手动触发
3. **本地运行**: 需要配置self-hosted runner
4. **查看结果**: 报告自动提交到仓库

## 📈 性能指标

### 模型性能
- **准确率**: ≥0.85
- **精确率**: ≥0.80
- **召回率**: ≥0.75
- **F1分数**: ≥0.80
- **AUC-ROC**: ≥0.80

### 对照组指标
- **分离度评分**: ≥0.80
- **欧氏距离**: 尽可能大
- **余弦距离**: 尽可能大
- **分布重叠度**: ≤0.20

## 🛠️ 开发指南

### 添加新特征

1. 在 `feature_extraction.py` 中添加新的特征提取方法
2. 在 `feature_normalization.py` 中更新特征列表
3. 重新训练模型

### 调整模型参数

编辑 `config/weights.json`:

```json
{
  "model_ensemble_weights": {
    "lr": 0.4,
    "rf": 0.3,
    "gb": 0.3
  }
}
```

### 修改筛选阈值

编辑 `config/parameters.json`:

```json
{
  "filtering": {
    "thresholds": [0.5, 0.4, 0.3],
    "min_candidates": 5,
    "max_candidates": 20
  }
}
```

## 📝 日志和监控

### 日志文件位置
- 数据采集: `logs/scheduler.log`
- 数据清洗: `logs/data_cleaning.log`
- 特征提取: `logs/feature_extraction.log`
- AI特征: `logs/ai_feature_synthesis.log`
- 筹码分布: `logs/chip_distribution.log`
- 对照组: `logs/contrast_group.log`
- ML训练: `logs/ml_training.log`
- 筛选: `logs/filtering.log`
- 跟踪: `logs/tracking.log`
- 备份: `logs/backup.log`

### 监控指标
- 数据采集成功率
- 特征提取完整性
- 模型预测精度
- 候选股票数量
- 跟踪成功率

## 🔒 安全性

1. **密码保护**: Dashboard需要密码才能修改参数
2. **GitHub Token**: 使用环境变量或GitHub Secrets存储
3. **数据备份**: 自动备份，保留180天
4. **备份验证**: 定期验证备份完整性

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 📞 联系方式

- **GitHub**: https://github.com/laobai6630-dotcom/cto/
- **项目路径**: `projects/山脚下/`

## 🙏 致谢

感谢所有为山脚下项目v2.0做出贡献的人！

---

**生成时间**: 2025-12-19  
**生成工具**: `generate_all_files.py`  
**版本**: v2.0
