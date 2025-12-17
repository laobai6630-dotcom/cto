# cto
山脚下
# 山脚下项目 - 完整重建计划书（最终版）

**项目名称**：山脚下 - A股"山脚下"形态股票精准筛选系统  
**最后更新时间**：2025-12-15  
**项目状态**：规划完成，待启动  
**负责人**：项目经理  

---

## 📑 完整目录

1. [项目概述](#项目概述)
2. [核心改动](#核心改动)
3. [完整树状结构](#完整树状结构)
4. [数据架构](#数据架构)
5. [88个特征体系](#88个特征体系)
6. [筹码分布详解](#筹码分布详解)
7. [机器学习方案](#机器学习方案)
8. [GitHub触发机制](#github触发机制)
9. [网页功能详解](#网页功能详解)
10. [员工配置](#员工配置)
11. [4阶段实现路线图](#4阶段实现路线图)
12. [每步确认机制](#每步确认机制)
13. [框架备份策略](#框架备份策略)
14. [项目资源清单](#项目资源清单)

---

## 🎯 项目概述

### 项目灵感与核心目标

**项目命名**：山脚下

**灵感来源**：
股票K线形态。作为股票投资领域的入门者，我最初的分析聚焦于日K线走势：当某只股票的K线在一段时期内呈现出平稳运行的态势，随后突然出现大幅拉升，继而又回落至前期的平稳区间，其整体形态恰似一片平原之上陡然隆起一座高峰。

其中，**"拉升日"** 被定义为股价开启连续拉升走势的首个交易日。

### 项目实施计划（4步骤）

1. **标的筛选**：以A股全市场股票为研究对象，划定时间范围为当日向前追溯 **30个交易日**，筛选出此区间内股价涨幅超过 **50%** 的股票。

2. **特征提炼**：深度剖析上述高涨幅股票的共性特征，构建 **88个特征指标体系**（包括原始特征、AI合成特征、筹码分布特征）。

3. **标的再筛选**：将已筛选出的高涨幅股票剔除，从剩余A股标的中，利用机器学习模型筛选出与前述特征指标相匹配的股票（支持 **50% → 40% → 30%** 递进筛选）。

4. **动态跟踪与策略优化**：借助人工智能技术，持续跟踪上述符合特征的股票在未来 **30个交易日** 内的市场表现，并基于实时数据动态迭代、优化分析策略。

### 核心逻辑流程图

数据采集（4程序）
↓
特征提取（88个特征）
↓
特征工程（标准化+缩放）
↓
ML训练（3模型+集成）
↓
相似度筛选（50%→40%→30%）
↓
30天动态跟踪
↓
反馈循环优化 ←── 筹码分布 + 消息面 + 市场情绪


### 关键要求确认清单

- ✅ **7项同等级要求**（所有功能必须实现）
  - 1️⃣ 框架不管由谁生成，都要给一个备份
  - 2️⃣ 每完成一步要用户确认才能写入步骤完成
  - 3️⃣ 同步GitHub要随时提醒
  - 4️⃣ 项目增加一个员工负责消息面分析
  - 5️⃣ 需要一个网页观察GitHub工作进度（包括可调整的功能按钮）
  - 6️⃣ 网页中英文双语，所有按钮都有中文
  - 7️⃣ 网页有密码：无密码可浏览，输入密码才能修改

- ✅ **新增要求**
  - 增加一位监督员工（项目监督、工作流监督、问题报告，报告中文展示在网页）
  - 所有可调整参数都要在网页留操作按钮
  - GitHub要有触发机制（程序间协调，不能自主决定启动时间）
  - 筹码分布算入分析元素，权重可调
  - 本地自动化数据同步到GitHub（谨慎，不超限，不影响分析）

- ✅ **不删除已合并的GitHub PR**

---

## 💡 核心改动

### 相比初稿的7项核心改动

| # | 改动项 | 初稿 | 本稿 | 影响范围 |
|---|--------|------|------|---------|
| 1 | 特征数量 | 70-80个 | **88个**（+筹码分布） | 特征体系、ML模型 |
| 2 | 筹码分布 | 简述 | **独立维度**，权重0.2 | 相似度筛选、Dashboard |
| 3 | 消息面分析 | 人工 | **新增员工职位** | 员工配置、日报、Dashboard |
| 4 | GitHub触发 | 定时 | **事件驱动+触发机制** | workflow配置、github_trigger.py |
| 5 | 密码保护 | 无 | **必需**（查看/修改分层） | 网页认证、auth.js |
| 6 | 框架备份 | 无 | **每阶段生成+版本控制** | 项目管理、进度跟踪 |
| 7 | 监督员工 | 无 | **新增职位**（工作流监督） | 员工配置、Dashboard报告 |

---

## 📊 完整树状结构

### 📍 第1层：数据存储（D:\cto\data\）❌ 不上传GitHub

D:\cto
│
└─ 📂 data/
│
├─ 📂 daily_minute_data/ [程序1生成] 日线+分钟线
│ ├─ ✅ daily_data.csv [日更新] 最近30个交易日
│ │ └─ 字段：日期、代码、开盘、最高、最低、收盘、前收盘、成交量、成交额、复权状态、换手率、交易状态、涨跌幅、市盈率、市净率、市销率、市现率、ST标识（18个）
│ ├─ ✅ minute_10min_data.csv [日更新] 最近5个交易日（10分钟）
│ ├─ ✅ minute_30min_data.csv [日更新] 最近5个交易日（30分钟）
│ ├─ ✅ minute_60min_data.csv [日更新] 最近5个交易日（60分钟）
│ └─ 📂 backup/
│ └─ ✅ daily_data_backup_.csv [自动备份，超30天自删]
│
├─ 📂 weekly_data/ [程序2生成] 周线
│ ├─ ✅ weekly_data.csv [周更新] 最近52周
│ │ └─ 字段：日期、代码、开盘、最高、最低、收盘、成交量、成交额、复权状态、换手率、涨跌幅（11个）
│ └─ 📂 backup/
│ └─ ✅ weekly_data_backup_.csv [自动备份，超52周自删]
│
├─ 📂 monthly_data/ [程序3生成] 月线
│ ├─ ✅ monthly_data.csv [月更新] 最近60个月
│ │ └─ 字段：日期、代码、开盘、最高、最低、收盘、成交量、成交额、复权状态、换手率、涨跌幅（11个）
│ └─ 📂 backup/
│ └─ ✅ monthly_data_backup_.csv [自动备份，超60月自删]
│
├─ 📂 financial_data/ [程序4生成] 财务数据
│ ├─ ✅ basic_info.csv [季度更新] 基本信息
│ ├─ ✅ profit_data.csv [季度更新] 利润表（8季度）
│ ├─ ✅ operation_data.csv [季度更新] 运营数据
│ ├─ ✅ growth_data.csv [季度更新] 成长数据
│ ├─ ✅ balance_data.csv [季度更新] 资产负债表
│ ├─ ✅ cash_flow_data.csv [季度更新] 现金流量表
│ ├─ ✅ dupont_data.csv [季度更新] 杜邦分析
│ ├─ ✅ download_progress.json [季度更新] 下载进度
│ └─ 📂 backup/
│ └─ ✅ financial_data_backup_.csv [自动备份，超8季度自删]
│
├─ 📂 analysis_output/ [分析脚本生成] ⬜ 上传GitHub
│ │
│ ├─ 📂 success_samples/
│ │ ├─ ⬜ success_samples.csv [日生成] 30天涨幅>50%成功样本
│ │ ├─ ⬜ success_samples_40pct.csv [日生成] 备选（40%）
│ │ └─ ⬜ success_samples_30pct.csv [日生成] 备选（30%）
│ │
│ ├─ 📂 feature_extraction/
│ │ ├─ ⬜ raw_features.csv [日生成] 134个原始特征
│ │ ├─ ⬜ ai_synthetic_features.csv [日生成] 10个AI特征
│ │ ├─ ⬜ all_features_88.csv [日生成] 88个特征（最终）
│ │ ├─ ⬜ feature_importance_ranking.csv [日生成] ✅ 特征重要性排名 路径标注✅
│ │ └─ ⬜ normalized_features.csv [日生成] 标准化后88个特征
│ │
│ ├─ 📂 chip_distribution/ ⬜ 新增 筹码分布
│ │ ├─ ⬜ chip_features.csv [日生成] 10个筹码特征
│ │ ├─ ⬜ cost_distribution.csv [日生成] 分价位筹码分布
│ │ └─ ⬜ chip_analysis_report.json [日生成] 筹码分析报告
│ │
│ ├─ 📂 ml_models/ ⬜ 机器学习模型
│ │ ├─ ⬜ model_lr.pkl [日更新] 逻辑回归
│ │ ├─ ⬜ model_rf.pkl [日更新] 随机森林
│ │ ├─ ⬜ model_gb.pkl [日更新] 梯度提升
│ │ ├─ ⬜ model_ensemble.pkl [日更新] 集成模型
│ │ ├─ ⬜ feature_scaler.pkl [日更新] 特征缩放器
│ │ └─ ⬜ model_metrics.json [日生成] 评估指标
│ │
│ ├─ 📂 candidates/ ⬜ 候选股票结果
│ │ ├─ ⬜ candidates_50pct.csv [日生成] 相似度≥50%
│ │ ├─ ⬜ candidates_40pct.csv [日生成] 降级：≥40%
│ │ ├─ ⬜ candidates_30pct.csv [日生成] 降级：≥30%
│ │ ├─ ⬜ selection_candidates.csv [日生成] 最终选择
│ │ └─ ⬜ selection_metadata.json [日生成] 参数元数据
│ │
│ └─ 📂 reports/
│ ├─ ⬜ daily_summary_.json [日生成] 日报汇总
│ └─ ⬜ analysis_log_.log [日生成] 分析日志
│
└─ 📂 tracking_output/ ⬜ 上传GitHub
├─ ⬜ active_tracking.json [日更新] 实时跟踪数据
├─ ⬜ tracking_history.csv [日追加] 历史跟踪记录
└─ ⬜ performance_report.csv [周生成] 效果评估报告


**存储容量估算**：
- 日线数据：~35-45MB
- 周线数据：~30-40MB
- 月线数据：~40-50MB
- 财务数据：~30-50MB
- 分析输出：~100-200MB（可定期清理）
- **总计**：约300-500MB（可接受）

---

### 📍 第2层：Python脚本（D:\cto\scripts\）⬜ 上传GitHub

D:\cto
│
└─ 📂 scripts/
│
├─ 📂 data_collection/ [4个数据采集程序]
│ ├─ ✅ collect_daily_minute.py [程序1] 日线+分钟线采集
│ │ └─ 调度：APScheduler - 每日09:00
│ │ └─ 路径：D:\cto\scripts\data_collection\collect_daily_minute.py ✅
│ ├─ ✅ collect_weekly.py [程序2] 周线采集
│ │ └─ 调度：APScheduler - 每周一16:00
│ │ └─ 路径：D:\cto\scripts\data_collection\collect_weekly.py ✅
│ ├─ ✅ collect_monthly.py [程序3] 月线采集
│ │ └─ 调度：APScheduler - 每月1日16:00
│ │ └─ 路径：D:\cto\scripts\data_collection\collect_monthly.py ✅
│ ├─ ✅ collect_financial.py [程序4] 财务数据采集
│ │ └─ 调度：APScheduler - 每交易日10:00
│ │ └─ 路径：D:\cto\scripts\data_collection\collect_financial.py ✅
│ ├─ ⬜ scheduler_main.py [新增] 主调度程序
│ │ └─ 功能：集成所有APScheduler任务，启动后持续运行
│ │ └─ 路径：D:\cto\scripts\data_collection\scheduler_main.py ✅
│ └─ ⬜ data_utils.py [工具库] 数据处理通用函数
│ └─ 路径：D:\cto\scripts\data_collection\data_utils.py ✅
│
├─ 📂 feature_engineering/ [特征工程]
│ ├─ ⬜ feature_extraction.py [提取134个原始特征]
│ │ └─ 路径：D:\cto\scripts\feature_engineering\feature_extraction.py ✅
│ ├─ ⬜ ai_feature_synthesis.py [合成10个AI特征]
│ │ └─ 路径：D:\cto\scripts\feature_engineering\ai_feature_synthesis.py ✅
│ ├─ ⬜ chip_distribution.py [计算10个筹码特征] ✅
│ │ └─ 路径：D:\cto\scripts\feature_engineering\chip_distribution.py ✅
│ ├─ ⬜ feature_normalization.py [标准化88个特征]
│ │ └─ 路径：D:\cto\scripts\feature_engineering\feature_normalization.py ✅
│ └─ ⬜ feature_engineering_utils.py [工具函数]
│ └─ 路径：D:\cto\scripts\feature_engineering\feature_engineering_utils.py ✅
│
├─ 📂 ml_training/ [机器学习训练]
│ ├─ ⬜ feature_importance.py [计算特征重要性] ✅
│ │ └─ 输出：feature_importance_ranking.csv ✅
│ │ └─ 路径：D:\cto\scripts\ml_training\feature_importance.py ✅
│ ├─ ⬜ model_training.py [训练LR/RF/GB模型]
│ │ └─ 路径：D:\cto\scripts\ml_training\model_training.py ✅
│ ├─ ⬜ model_ensemble.py [集成3个模型]
│ │ └─ 路径：D:\cto\scripts\ml_training\model_ensemble.py ✅
│ ├─ ⬜ model_evaluation.py [模型评估]
│ │ └─ 路径：D:\cto\scripts\ml_training\model_evaluation.py ✅
│ └─ ⬜ ml_utils.py [工具库]
│ └─ 路径：D:\cto\scripts\ml_training\ml_utils.py ✅
│
├─ 📂 similarity_filtering/ [相似度筛选]
│ ├─ ⬜ similarity_filter.py [相似度筛选主程序]
│ │ └─ 集成：筹码分布、消息面、降级逻辑
│ │ └─ 路径：D:\cto\scripts\similarity_filtering\similarity_filter.py ✅
│ ├─ ⬜ filtering_logic.py [50%→40%→30%递进逻辑]
│ │ └─ 路径：D:\cto\scripts\similarity_filtering\filtering_logic.py ✅
│ └─ ⬜ filtering_utils.py [工具函数]
│ └─ 路径：D:\cto\scripts\similarity_filtering\filtering_utils.py ✅
│
├─ 📂 tracking/ [30天跟踪]
│ ├─ ⬜ track_candidates_30d.py [跟踪程序]
│ │ └─ 路径：D:\cto\scripts\tracking\track_candidates_30d.py ✅
│ ├─ ⬜ performance_evaluation.py [效果评估]
│ │ └─ 路径：D:\cto\scripts\tracking\performance_evaluation.py ✅
│ └─ ⬜ tracking_utils.py [工具函数]
│ └─ 路径：D:\cto\scripts\tracking\tracking_utils.py ✅
│
├─ 📂 reporting/ [报告生成]
│ ├─ ⬜ generate_daily_report.py [日报生成]
│ │ └─ 路径：D:\cto\scripts\reporting\generate_daily_report.py ✅
│ ├─ ⬜ generate_weekly_report.py [周报生成]
│ │ └─ 路径：D:\cto\scripts\reporting\generate_weekly_report.py ✅
│ ├─ ⬜ generate_monthly_report.py [月报生成]
│ │ └─ 路径：D:\cto\scripts\reporting\generate_monthly_report.py ✅
│ └─ ⬜ reporting_utils.py [工具函数]
│ └─ 路径：D:\cto\scripts\reporting\reporting_utils.py ✅
│
├─ 📂 utils/ [通用工具]
│ ├─ ⬜ config.py [配置管理]
│ │ └─ 路径：D:\cto\scripts\utils\config.py ✅
│ ├─ ⬜ logger.py [日志管理]
│ │ └─ 路径：D:\cto\scripts\utils\logger.py ✅
│ ├─ ⬜ api_client.py [API客户端]
│ │ └─ 路径：D:\cto\scripts\utils\api_client.py ✅
│ ├─ ⬜ github_trigger.py [GitHub事件触发] ✅
│ │ └─ 功能：检测本地数据完成后，触发GitHub Actions
│ │ └─ 路径：D:\cto\scripts\utils\github_trigger.py ✅
│ └─ ⬜ database.py [数据库操作]
│ └─ 路径：D:\cto\scripts\utils\database.py ✅
│
└─ 📂 tests/ [测试脚本]
├─ ⬜ test_feature_extraction.py
│ └─ 路径：D:\cto\scripts\tests\test_feature_extraction.py ✅
├─ ⬜ test_ml_models.py
│ └─ 路径：D:\cto\scripts\tests\test_ml_models.py ✅
├─ ⬜ test_similarity_filter.py
│ └─ 路径：D:\cto\scripts\tests\test_similarity_filter.py ✅
└─ ⬜ test_integration.py
└─ 路径：D:\cto\scripts\tests\test_integration.py ✅


---

### 📍 第3层：网页应用（D:\cto\dashboard\）⬜ 上传GitHub

D:\cto
│
└─ 📂 dashboard/
│
├─ ⬜ index.html [主Dashboard数据看板]
│ └─ 功能：候选股票列表 + 参数调整 + 概览指标
│ └─ 路径：D:\cto\dashboard\index.html ✅
│
├─ ⬜ monitor.html [GitHub监控页面]
│ └─ 功能：Workflow状态 + API统计 + 功能按钮
│ └─ 路径：D:\cto\dashboard\monitor.html ✅
│
├─ ⬜ guide.html [使用指南页面]
│ └─ 功能：项目计划 + 员工配置 + 框架备份 + 监督报告
│ └─ 路径：D:\cto\dashboard\guide.html ✅
│
├─ 📂 assets/
│ ├─ 📂 css/
│ │ ├─ ⬜ tailwind.min.css [Tailwind CSS库]
│ │ │ └─ 路径：D:\cto\dashboard\assets\css\tailwind.min.css ✅
│ │ ├─ ⬜ dashboard.css [Dashboard样式]
│ │ │ └─ 路径：D:\cto\dashboard\assets\css\dashboard.css ✅
│ │ ├─ ⬜ monitor.css [Monitor页样式]
│ │ │ └─ 路径：D:\cto\dashboard\assets\css\monitor.css ✅
│ │ └─ ⬜ common.css [通用样式]
│ │ └─ 路径：D:\cto\dashboard\assets\css\common.css ✅
│ │
│ ├─ 📂 js/
│ │ ├─ ⬜ i18n.js [多语言（中/英）]
│ │ │ └─ 路径：D:\cto\dashboard\assets\js\i18n.js ✅
│ │ ├─ ⬜ dashboard.js [Dashboard逻辑]
│ │ │ └─ 路径：D:\cto\dashboard\assets\js\dashboard.js ✅
│ │ ├─ ⬜ monitor.js [Monitor逻辑]
│ │ │ └─ 路径：D:\cto\dashboard\assets\js\monitor.js ✅
│ │ ├─ ⬜ auth.js [密码认证] ✅
│ │ │ └─ 功能：无密码查看，密码输入才能修改
│ │ │ └─ 路径：D:\cto\dashboard\assets\js\auth.js ✅
│ │ ├─ ⬜ api_client.js [API客户端]
│ │ │ └─ 路径：D:\cto\dashboard\assets\js\api_client.js ✅
│ │ └─ ⬜ utils.js [工具函数]
│ │ └─ 路径：D:\cto\dashboard\assets\js\utils.js ✅
│ │
│ ├─ 📂 vendor/
│ │ ├─ ⬜ chart.min.js [Chart.js图表库]
│ │ │ └─ 路径：D:\cto\dashboard\assets\vendor\chart.min.js ✅
│ │ └─ ⬜ echarts.min.js [ECharts筹码分布图]
│ │ └─ 路径：D:\cto\dashboard\assets\vendor\echarts.min.js ✅
│ │
│ └─ 📂 data/
│ ├─ ⬜ candidates_data.json [日更新] 候选股票数据
│ │ └─ 路径：D:\cto\dashboard\assets\data\candidates_data.json ✅
│ ├─ ⬜ tracking_data.json [日更新] 跟踪数据
│ │ └─ 路径：D:\cto\dashboard\assets\data\tracking_data.json ✅
│ ├─ ⬜ chip_distribution.json [日更新] 筹码分布数据
│ │ └─ 路径：D:\cto\dashboard\assets\data\chip_distribution.json ✅
│ ├─ ⬜ news_analysis.json [日更新] 消息面分析
│ │ └─ 路径：D:\cto\dashboard\assets\data\news_analysis.json ✅
│ ├─ ⬜ feature_importance.json [日更新] 特征重要性
│ │ └─ 路径：D:\cto\dashboard\assets\data\feature_importance.json ✅
│ ├─ ⬜ api_usage.json [日更新] API使用统计
│ │ └─ 路径：D:\cto\dashboard\assets                     │  └─ 路径：D:\cto\dashboard\assets\data\api_usage.json ✅
   │     └─ ⬜ supervisor_report.json [日更新] 监督员工报告 ✅
   │        └─ 路径：D:\cto\dashboard\assets\data\supervisor_report.json ✅
   │
   └─ ⬜ server.py [简单Flask服务器]
      └─ 路径：D:\cto\dashboard\server.py ✅
📍 第4层：GitHub工作流（D:\cto.github\workflows\）⬜ 上传GitHub
D:\cto\
│
└─ 📂 .github/workflows/
   │
   ├─ ⬜ daily.yml [日分析工作流（自托管Runner）]
   │  └─ 触发：每日09:30 或 手动 workflow_dispatch
   │  └─ 路径：D:\cto\.github\workflows\daily.yml ✅
   │
   ├─ ⬜ weekly.yml [周报告工作流]
   │  └─ 触发：每周一 或 手动
   │  └─ 路径：D:\cto\.github\workflows\weekly.yml ✅
   │
   ├─ ⬜ monthly.yml [月报告工作流]
   │  └─ 触发：每月1日 或 手动
   │  └─ 路径：D:\cto\.github\workflows\monthly.yml ✅
   │
   ├─ ⬜ trigger.yml [触发机制工作流] ✅
   │  └─ 功能：检测本地数据完成，自动启动daily.yml
   │  └─ 由github_trigger.py调用
   │  └─ 路径：D:\cto\.github\workflows\trigger.yml ✅
   │
   └─ ⬜ deploy.yml [部署网页工作流]
      └─ 触发：每天 或 手动
      └─ 路径：D:\cto\.github\workflows\deploy.yml ✅
📍 第5层：文档与报告（D:\cto\projects\山脚下\）⬜ 上传GitHub
D:\cto\
│
└─ 📂 projects/山脚下/
   │
   ├─ ⬜ 项目计划.md [完整计划书]
   │  └─ 路径：D:\cto\projects\山脚下\项目计划.md ✅
   │
   ├─ ⬜ 进度跟踪.md [实时进度更新]
   │  └─ 路径：D:\cto\projects\山脚下\进度跟踪.md ✅
   │
   ├─ ⬜ 新聊天快速恢复.md [快速恢复清单]
   │  └─ 路径：D:\cto\projects\山脚下\新聊天快速恢复.md ✅
   │
   ├─ 📂 日报/
   │  └─ ⬜ daily_2025-12-15.md [每日生成]
   │     └─ 路径：D:\cto\projects\山脚下\日报\daily_*.md ✅
   │
   ├─ 📂 周报/
   │  └─ ⬜ weekly_2025-W50.md [每周生成]
   │     └─ 路径：D:\cto\projects\山脚下\周报\weekly_*.md ✅
   │
   ├─ 📂 月报/
   │  └─ ⬜ monthly_2025-12.csv [每月生成]
   │     └─ 路径：D:\cto\projects\山脚下\月报\monthly_*.csv ✅
   │
   ├─ 📂 框架备份/
   │  ├─ ✅ framework_backup_v1.0.zip [初始化完成] ✅
   │  ├─ ⬜ framework_backup_v1.1.zip [阶段1完成]
   │  ├─ ⬜ framework_backup_v1.2.zip [阶段2完成]
   │  ├─ ⬜ framework_backup_v1.3.zip [阶段3完成]
   │  ├─ ⬜ framework_backup_v1.4.zip [最终完成]
   │  ├─ ⬜ framework_backup_current.zip [最新备份]
   │  └─ ⬜ README.md [备份说明]
   │     └─ 路径：D:\cto\projects\山脚下\框架备份\ ✅
   │
   ├─ 📂 员工配置/
   │  └─ ⬜ staff_config.md [员工信息和权限]
   │     └─ 路径：D:\cto\projects\山脚下\员工配置\staff_config.md ✅
   │
   ├─ 📂 使用手册/
   │  ├─ ⬜ dashboard_guide.md [Dashboard使用指南]
   │  │  └─ 路径：D:\cto\projects\山脚下\使用手册\dashboard_guide.md ✅
   │  ├─ ⬜ monitor_guide.md [Monitor使用指南]
   │  │  └─ 路径：D:\cto\projects\山脚下\使用手册\monitor_guide.md ✅
   │  └─ ⬜ parameter_guide.md [参数调整指南]
   │     └─ 路径：D:\cto\projects\山脚下\使用手册\parameter_guide.md ✅
   │
   └─ 📂 API调用策略/
      └─ ⬜ api_strategy.md [API限制和优化策略]
         └─ 路径：D:\cto\projects\山脚下\API调用策略\api_strategy.md ✅
📍 第6层：日志与配置（D:\cto\logs\ + 根目录）⬜ 上传GitHub
D:\cto\
│
├─ 📂 logs/
│  ├─ 📂 api_usage/
│  │  └─ ⬜ api_usage_*.json [API使用统计]
│  │     └─ 路径：D:\cto\logs\api_usage\api_usage_*.json ✅
│  │
│  └─ 📂 analysis/
│     └─ ⬜ analysis_*.log [分析日志]
│        └─ 路径：D:\cto\logs\analysis\analysis_*.log ✅
│
├─ ⬜ requirements.txt [Python依赖清单]
│  └─ 路径：D:\cto\requirements.txt ✅
│
├─ ⬜ .gitignore [Git忽略规则]
│  └─ 路径：D:\cto\.gitignore ✅
│
├─ ⬜ README.md [项目说明]
│  └─ 路径：D:\cto\README.md ✅
│
└─ ⬜ config.json [全局配置文件]
   └─ 路径：D:\cto\config.json ✅
📡 数据架构
数据流向完整说明
┌─────────────────────────────────────────────┐
│ 每个交易日 09:00                            │
├─────────────────────────────────────────────┤
│ Windows 任务计划 或 Python APScheduler      │
│ ↓                                           │
│ 运行：collect_daily_minute.py               │
│ 输出：D:\cto\data\daily_minute_data\       │
│      daily_data.csv                        │
│                                             │
│ 运行：collect_financial.py（按需）         │
│ 输出：D:\cto\data\financial_data\          │
│      financial_data.csv                    │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ 本地 collect_daily_minute.py 完成后        │
├─────────────────────────────────────────────┤
│ 调用：github_trigger.py                     │
│ ↓                                           │
│ 触发 GitHub Actions：trigger.yml            │
│ ↓                                           │
│ 自动启动：daily.yml                        │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ GitHub Actions 工作流（自托管Runner）       │
├─────────────────────────────────────────────┤
│ ✅ 从本地读取数据（Self-hosted Runner）    │
│   - daily_data.csv                         │
│   - weekly_data.csv                        │
│   - monthly_data.csv                       │
│   - financial_data.csv                     │
│                                             │
│ ✅ 运行分析脚本                             │
│   - identify_success_samples.py            │
│   - feature_extraction.py                  │
│   - ai_feature_synthesis.py                │
│   - chip_distribution.py ✅                │
│   - feature_importance.py ✅               │
│   - model_training.py                      │
│   - model_ensemble.py                      │
│   - similarity_filter.py                   │
│   - generate_daily_report.py               │
│   - generate_supervisory_report.py ✅      │
│                                             │
│ ✅ 生成结果（GitHub 仓库内）               │
│   - success_samples.csv                    │
│   - all_features_88.csv                    │
│   - feature_importance_ranking.csv ✅      │
│   - chip_features.csv                      │
│   - chip_analysis_report.json              │
│   - model_ensemble.pkl                     │
│   - candidates_50pct.csv                   │
│   - selection_candidates.csv               │
│   - daily_news_analysis.json               │
│   - supervisor_report.json ✅              │
│   - daily_2025-12-15.md                    │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ 数据汇总 & Dashboard 更新                   │
├─────────────────────────────────────────────┤
│ 自动读取 GitHub 数据                        │
│ ↓                                           │
│ 转换为 JSON：                               │
│ dashboard/assets/data/                     │
│ ├─ candidates_data.json                    │
│ ├─ tracking_data.json                      │
│ ├─ chip_distribution.json                  │
│ ├─ news_analysis.json                      │
│ ├─ feature_importance.json                 │
│ └─ supervisor_report.json ✅               │
│                                             │
│ ↓                                           │
│ 网页实时显示给用户                         │
│ - Dashboard：候选股票 + 参数调整             │
│ - Monitor：工作流状态 + 功能按钮             │
│ - Guide：项目计划 + 监督报告 ✅            │
└─────────────────────────────────────────────┘
自托管Runner配置说明
为什么需要自托管Runner？

GitHub公有Runner无法访问你的本地数据
自托管Runner安装在本地Windows机器上
可以直接读取D:\cto\data\ 目录
配置步骤：

在GitHub仓库Settings → Actions → Runners
添加新的自托管Runner
在本地运行Runner配置脚本
Runner会持续监听GitHub Actions事件
触发时自动在本地运行工作流
🎯 88个特征体系
特征总体统计
| 数据源 | 个数 | 类型 | 备注 |
|--------|------|------|------|
| 日线数据（日频） | 18个 | 原始特征 | ⭐⭐⭐⭐⭐ 最重要 |
| 分钟线数据 | 30个 | 原始特征 | 短期波动分析 |
| 周线数据 | 11个 | 原始特征 | 中期趋势 |
| 月线数据 | 11个 | 原始特征 | 长期趋势 |
| 财务数据 | 64个 | 原始特征 | 基本面分析 |
| 原始特征小计 | 134个 | | |
| AI合成特征 | 10个 | 高级特征 | ⭐⭐⭐⭐⭐ 最最重要 |
| 筹码分布特征 | 10个 | 高级特征 | ⭐⭐⭐⭐ 权重0.2 |
| 去重后最终 | 88个 | | 去除相关性强的特征 |

AI合成的10个高级特征（最最
重要）

| # | 特征名 | 类型 | 优先级 | 权重 | 说明 |
|---|--------|------|--------|------|------|
| 1 | 潜伏期资金流入综合指标 | 资金面 | 🔴最高 | 1.5 | 多维度资金流向合成 |
| 2 | 技术形态突破概率评分 | 技术面 | 🔴最高 | 1.5 | 基于历史模式，0-100分 |
| 3 | 市场情绪转折点检测 | 情绪面 | 🔴最高 | 1.5 | 情绪极值量化 |
| 4 | 风险收益比综合评估 | 风险控制 | 🔴最高 | 1.5 | 拉升前风险释放程度 |
| 5 | 历史相似度匹配系数 | 策略核心 | 🔴最高 | 1.5 | 与成功案例特征相似度 |
| 6 | 多时间周期共振指标 | 技术面 | 🟠次高 | 1.2 | 日/周/月信号协同强度 |
| 7 | 量价关系健康度评分 | 技术面 | 🟠次高 | 1.2 | 成交量与价格匹配，0-100分 |
| 8 | 资金流向持续性指标 | 资金面 | 🟠次高 | 1.2 | 主力资金持续流入能力 |
| 9 | 板块轮动先行指标 | 情绪面 | 🟠次高 | 1.2 | 提前识别热点切换 |
| 10 | 市场情绪温度计 | 情绪面 | 🟠次高 | 1.2 | 整体市场情绪量化 |

筹码分布的10个特征（权重0.2）
| # | 特征名 | 计算方法 | 范围 | 说明 |
|---|--------|---------|------|------|
| 1 | 筹码集中度 | Herfindahl指数 | 0-1 | 越高越集中 |
| 2 | 锁定率 | 套牢盘占比 | 0-100% | 套牢程度 |
| 3 | 成本均线 | 所有筹码平均成本 | 价格 | 持仓成本 |
| 4 | 获利盘占比 | 获利者比例 | 0-100% | 盈利程度 |
| 5 | 最大筹码堆积价位 | 最大筹码密集区 | 价格 | 关键价位 |
| 6 | 筹码密集区宽度 | 密集区价格范围 | % | 宽度越小越集中 |
| 7 | 历史套牢比例 | 历史最高价套牢 | 0-100% | 历史高点套牢 |
| 8 | 资金成本差 | 最高价-成本均线 | % | 盈利空间 |
| 9 | 筹码突破强度 | 价格突破筹码顶部幅度 | % | 突破力度 |
| 10 | 筹码转换速度 | 成交量变化速度 | 倍数 | 换手速度 |

特征在相似度筛选中的权重分配
最终相似度评分 = 0.6 * ML模型预测 + 0.2 * 筹码分布评分 + 0.2 * 消息面评分

ML模型预测 = 集成(逻辑回归 + 随机森林 + 梯度提升)
筹码分布评分 = 10个筹码特征的加权平均
消息面评分 = 消息面分析员工手动评估 + 自动权重调整
可调参数（在网页可修改）：

{
  "weights": {
    "ml_model": 0.6,           // 可调 0.3-0.8
    "chip_distribution": 0.2,  // 可调 0.1-0.4
    "news_sentiment": 0.2      // 可调 0.1-0.4
  },
  "chip_thresholds": {
    "concentration_min": 0.3,  // 最小筹码集中度
    "lock_rate_max": 0.8,      // 最大锁定率
    "breakout_strength_min": 0.15  // 最小突破强
度
}
}


---

## 💰 筹码分布详解

### 筹码分布的3个输出文件

1. **chip_features.csv** - 10个筹码指标
   ```csv
   code,date,chip_concentration,lock_rate,cost_price,profit_ratio,loss_ratio,max_chip_price,density_width,historical_loss_ratio,fund_cost_diff,breakout_strength,turnover_speed,chip_score
更新频率：每日
用途：输入ML模型训练
cost_distribution.csv - 分价位筹码分布

code,date,price_level,chip_volume,chip_ratio,cost_concentration
详细的分价位筹码分布
用途：绘制筹码分布图表（ECharts）
chip_analysis_report.json - 筹码分析报告

{
  "date": "2025-12-15",
  "summary": "今日市场筹码整体偏弱，集中度下降",
  "top_stocks_with_good_chips": [
    {
      "code": "000001",
      "name": "平安银行",
      "chip_score": 85,
      "concentration": 0.72,
      "lock_rate": 0.45,
      "breakout_potential": "high"
    }
  ],
  "market_overview": {
    "avg_concentration": 0.58,
    "total_locked_ratio": 0.62,
    "bullish_count": 1250,
    "bearish_count": 3200
  }
}
筹码分布在Dashboard中如何展示
概览板块：显示市场整体筹码集中度
候选股票列表：每只股票显示筹码评分（0-100分）
详细分析：点击某只股票查看其筹码分布图（ECharts）
参数调整：
筹码权重滑块（0-1.0）
筹码集中度阈值滑块（0-1.0）
[应用]按钮
🤖 机器学习方案
3模型集成方案
模型选择：

逻辑回归 (Logistic Regression) - 基础线性模型
随机森林 (Random Forest) - 非线性特征交互
梯度提升 (XGBoost/LightGBM) - 最优非线性拟合
训练流程：

输入：88个特征 + 成功样本标签（正样本）+ 随机采样的失败样本（负样本）
↓
特征标准化（StandardScaler）
↓
训练三个模型（参数优化）
↓
交叉验证（5折）
↓
集成方案：投票或加权平均
↓
输出：model_ensemble.pkl + model_metrics.json
集成方案细节：

ensemble_score = 0.4 * lr_pred + 0.3 * rf_pred + 0.3 * gb_pred
训练数据准备：

正样本：历史上"山脚下"形态的股票（过去的成功案例）
负样本：随机采样的非山脚下形态股票（1:3或1:5的比例）
模型评估指标：

Precision（精准率）：预测为正的中有多少真的是正样本
Recall（召回率）：实际正样本中有多少被正确预测
F1 Score：精准率和召回率的调和平均
AUC-ROC：模型区分能力
模型输出
model_metrics.json：

{
  "date": "2025-12-15",
  "train_samples": 5000,
  "test_samples": 1000,
  "lr_metrics": {
    "accuracy": 0.82,
    "precision": 0.75,
    "recall": 0.68,
    "f1": 0.71,
    "auc_roc": 0.81
  },
  "rf_metrics": {
    "accuracy": 0.85,
    "precision": 0.78,
    "recall": 0.72,
    "f1": 0.75,
    "auc_roc": 0.84
  },
  "gb_metrics": {
    "accuracy": 0.87,
    "precision": 0.81,
    "recall": 0.74,
    "f1": 0.77,
    "auc_roc": 0.86
  },
  "ensemble_metrics": {
    "accuracy": 0.88,
    "precision": 0.82,
    "recall": 0.75,
    "f1": 0.78,
    "auc_roc": 0.87
  }
}
🔗 GitHub触发机制
事件驱动架构说明
核心理念：程序间协调，不能自主决定启动时间

触发链路：

步骤1：本地 collect_daily_minute.py 完成
   ↓ 写入flag：D:\cto\data\.sync_flag
   ↓
步骤2：github_trigger.py 监听该flag
   ↓ 检测到flag后
   ↓
步骤3：调用GitHub API触发 trigger.yml
   ↓ 发送HTTP POST请求
   ↓
步骤4：trigger.yml 工作流启动
   ↓ 验证本地数据完整性
   ↓
步骤5：自动触发 daily.yml
   ↓ 在自托管Runner上运行
   ↓
步骤6：daily.yml 执行所有分析脚本
   ↓ 生成结果，上传GitHub
   ↓
步骤7：Dashboard 自动读取最新结果
github_trigger.py 实现要点
职责：

监听本地数据文件变化（D:\cto\data\）
检测成功标志（daily_data.csv 最新时间戳）
验证数据完整性（行数、列数）
调用GitHub REST API或Webhook
传递参数给workflow（如分析日期、参数等）
伪代码：

def github_trigger():
    while True:
        if check_sync_flag():  # 本地数据完成
            if validate_data_integrity():  # 验证数据完整
                trigger_github_action(
                    workflow="trigger.yml",
                    params={
                        "analysis_date": today(),
                        "data_version": get_data_hash()
                    }
                )
                clear_sync_flag()
        time.sleep(60)  # 每60秒检查一次
trigger.yml 工作流
职责：

接收本地触发
验证参数
检查自托管Runner健康状态
启动daily.yml
配置示例：

name: Trigger Daily Workflow

on:
  workflow_dispatch:
    inputs:
      analysis_date:
        required: true
      data_version:
        required: true

jobs:
  validate_and_trigger:
    runs-on: ubuntu-latest
    steps:
      - name: Validate Data
        run: |
          echo "验证本地数据完整性..."
          # 验证逻辑
      
      - name: Trigger Daily Workflow
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.actions.createWorkflowDispatch({
              owner: context.repo.owner,
              repo: context.repo.repo,
              workflow_id: 'daily.yml',
              ref: 'main',
              inputs: {
                analysis_date: '${{ github.event.inputs.analysis_date }}'
              }
            })
🌐 网页功能详解
网页1：Dashboard数据看板（index.html）
三大功能板块：

板块1：概览 (Overview)
┌─────────────────────────────────────┐
│ 山脚下 - 投资决策看板               │
├─────────────────────────────────────┤
│ [中文] [English] 密码: [输入] [登录] │
├─────────────────────────────────────┤
│ 📊 概览指标                          │
│ ├─ 候选股票总数：1,250只             │
│ ├─ 近30天平均涨幅：15.3%            │
│ ├─ 成功率（涨幅>0%）：72.5%         │
│ ├─ 市场筹码集中度：0.58              │
│ └─ 最近更新时间：2025-12-15 15:30  │
└─────────────────────────────────────┘
板块2：候选股票列表 (Candidates)
┌──────────────────────────────────────────────────────┐
│ 搜索: ___________  排序: [相似度↓] 筛选: [行业] [地域] │
├─────┬──────┬────────┬────────┬────────┬───────────┤
│代码  │名称  │相似度  │筹码评分│消息评分│30天涨幅   │
├─────┼──────┼────────┼────────┼────────┼───────────┤
│000001│平安银│ 85%   │ 78分  │ 72分  │ +18.5%   │
│600000│浦发银│ 78%   │ 72分  │ 65分  │ +12.3%   │
│000858│五粮液│ 72%   │ 81分  │ 88分  │ +25.6%   │
└─────┴──────┴────────┴────────┴────────┴───────────
│
│ [上一页] 第1-20条，共1,250条 [下一页]     │
└──────────────────────────────────────────────────────┘
板块3：参数调整面板（需要密码）✅
┌──────────────────────────────────────────────────────┐
│ 🔧 参数调整（需要密码）                              │
├──────────────────────────────────────────────────────┤
│
│ 基础参数：
│ ├─ 时间窗口：[15天] [20天] [30天] [45天] 或 输入框
│ ├─ 成功样本涨幅：[30%] [40%] [50%] [60%] 或 输入框
│ ├─ 追溯交易日数：30天 (固定)
│ └─ 跟踪周期：[30天] [60天] [90天]
│
│ 相似度阈值：
│ ├─ 初始阈值：[0.7 ═════●═════ 0.95]
│ ├─ 降级阈值1：[0.5 ═════●═════ 0.70]
│ ├─ 降级阈值2：[0.3 ═════●═════ 0.50]
│ └─ 说明：如无50%的候选，自动降级至40%、30%
│
│ 权重调整：
│ ├─ ML模型权重：[0.3 ════●════ 0.8]  (默认0.6)
│ ├─ 筹码分布权重：[0.1 ════●════ 0.4]  (默认0.2)
│ ├─ 消息面权重：[0.1 ════●════ 0.4]  (默认0.2)
│ └─ 权重总和必须=1.0（自动调整）
│
│ 筹码分布参数：
│ ├─ 最小筹码集中度：[0.2 ════●════ 0.8]  (默认0.3)
│ ├─ 最大锁定率：[0.5 ════●════ 1.0]  (默认0.8)
│ └─ 最小突破强度：[0.05 ═════●═════ 0.3]  (默认0.15)
│
│ 行业与地域筛选：
│ ├─ ☐ 医药生物  ☐ 电子  ☐ 机械设备  ☐ 化工
│ ├─ ☐ 食品饮料  ☐ 房地产  ☐ 消费服务  ☐ 其他
│ └─ 地域：[全国] [北京] [深圳] [上海]
│
│ 消息面权重调整（仅供参考，由消息面员工主要负责）：
│ ├─ 医药行业权重：[0.5 ════●════ 1.5]  (默认1.0)
│ ├─ 科技行业权重：[0.5 ════●════ 1.5]  (默认1.0)
│ ├─ 金融行业权重：[0.5 ════●════ 1.5]  (默认1.0)
│ └─ ... 其他行业
│
│ [应用修改] [重置默认] [保存为预设]
│
└──────────────────────────────────────────────────────┘
板块4：特征重要性排名 ✅
┌──────────────────────────────────────────────────────┐
│ 📊 特征重要性排名                                    │
├──────────────────────────────────────────────────────┤
│
│ 前20个关键特征（ML模型权重）：
│
│ # │ 特征名                    │ 重要性 │ 类型    │ 权重
│───┼──────────────────────────┼────────┼────────┼─────
│ 1 │ 历史相似度匹配系数        │ ████░  │ AI合成 │ 1.5
│ 2 │ 技术形态突破概率评分      │ ███░░  │ AI合成 │ 1.5
│ 3 │ 潜伏期资金流入综合指标    │ ███░░  │ AI合成 │ 1.5
│ 4 │ 成交量放大倍数            │ ███░░  │ 技术   │ 1.2
│ 5 │ 价格波动率变化            │ ██░░░  │ 技术   │ 1.2
│ 6 │ RSI位置                   │ ██░░░  │ 技术   │ 1.0
│ 7 │ MACD金叉强度              │ ██░░░  │ 技术   │ 1.0
│ 8 │ 大单净流入率              │ ██░░░  │ 资金   │ 1.0
│ 9 │ 筹码集中度                │ ██░░░  │ 筹码   │ 0.8
│10 │ 换手率变化率              │ ██░░░  │ 资金   │ 0.8
│ ⋮  │ ⋮                        │ ⋮     │ ⋮     │ ⋮
│20 │ 净利润增长率              │ █░░░░  │ 财务   │ 0.3
│
│ [查看完整排名] [导出为Excel]
│
└──────────────────────────────────────────────────────┘
板块5：对比分析 (Historical Performance)
┌──────────────────────────────────────────────────────┐
│ 📈 参数对比分析                                      │
├──────────────────────────────────────────────────────┤
│
│ 历史参数效果对比：
│
│ 参数配置           │ 候选数 │ 平均涨幅 │ 成功率  │ 日期
│─────────────────────┼────────┼────────┼────────┼──────
│ 默认(50%↓40%↓30%)   │ 1,250 │ 15.3%  │ 72.5%  │今天
│ 上周参数(50%↓40%)   │ 850   │ 18.2%  │ 75.2%  │12-08
│ 上月参数(固定50%)   │ 450   │ 21.5%  │ 81.3%  │11-15
│ 严格筹码(集中度>0.7)│ 280   │ 24.8%  │ 85.6%  │11-10
│
│ [对比图表] [回测分析] [导出数据]
│
└──────────────────────────────────────────────────────┘
网页2：GitHub工作进度监控（monitor.html）⭐
实时显示内容
板块1：工作流状态 (Workflow Runs)

┌──────────────────────────────────────────────────────┐
│ 🔄 最近5个工作流执行                                │
├──────────────────────────────────────────────────────┤
│
│ 日期     │ 工作流      │ 状态   │ 执行时间 │ 操作
│──────────┼─────────────┼────────┼────────┼──────
│ 今天     │ daily.yml   │ ✅成功 │ 12分   │ 查看日志
│ 昨天     │ daily.yml   │ ✅成功 │ 15分   │ 查看日志
│ 12-13    │ weekly.yml  │ ✅成功 │ 45分   │ 查看日志
│ 12-12    │ daily.yml   │ ❌失败 │ 8分    │ 查看日志
│ 12-11    │ trigger.yml │ ⏳运行中│ 2分   │ 取消
│
│ 详细日志：[standard output] [error logs] [API usage]
│
└──────────────────────────────────────────────────────┘
板块2：当前任务列表 (Current Tasks)

┌──────────────────────────────────────────────────────┐
│ 📋 当前任务                                          │
├──────────────────────────────────────────────────────┤
│
│ 开放的Pull Requests：3条
│ ├─ [PR#125] 特征重要性排名计算 (审核中) 预计2天
│ ├─ [PR#124] 筹码分布集成 (编写中) 预计1天
│ └─ [PR#123] Dashboard双语支持 (已合并) 已完成
│
│ 开放的任务：5条
│ ├─ [Task#1] 实现trigger.yml (进行中 60%) 预计1天
│ ├─ [Task#2] 集成监督报告 (待开始) 预计2天
│ ├─ [Task#3] 优化ML模型 (待开始) 预计3天
│ └─ ...
│
│ [查看全部] [新建任务]
│
└──────────────────────────────────────────────────────┘
板块3：API使用统计 (API Usage)

┌──────────────────────────────────────────────────────┐
│ 📊 API调用统计                                       │
├──────────────────────────────────────────────────────┤
│
│ 今日API调用数：15,234次
│ 昨日API调用数：18,456次
│ 本周总计：125,680次
│ 月度配额：100,000次
│ 剩余配额：-25,680次 ⚠️ 已超
│
│ 按接口统计：
│ ├─ 行情数据查询：8,200次 (54%)
│ ├─ 财务数据查询：4,100次 (27%)
│ ├─ 基本信息查询：2,100次 (14%)
│ └─ 其他：834次 (5%)
│
│ [详细报告] [趋势图] [导出日志]
│
│ 📈 过去7天API调用趋势图（柱状图）
│ 
└──────────────────────────────────────────────────────┘
板块4：团队活动 (Team Activity)

┌──────────────────────────────────────────────────────┐
│ 👥 团队活动                                          │
├──────────────────────────────────────────────────────┤
│
│ 最近提交（Git Commits）：
│ ├─ [15:30] 修复特征提取bug - AI Agent
│ ├─ [14:20] 更新参数权重配置 - 项目经理
│ └─ [12:45] 集成消息面分析数据 - AI Agent
│
│ 员工状态：
│ ├─ 项目经理 🟢 在线 - 最后活动：5分钟前
│ ├─ AI Agent 🟢 在线 - 运行中：Daily workflow
│ ├─ 消息面分析员工 🟡 离线 - 最后活动：1小时前
│ └─ 监督员工 🟢 在线 - 最后活动：2分钟前
│
│ [刷新] [详细信息]
│
└──────────────────────────────────────────────────────┘
功能按钮（需要密码）✅
┌──────────────────────────────────────────────────────┐
│ 🎮 操作按钮（需要密码才能执行）                     │
├──────────────────────────────────────────────────────┤
│
│ [手动触发 Daily] / [Trigger Daily Manually]
│   └─ 立即执行 daily.yml 工作流
│
│ [手动触发 Weekly] / [Trigger Weekly Manually]
│   └─ 立即执行 weekly.yml 工作流
│
│ [手动触发 Monthly] / [Trigger Monthly Manually]
│   └─ 立即执行 monthly.yml 工作流
│
│ [查看日志] / [View Logs]
│   └─ 跳转到GitHub Actions详细日志
│
│ [刷新数据] / [Refresh Data]
│   └─ 立即更新页面数据（从GitHub API）
│
│ [重新运行失败的Job] / [Retry Failed Job]
│   └─ 如果有失败的工作流，可点击重新运行
│
│ [设置参数] / [Go to Parameters]
│   └─ 跳转到 Dashboard 参数调整面板
│
│ [查看报告] / [View Reports]
│   └─ 查看日报、周报、月报
│
└──────────────────────────────────────────────────────┘
网页3：使用指南与监督报告（guide.html）⭐
页面导航结构
左侧导航栏：
├─ 📘 项目计划
├─ 📊 完整树状结构
├─ 🎯 核心改动说明
├─ 🧬 88个特征体系
├─ 💰 筹码分布详解
├─ 🤖 机器学习方案
├─ 🔗 GitHub触发机制
├─ 🌐 网页功能详解
├─ 👥 员工配置
├─ 📋 使用手册
│   ├─ Dashboard使用指南
│   ├─ Monitor使用指南
│   └─ 参数调整指南
├─ 📈 API调用策略
├─ 🔄 框架备份清单
└─ 📢 监督报告 ⭐ 新增

右侧内容区：
├─ 对应左侧导航的详细内容
├─ 搜索功能（Ctrl+F搜索）
└─ 打印/导出功能
监督报告板块（新增）⭐
监督员工职责：

监控项目进度
监督工作流程
检测问题和异常
向项目经理报告
┌──────────────────────────────────────────────────────┐
│ 📢 监督报告（中文）                                 │
├──────────────────────────────────────────────────────┤
│
│ 报告日期：2025-12-15 16:00
│ 监督员工：系统监督员
│ 报告类型：日报 | 周报 | 月报
│
│ ✅ 正常项目状态
│ ├─ 数据采集：✅ 正常（今日4个程序均已完成）
│ ├─ GitHub工作流：✅ 正常（今日2个工作流成功执行）
│ ├─ Dashboard更新：✅ 正常（页面数据已同步）
│ ├─ API调用：✅ 正常（日调用数15,234次，在限额内）
│ ├─ 候选股票生成：✅ 正常（生成1,250只候选）
│ └─ 跟踪数据更新：✅ 正常（30天跟踪数据已更新）
│
│ ⚠️ 需要关注的问题
│ ├─ 【消息面】消息面分析员工未及时提交分析
│    └─ 预期提交时间：15:30，实际提交时间：未提交
│    └─ 影响：news_analysis.json 为前一天数据
│    └─ 建议：立即联系消息面员工，确认数据来源
│
│ ├─ 【特征】特征importance排名计算耗时过长
│    └─ 预期耗时：5分钟，实际耗时：12分钟
│    └─ 原因分析：88个特征，样本数较多
│    └─ 建议：考虑优化特征选择或加快计算

│
│ ❌ 严重问题
│ 【无】本日未发生严重问题
│
│ 📊 数据质量检查
│ ├─ daily_data.csv：✅ 完整（5,664只股票，18个字段）
│ ├─ features_88.csv：✅ 完整（4,200只股票，88个字段）
│ ├─ candidates.csv：✅ 完整（1,250只候选）
│ ├─ chip_features.csv：✅ 完整（1,250只股票，10个筹码特征）
│ ├─ selection_metadata.json：✅ 完整
│ └─ supervisor_report.json：✅ 已生成
│
│ 📈 关键指标
│ ├─ 今日候选数：1,250只（50%阈值）
│ ├─ 成功率（30天涨幅>0%）：72.5%
│ ├─ 平均涨幅：+15.3%
│ ├─ 最高涨幅：+68.2%
│ └─ 最低涨幅：-12.5%
│
│ 🔍 员工工作日志
│ ├─ AI Agent：✅ 已完成所有分析脚本运行
│ ├─ 消息面分析员工：⚠️ 数据未及时提交
│ ├─ 监督员工：✅ 已完成日常监督
│ └─ 项目经理：📝 参数调整：筹码权重由0.2→0.25
│
│ 📅 明日预告
│ ├─ 定期检查消息面分析数据提交情况
│ ├─ 继续监控API调用是否超限
│ ├─ 验证跟踪数据的准确性
│
│ [生成完整报告] [导出为PDF] [发送通知]
│
└──────────────────────────────────────────────────────┘
监督报告数据结构（JSON）：

{
  "date": "2025-12-15",
  "time": "2025-12-15T16:00:00Z",
  "report_type": "daily",
  "supervisor": "系统监督员",
  
  "status_summary": {
    "overall": "正常",
    "data_collection": "✅正常",
    "workflow_execution": "✅正常",
    "dashboard_update": "✅正常",
    "api_usage": "✅正常"
  },
  
  "issues": [
    {
      "level": "warning",
      "category": "消息面",
      "title": "消息面分析员工未及时提交分析",
      "description": "预期提交时间15:30，实际未提交",
      "impact": "news_analysis.json为前一天数据",
      "action": "联系消息面员工确认"
    },
    {
      "level": "warning",
      "category": "特征",
      "title": "特征importance排名计算耗时过长",
      "description": "预期5分钟，实际12分钟",
      "impact": "整体workflow耗时增加",
      "action": "优化特征选择或计算效率"
    }
  ],
  
  "data_quality": {
    "daily_data_csv": { "status": "✅完整", "rows": 5664, "columns": 18 },
    "features_88_csv": { "status": "✅完整", "rows": 4200, "columns": 88 },
    "candidates_csv": { "status": "✅完整", "rows": 1250, "columns": 15 },
    "chip_features_csv": { "status": "✅完整", "rows": 1250, "columns": 10 }
  },
  
  "staff_logs": {
    "ai_agent": { "status": "✅已完成", "tasks": "所有分析脚本" },
    "news_analyst": { "status": "⚠️未完成", "tasks": "消息面分析" },
    "supervisor": { "status": "✅已完成", "tasks": "日常监督" },
    "project_manager": { "status": "📝已操作", "tasks": "参数调整" }
  },
  
  "key_metrics": {
    "candidates_count": 1250,
    "success_rate": 0.725,
    "avg_gain": 0.153,
    "max_gain": 0.682,
    "min_gain": -0.125
  }
}
语言支持详解
所有按钮的中英文标签：

| 按钮功能 | 中文 | English |
|---------|------|---------|
| 时间窗口 | 时间窗口 | Time Window |
| 相似度阈值 | 相似度阈值 | Similarity Threshold |
| 应用修改 | 应用修改 | Apply Changes |
| 重置默认 | 重置默认 | Reset to Default |
| 手动触发Daily | 手动触发 Daily | Trigger Daily Manually |
| 查看日志 | 查看日志 | View Logs |
| 刷新数据 | 刷新数据 | Refresh Data |
| 设置参数 | 设置参数 | Set Parameters |
| 查看报告 | 查看报告 | View Reports |
| 导出数据 | 导出数据 | Export Data |
| 生成完整报告 | 生成完整报告 | Generate Full Report |
| 发送通知 | 发送通知 | Send Notification |

i18n.js 集成：

window.I18n = {
  t(key, replacements = {}) {
    // key 格式：'nav.dashboard', 'button.apply', 'message.success'
    // 返回对应语言的翻译
  },
  setLanguage(lang) {
    // 设置语言：'zh' 或 'en'
    // 触发 'languageChanged' 事件
    // 自动保存到localStorage
  }
}
密码保护机制详解 ✅
auth.js 实现：

行为分层：
│
├─ 无密码状态
│  └─ 只读操作
│     ├─ 查看候选股票列表
│     ├─ 查看工作流状态
│     ├─ 查看报告
│     └─ 查看参数（不能修改）
│
├─ 输入密码后
│  └─ 可写操作
│     ├─ 修改参数并保存
│     ├─ 手动触发工作流
│     ├─ 重新运行失败Job
│     ├─ 调整权重
│     └─ 导出数据
│
└─ 密码存储
   ├─ 前端：localStorage (简单方案)
   │  └─ 风险：明文存储，可被查看
   │
   └─ 后端：server.py + Flask (安全方案)
      └─ 优点：密码加密，更安全
简单实现（前端localStorage）：

function authenticate(password) {
  const correctPassword = 'your_password_here';  // 应在后端设置
  if (password === correctPassword) {
    localStorage.setItem('auth_token', true);
    localStorage.setItem('auth_time', Date.now());
    showWritableElements();
    return true;
  }
  return false;
}
安全实现（后端server.py）：

from flask import Flask, request, session
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/api/login', methods=['POST'])
def login():
    password = request.json.get('password')
    hashed = hashlib.sha256(password.encode()).hexdigest()
    
    if hashed == stored_password_hash:  # 与存储的hash比对
        session['authenticated'] = True
        return {'status': 'success'}
    return {'status': 'failed'}, 401
👥 员工配置
4个职位明细
1️⃣ 项目经理（用户本人）
职责：

项目决策和规划
参数调整和优化
进度跟踪和确认
风险评估和管理
与监督员工沟通
权限：

✅ 所有权限（GitHub、Dashboard、参数修改）
✅ 密码：拥有完全权限
✅ 无需approval
工时：按需

工作内容示例：

早上（09:00）：
  ├─ 检查前一天的分析结果
  ├─ 查看监督报告，了解问题
  ├─ 根据市场情况调整参数

中午（12:00）：
  ├─ 查看实时候选股票
  ├─ 评估入场机会

下午（15:00）：
  ├─ 查看跟踪效果
  ├─ 调整参数权重
  └─ 必要时手动触发分析
Dashboard权限：

查看：✅ 所有数据
修改：✅ 所有参数
执行：✅ 所有操作
2️⃣ AI Agent（cto.new代码开发）
职责：

脚本开发和维护
Bug修复和优化
自动化工作流配置
性能优化
依赖管理
权限：

✅ 代码修改和提交
✅ PR创建和合并
✅ 工作流配置
❌ 参数修改（仅项目经理）
❌ 密码访问Dashboard（仅查看）
触发方式：

通过 cto.new task 触发
通过 GitHub issue 触发
工作内容示例：

每日工作：
  ├─ 接收trigger.yml的启动信号
  ├─ 运行所有分析脚本
  │  ├─ feature_extraction.py
  │  ├─ ai_feature_synthesis.py
  │  ├─ chip_distribution.py
  │  ├─ model_training.py
  │  └─ similarity_filter.py
  ├─ 生成输出文件
  ├─ 上传GitHub
  └─ 更新Dashboard数据

每周工作：
  ├─ 代码优化和重构
  ├─ 性能测试
  ├─ 问题修复（如有）

每月工作：
  ├─ 重大功能开发
  ├─ 架构优化
  └─ 依赖库更新
3️⃣ 消息面分析员工⭐
职责：

每日监控股票相关政策和重大消息
分析对候选股票的影响
生成消息面风险评估
动态调整相似度筛选的权重
权限：

✅ 查看：所有数据
✅ 修改：daily_news_analysis.json 文件
✅ Dashboard：可查看，需密码才能修改权重
❌ 不能修改：代码
输出文件：daily_news_analysis.json

{
  "date": "2025-12-15",
  "important_events": [
    {
      "category": "政策",
      "title": "央行降准0.5个百分点",
      "impact": "利好金融股",
      "affected_sectors": ["金融", "房地产"],
      "weight_adjustment": 1.3
    },
    {
      "category": "行业",
      "title": "新能源政策支持力度加大",
      "impact": "利好新能源汽车和光伏",
      "affected_sectors": ["汽车", "电气设备"],
      "weight_adjustment": 1.4
    }
  ],
  "sector_impact": {
    "金融": 1.3,
    "房地产": 1.2,
    "医药生物": 0.9,
    "科技": 1.4,
    "消费": 1.1,
    "汽车": 1.4,
    "电气设备": 1.3
  },
  "risk_assessment": "中等",
  "sentiment_score": 0.65,
  "recommendations": [
    "重点关注金融和房地产板块",
    "谨慎看待医药板块短期表现",
    "科技和新能源板块维持高权重"
  ],
  "weight_adjustments": {
    "finance": 1.3,
    "real_estate": 1.2,
    "pharma": 0.9,
    "tech": 1.4,
    "consumer": 1.1,
    "auto": 1.4,
    "power": 1.3
  }
}
工作方式：

定时：每个交易日 09:00-15:00 持续监控
提交截止：每个交易日 15:30 之前提交分析
方式：可以是人工分析 + 手工填写 JSON
或者：AI辅助分析（接入新闻API，如百度新闻、新浪财经等）
Dashboard权限：

查看：✅ 候选股票、跟踪数据、参数配置
修改：✅ 行业权重（需密码）
执行：❌ 不能手动触发工作流
考虑因素：

政策面：央行政策、财政政策、产业政策
市场面：板块热点、资金流向、情绪指标
公司面：重大公告、融资、并购
风险面：风险警示、停牌、退市预警
4️⃣ 监督员工⭐ 新增职位
职责：

监控项目日常运行状态
监督工作流执行情况
检测和记录异常问题
向项目经理报告
生成监督报告（中文）
权限：

✅ 查看：所有数据
✅ 生成：supervisor_report.json 文件
✅ Dashboard：可查看监督报告板块
❌ 不能修改：参数和代码
输出文件：supervisor_report.json

监控内容：

数据采集层：
├─ 4个数据程序是否按时完成
├─ 数据文件是否完整（行数、列数）
├─ 是否有缺失或异常
└─ API调用是否超限

工作流层：
├─ GitHub Actions是否按时触发
├─ 各个workflow运行是否成功
├─ 是否有失败或超时
└─ 执行耗时是否异常

分析层：
├─ 各个分析脚本是否运行成功
├─ 输出文件是否生成
├─ 特征数据是否完整
└─ 候选股票数是否在预期范围

员工层：
├─ 消息面分析员工是否及时提交
├─ 各员工的任务完成情况
├─ 是否有人工介入需求
└─ 是否有紧急问题

Dashboard层：
├─ 网页数据是否实时同步
├─ 参数是否生效
└─ 用户操作是否正常
工作方式：

定时：每个交易日 16:00 生成日报
频率：日报 + 周报 + 月报
自动化：脚本自动检测 + 人工复核
报告格式：JSON（最终展示在网页）
通知机制：

⚠️ 警告级别：发邮件/Slack通知项目经理
🔴 严重级别：立即通知项目经理 + 自动暂停后续分析
Dashboard权限：

查看：✅ 监督报告、项目进度、工作流状态
生成报告：✅ 自动或手动
修改：❌ 不能修改任何参数
员工权限速查表
| 功能 | 项目经理 | AI Agent | 消息分析 | 监督员工 |
|------|---------|---------|---------|---------|
| 查看Dashboard | ✅ | 📖只读 | ✅ | ✅ |
| 修改参数 | ✅ | ❌ | ⚠️行业权重 | ❌ |
| 修改代码 | ❌ | ✅ | ❌ | ❌ |
| 修改消息面 | ❌ | ❌ | ✅ | ❌ |
| 生成报告 | ❌ | ✅ | ❌ | ✅ |
| 手动触发workflow | ✅ | ❌ | ❌ | ❌ |
| 查看监督报告 | ✅ | 📖只读 | ✅ | ✅ |
| 生成监督报告 | ❌ | ❌ | ❌ | ✅ |
| 密码权限 | 完全 | 无 | 部分 | 无 |

---

## 📅 4阶段实现路线图

### 阶段1：基础框架搭建（第1-2周）

**目标**：完成数据采集、特征提取、基础ML模型

**任务清单**：
- ☐ 搭建本地APScheduler定时框架
- ☐ 完成4个数据采集程序
  - ☐ collect_daily_minute.py
  - ☐ collect_weekly.py
  - ☐ collect_monthly.py
  - ☐ collect_financial.py
- ☐ 搭建 github_trigger.py 触发机制
- ☐ 完成特征提取
  - ☐ feature_extraction.py（134个原始特征）
  - ☐ ai_feature_synthesis.py（10个AI特征）
  - ☐ chip_distribution.py（10个筹码特征）
- ☐ 完成特征工程
  - ☐ feature_normalization.py（标准化）
  - ☐ feature_importance.py（重要性排名）
- ☐ 搭建基础ML模型
  - ☐ model_training.py（LR/RF/GB）
  - ☐ model_ensemble.py（集成）

**预期产出**：
- ✅ D:\cto\data\analysis_output\ （各类输出文件）
- ✅ feature_importance_ranking.csv（特征排名）
- ✅ model_ensemble.pkl（集成模型）
- ✅ 框架备份 v1.1

**确认点**：
- [ ] 项目经理确认：数据采集成功，文件完整
- [ ] 项目经理确认：特征提取无误
- [ ] 项目经理确认：ML模型训练完成

---

### 阶段2：相似度筛选与跟踪（第3周）

**目标**：完成相似度筛选、30天跟踪、基础Dashboard

**任务清单**：
- ☐ 完成相似度筛选
  - ☐ similarity_filter.py（主程序）
  - ☐ filtering_logic.py（50%→40%→30%递进）
  - ☐ 集成：筹码分布权重
  - ☐ 集成：消息面权重
- ☐ 完成30天跟踪
  - ☐ track_candidates_30d.py
  - ☐ performance_evaluation.py
- ☐ 完成报告生成
  - ☐ generate_daily_report.py
  - ☐ generate_weekly_report.py
  - ☐ generate_monthly_report.py
- ☐ 搭建Dashboard基础
  - ☐ index.html（候选股票列表）
  - ☐ dashboard.js（基础逻辑）
  - ☐ 集成Chart.js图表

**预期产出**：
- ✅ selection_candidates.csv（最终候选）
- ✅ active_tracking.json（跟踪数据）
- ✅ daily_*.md（日报）
- ✅ Dashboard网页（基础版）
- ✅ 框架备份 v1.2

**确认点**：
- [ ] 项目经理确认：候选股票数在预期范围
- [ ] 项目经理确认：Dashboard可正常显示数据
- [ ] 项目经理确认：跟踪数据准确

---

### 阶段3：高级功能与工作流（第4周）

**目标**：完成参数调整面板、GitHub工作流、监督报告

**任务清单**：
- ☐ Dashboard高级功能
  - ☐ 参数调整面板（可调权重、阈值等）
  - ☐ 密码认证（auth.js）
  - ☐ 中英文双语（i18n.js）
  - ☐ 监督报告板块
- ☐ GitHub工作流配置
  - ☐ daily.yml（日分析）
  - ☐ weekly.yml（周报）
  - ☐ monthly.yml（月报）
  - ☐ trigger.yml（触发机制）
  - ☐ deploy.yml（部署网页）
- ☐ 自托管Runner配置
  - ☐ 在本地机器安装Runner
  - ☐ 配置Runner访问本地data目录
- ☐ 监督报告系统
  - ☐ generate_supervisory_report.py
  - ☐ supervisor_report.json 生成
- ☐ 消息面分析集成
  - ☐ daily_news_analysis.json
  - ☐ 权重调整逻辑

**预期产出**：
- ✅ Dashboard完整版（参数调整+密码+双语）
- ✅ GitHub工作流5个（daily/weekly/monthly/trigger/deploy）
- ✅ supervisor_report.json（监督报告）
- ✅ 框架备份 v1.3

**确认点**：
- [ ] 项目经理确认：参数调整生效
- [ ] 项目经理确认：密码保护正常
- [ ] 项目经理确认：GitHub工作流正常触发
- [ ] 项目经理确认：监督报告准确

---

### 阶段4：优化与文档完善（第5周及后续）

**目标**：性能优化、文档完善、上线运维

**任务清单**：
- ☐ 性能优化
  - ☐ 特征计算优化
  - ☐ ML模型推理优化
  - ☐ 数据库查询优化
- ☐ 文档完善
  - ☐ 项目计划.md（本文件）
  - ☐ dashboard_guide.md（使用指南）
  - ☐ monitor_guide.md（监控指南）
  - ☐ parameter_guide.md（参数调整指南）
  - ☐ api_strategy.md（API策略）
  - ☐ README.md（项目说明）
- ☐ 测试与验证
  - ☐ 单元测试（各模块）
  - ☐ 集成测试（端到端）
  - ☐ 回测验证（历史数据）
- ☐ 框架备份与版本控制
  - ☐ framework_backup_v1.4.zip
  - ☐ framework_backup_current.zip

**预期产出**：
- ✅ 完整文档体系
- ✅ 所有代码通过测试
- ✅ 框架备份 v1.4（最终）
- ✅ 项目上线运维

**确认点**：
- [ ] 项目经理确认：所有文档完整
- [ ] 项目经理确认：项目可稳定运维

---

## ⛳ 每步确认机制

### 核心原则

**每完成一步，需项目经理人工确认，方可写入"步骤完成"状态，防止误操作和遗漏。**

### 实现方式

1. **每阶段/每任务完成后**，Dashboard 或 Monitor 页面弹窗提示
   - 示例："请确认本步骤是否完成"

2. **项目经理点击"确认"后**
   - 系统写入进度跟踪文件（`进度跟踪.md`）
   - 在树状结构中对应节点打绿色对号 ✅
   - 自动生成框架备份（vX.X.zip）
   - 记录确认时间和确认人

3. **所有确认操作均有日志记录**
   - 便于追溯、审计

### 示例流程

步骤1：数据采集完成
↓ 页面弹窗："请确认数据采集已完成"
↓ 项目经理点击"确认"
↓ 系统动作：
├─ 写入 进度跟踪.md：数据采集 ✅
├─ 生成备份：framework_backup_v1.1.zip
├─ 记录日志：确认时间、确认人
└─ 释放下一步：特征提取可启动

步骤2：特征提取完成
↓ 页面弹窗："请确认特征提取已完成"
↓ 项目经理点击"确认"
↓ 系统动作：
├─ 写入 进度跟踪.md：特征提取 ✅
├─ 生成备份：framework_backup_v1.2.zip
├─ 记录日志：确认时间、确认人
└─ 释放下一步：ML训练可启动

依此类推...


### 确认检查清单

| # | 确认点 | 检查项 | 项目经理 |
|----|--------|--------|---------|
| 1 | 数据采集 | 4个数据文件完整，无缺失 | ☐ |
| 2 | 特征提取 | 88个特征已生成，无异常 | ☐ |
| 3 | 特征重要性 | feature_importance_ranking.csv 已生成 | ☐ |
| 4 | 筹码分布 | chip_features.csv 已生成 | ☐ |
| 5 | ML模型 | model_ensemble.pkl 训练完成 | ☐ |
| 6 | 相似度筛选 | candidates_50pct.csv 已生成 | ☐ |
| 7 | 降级逻辑 | 50%→40%→30%递进生效 | ☐ |
| 8 | 30天跟踪 | active_tracking.json 已更新 | ☐ |
| 9 | Dashboard基础 | 网页可正常显示数据 | ☐ |
| 10 | 参数面板 | 参数调整生效 | ☐ |
| 11 | 密码认证 | 无密码可查看，有密码可修改 | ☐ |
| 12 | 双语支持 | 中英文切换正常 | ☐ |
| 13 | GitHub工作流 | 5个工作流正常运行 | ☐ |
| 14 | 自托管Runner | Runner正常连接，可执行任务 | ☐ |
| 15 | 消息面分析 | daily_news_analysis.json 已集成 | ☐ |
| 16 | 监督报告 | supervisor_report.json 已集成 | ☐ |
| 17 | 文档完善 | 所有使用手册已完成 | ☐ |
| 18 | 项目上线 | 项目可稳定运维 | ☐ |

---

## 🗂 框架备份策略

### 原则

**每完成一个阶段，自动生成框架备份zip包，命名规范 `framework_backup_vX.X.zip`，并同步到 `框架备份/` 目录，防止丢失和误改。**

### 备份内容

framework_backup_vX.X.zip
│
├─ 📂 scripts/ [所有Python脚本]
│ ├─ data_collection/
│ ├─ feature_engineering/
│ ├─ ml_training/
│ ├─ similarity_filtering/
│ ├─ tracking/
│ ├─ reporting/
│ ├─ utils/
│ └─ tests/
│
├─ 📂 dashboard/ [所有网页代码]
│ ├─ *.html
│ ├─ assets/
│ │ ├─ css/
│ │ ├─ js/
│ │ └─ vendor/
│ └─ server.py
│
├─ 📂 .github/workflows/ [所有工作流]
│ ├─ daily.yml
│ ├─ weekly.yml
│ ├─ monthly.yml
│ ├─ trigger.yml
│ └─ deploy.yml
│
├─ 📂 projects/山脚下/ [所有文档]
│ ├─ 项目计划.md
│ ├─ 进度跟踪.md
│ ├─ 新聊天快速恢复.md
│ ├─ 使用手册/
│ ├─ 员工配置/
│ └─ ...
│
├─ 📄 requirements.txt [依赖清单]
├─ 📄 .gitignore
├─ 📄 README.md
├─ 📄 config.json
└─ 📄 BACKUP_INFO.txt [备份元信息]
├─ 版本：v1.1
├─ 生成时间：2025-12-15 10:30
├─ 生成者：项目经理
├─ 对应阶段：阶段1完成
└─ 文件数量：125个文件


### 备份计划

| 版本 | 对应阶段 | 触发条件 | 文件大小 | 存储路径 |
|------|---------|---------|---------|---------|
| v1.0 | 初始化 | 项目启动 | ~5MB | D:\cto\projects\山脚下\框架备份\framework_backup_v1.0.zip |
| v1.1 | 阶段1完成 | 数据采集+特征提取完成 | ~15MB | D:\cto\projects\山脚下\框架备份\framework_backup_v1.1.zip |
| v1.2 | 阶段2完成 | 相似度筛选+跟踪完成 | ~25MB | D:\cto\projects\山脚下\框架备份\framework_backup_v1.2.zip |
| v1.3 | 阶段3完成 | Dashboard+工作流完成 | ~35MB | D:\cto\projects\山脚下\框架备份\framework_backup_v1.3.zip |
| v1.4 | 阶段4完成 | 文档完善+上线 | ~45MB | D:\cto\projects\山脚下\框架备份\framework_backup_v1.4.zip |
| current | 最新备份 | 每周五 | ~45MB | D:\cto\projects\山脚下\框架备份\framework_backup_current.zip |

### 备份操作

**自动备份脚本**（backup.py）：
```python
import shutil
import json
from datetime import datetime
from pathlib import Path

def create_backup(stage_name, version):
    """生成框架备份"""
    
    # 源目录
    source_dirs = [
        'D:\\cto\\scripts',
        'D:\\cto\\dashboard',
        'D:\\cto\\.github\\workflows',
        'D:\\cto\\projects\\山脚下',
        'D:\\cto\\requirements.txt',
        'D:\\cto\\README.md',
        'D:\\cto\\config.json'
    ]
    
    # 目标备份文件
    backup_name = f'framework_backup_v{version}.zip'
    backup_path = f'D:\\cto\\projects\\山脚下\\框架备份\\{backup_name}'
    
    # 创建备份
    shutil.make_archive(
        backup_path.replace('.zip', ''),
        'zip',
        *source_dirs
    )
    
    # 记录元信息
    metadata = {
        'version': version,
        'stage': stage_name,
        'timestamp': datetime.now().isoformat(),
        'creator': 'AI Agent',
        'file_count': count_files(source_dirs),
        'size_mb': get_file_size(backup_path) / (1024**2)
    }
    
    with open(f'{backup_path}.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return backup_path
📊 项目资源清单
本地存储位置（D:\cto\）
| 类型 | 文件/文件夹 | 大小估计 | 上传GitHub | 说明 |
|------|-----------|---------|-----------|------|
| 数据 | data/ | 300-500MB | ❌ | 原始和分析数据，不上传 |
| 脚本 | scripts/ | 20-30MB | ✅ | 所有Python脚本 |
| 网页 | dashboard/ | 10-15MB | ✅ | 前端代码和资源 |
| 工作流 | .github/workflows/ | <1MB | ✅ | GitHub Actions配置 |
| 文档 | projects/山脚下/ | 5-10MB | ✅ | 项目文档和报告 |
| 日志 | logs/ | 50-100MB | ✅ | 分析日志和API使用日志 |
| 配置 | 根目录 | <1MB | ✅ | requirements.txt、config.json等 |
| 备份 | projects/山脚下/框架备份/ | 150-200MB | 部分✅ | 框架备份zip包（可选上传） |
| 总计 | | ~500-1000MB | | |

GitHub仓库结构（不包含本地原始数据）
cto/ (GitHub repo)
│
├─ 📂 scripts/                      (~20MB)
│  ├─ data_collection/
│  ├─ feature_engineering/
│  ├─ ml_training/
│  ├─ similarity_filtering/
│  ├─ tracking/
│  ├─ reporting/
│  ├─ utils/
│  └─ tests/
│
├─ 📂 dashboard/                    (~10MB)
│  ├─ index.html
│  ├─ monitor.html
│  ├─ guide.html
│  ├─ assets/
│  └─ server.py
│
├─ 📂 .github/workflows/            (<1MB)
│  ├─ daily.yml
│  ├─ weekly.yml
│  ├─ monthly.yml
│  ├─ trigger.yml
│  └─ deploy.yml
│
├─ 📂 projects/山脚下/             (~5MB)
│  ├─ 项目计划.md
│  ├─ 进度跟踪.md
│  ├─ 新聊天快速恢复.md
│  ├─ 日报/
│  ├─ 周报/
│  ├─ 月报/
│  ├─ 员工配置/
│  ├─ 使用手册/
│  └─ API调用策略/
│
├─ 📂 logs/                         (~50MB，可定期清理)
│  ├─ api_usage/
│  └─ analysis/
│
├─ 📄 requirements.txt              (<1MB)
├─ 📄 .gitignore                    (<1MB)
├─ 📄 README.md                     (<1MB)
└─ 📄 config.json                   (<1MB)

总计：~85-90MB（不含原始数据）
外部依赖与工具
| 工具/库 | 版本 | 用途 | 来源 |
|--------|------|------|------|
| Python | 3.10+ | 编程语言 | python.org |
| Baostock API | latest | 股票数据采集 | baostock.com |
| APScheduler | 3.10+ | 本地定时任务 | pip |
| Pandas | 1.5+ | 数据处理 | pip |
| NumPy | 1.21+ | 数值计算 | pip |
| Scikit-learn | 1.0+ | 机器学习 | pip |
| XGBoost/LightGBM | latest | 梯度提升 | pip |
| Chart.js | 3.9+ | 前端图表 | CDN |
| ECharts | 5.4+ | 筹码分布图 | CDN |
| Tailwind CSS | 3.0+ | 前端样式 | CDN |
| Flask | 2.0+ | 后端服务器 | pip |
| GitHub API | v3 | GitHub交互 | github.com |
| GitHub Actions | latest | CI/CD | github.com |

✅ 最终确认清单
在开始实施项目前，请确认以下事项：

[ ] 项目经理：已理解完整的项目计划和4阶段路线图
[ ] 项目经理：已确认所有7项同等级要求均已涵盖
[ ] 项目经理：已确认员工配置（项目经理、AI Agent、消息面分析、监督员工）
[ ] 项目经理：已确认Dashboard功能（参数调整、双语、密码、监督报告）
[ ] 项目经理：已确认GitHub工作流架构（自托管Runner、trigger.yml、事件驱动）
[ ] 项目经理：已确认框架备份计划（每阶段生成）
[ ] 项目经理：已确认每步确认机制（完成→确认→备份→下步）
[ ] 项目经理：已准备好Slack频道（用于跨聊天窗口协调）
[ ] 项目经理：本地已安装Python、依赖库、GitHub Actions Runner
[ ] 项目经理：GitHub仓库已创建，已配置自托管Runner
当所有确认完成后，项目正式启动！ 🚀

📌 快速参考
关键文件路径
| 文件 | 路径 |
|------|------|
| 项目计划 | D:\cto\projects\山脚下\项目计划.md |
| 进度跟踪 | D:\cto\projects\山脚下\进度跟踪.md |
| 快速恢复 | D:\cto\projects\山脚下\新聊天快速恢复.md |
| 员工配置 | D:\cto\projects\山脚下\员工配置\staff_config.md |
| 框架备份 | D:\cto\projects\山脚下\框架备份\ |
| 数据采集 | D:\cto\data\ |
| Python脚本 | D:\cto\scripts\ |
| Dashboard | D:\cto\dashboard\ |
| GitHub工作流 | D:\cto.github\workflows\ |

关键命令
# 启动本地定时调度
python D:\cto\scripts\data_collection\scheduler_main.py

# 运行数据采集
python D:\cto\scripts\data_collection\collect_daily_minute.py

# 运行特征提取
python D:\cto\scripts\feature_engineering\feature_extraction.py

# 运行ML训练
python D:\cto\scripts\ml_training\model_training.py

# 运行相似度筛选
python D:\cto\scripts\similarity_filtering\similarity_filter.py

# 启动Dashboard服务器
python D:\cto\dashboard\server.py

# 生成框架备份
python D:\cto\backup.py --version 1.1 --stage "阶段1完成"
监控网址
Dashboard：http://localhost:8080 （参数调整、候选股票）
Monitor：http://localhost:8080/monitor.html （工作流状态、功能按钮）
Guide：http://localhost:8080/guide.html （使用指南、监督报告）
项目计划书 - 最终版 - 2025-12-15

下一步行动：

1.将本文保存为 D:\cto\projects\山脚下\项目计划.md
2.同步到GitHub仓库
3.与团队分享并确认
4.在 进度跟踪.md 中记录计划完成时间
5.开始阶段1实施

---
