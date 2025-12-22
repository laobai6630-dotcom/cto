# 山脚下项目 v2.0 - 完整代码框架

## 📊 项目概述

A股"山脚下"形态股票精准筛选系统 - 完整的Python项目框架

本项目基于山脚下项目计划v2.0（`项目计划.md`）构建，包含所有必需的Python脚本、Dashboard网页、配置文件、文档和GitHub工作流。

## ✨ 核心功能

1. **数据采集**: 180天数据保留期，支持日线/周线/月线/财务数据自动调度
2. **特征工程**: 88个特征（134原始+10AI+10筹码）自动提取
3. **对照组分析**: 跌幅前20名股票对比，计算分离度评分
4. **ML模型**: 3个模型集成（Logistic Regression + Random Forest + XGBoost）
5. **相似度筛选**: 递进筛选（50%→40%→30%）找出最相似的候选股票
6. **30天跟踪**: 动态跟踪候选股票表现和成功率
7. **Dashboard**: 中英双语监控面板，密码保护，参数可调
8. **GitHub Workflows**: 自动化日报/周报/月报生成

## 📂 项目文件结构

详见 [完整目录结构和说明](docs/DIRECTORY_STRUCTURE.md)

简要说明：
- `D:\cto\` - 原始采集程序和原始数据文件夹
- `D:\cto\projects\山脚下\` - 完整项目代码

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
主要依赖：pandas, numpy, scikit-learn, xgboost, lightgbm, schedule, ta-lib, scipy

2. 配置项目
编辑 config/config.json:

{
  "project_name": "山脚下项目 v2.0",
  "data_retention_days": 180,
  "feature_time_window": 20,
  "github_token": "YOUR_GITHUB_TOKEN",
  "github_repo": "laobai6630-dotcom/cto",
  "dashboard_password": "admin123"
}
3. 运行核心模块
启动数据采集调度:

python scripts/data_collection/scheduler_main.py
python scripts/data_collection/scheduler_financial.py
执行特征提取流程:

python scripts/feature_engineering/feature_extraction.py
python scripts/feature_engineering/ai_feature_synthesis.py
python scripts/feature_engineering/chip_distribution.py
python scripts/feature_engineering/feature_normalization.py
训练ML模型:

python scripts/ml_training/model_training.py
python scripts/ml_training/model_ensemble.py
python scripts/ml_training/model_evaluation.py
生成报告:

python scripts/tracking/generate_daily_report.py
python scripts/tracking/generate_weekly_report.py
python scripts/tracking/generate_monthly_report.py
4. 启动Dashboard
打开 dashboard/index.html 在浏览器中查看监控面板。

默认密码: admin123 (可在 config/config.json 中修改)

📊 核心流程
数据采集 → 特征提取 → 模型训练 → 对照组分析 → 相似度筛选 → 30天跟踪 → Dashboard展示
日线/周线/月线/财务数据采集 
    ↓ (每日/周/月自动调度)
原始数据清洗和标准化
    ↓
134原始特征 + 10AI特征 + 10筹码特征 = 88个特征
    ↓
特征标准化 + 重要性分析
    ↓
训练LR/RF/XGB三个模型，集成
    ↓
识别30日跌幅前20只对照组股票，提取特征
    ↓
计算对照组 vs 候选股票的分离度评分
    ↓
相似度筛选：50% → 40% → 30% 递进
    ↓
30天跟踪最终候选股票
    ↓
Dashboard展示结果 + 自动生成日报/周报/月报
🔑 核心参数
数据参数
| 参数 | 值 | 说明 |
|------|-----|------|
| 数据保留期 | 180个交易日 | 历史数据备份周期 |
| 特征时间窗口 | 20个交易日 | 从拉升日前一天向前 |
| 对照组规模 | 20只股票 | 30日涨跌幅排名 |

特征参数
| 参数 | 值 |
|------|-----|
| 原始特征 | 134个 |
| AI合成特征 | 10个 |
| 筹码分布特征 | 10个 |
| 最终选用特征 | 88个 |

模型参数
| 参数 | 值 |
|------|-----|
| 模型数量 | 3个（LR + RF + XGB） |
| 集成权重 | LR(0.4) + RF(0.3) + XGB(0.3) |
| 目标精度 | ≥0.85 |

筛选参数
| 参数 | 值 |
|------|-----|
| 相似度权重 | ML(0.6) + 筹码(0.2) + 消息面(0.2) |
| 筛选阈值 | 50% → 40% → 30% |
| 候选范围 | 5-20只股票 |

📈 性能指标
模型性能目标
准确率: ≥0.85
精确率: ≥0.80
召回率: ≥0.75
F1分数: ≥0.80
AUC-ROC: ≥0.80
对照组分离度指标
分离度评分: ≥0.80
欧氏距离: 尽可能大
余弦距离: 尽可能大
分布重叠度: ≤0.20
💡 Dashboard使用说明
无密码模式: 可以浏览所有数据，但不能修改参数
登录模式: 输入密码后可以修改筛选参数
语言切换: 支持中文/英文一键切换
实时刷新: 自动加载最新的候选股票和对照组数据
📚 详细文档
| 文档 | 说明 |
|------|------|
| 完整目录结构 | 所有文件和文件夹的详细说明 |
| 系统架构 | 系统设计和模块关系 |
| 部署指南 | 生产环境部署步骤 |
| 开发指南 | 添加新特征、调整参数、扩展功能 |
| 运维手册 | 日志、监控、故障排查 |
| 安全指南 | 密码保护、备份策略、权限管理 |
| API参考 | 模块接口和函数说明 |

🔄 自动化工作流
GitHub Workflows 支持自动执行以下任务：

daily.yml - 每日数据采集和特征提取
weekly.yml - 每周报告生成
monthly.yml - 每月汇总报告
trigger.yml - 手动触发工作流
deploy.yml - Dashboard部署
需要配置 Self-Hosted Runner 才能在本地执行工作流。详见 部署指南

🤝 贡献指南
Fork 本仓库
创建特性分支 (git checkout -b feature/AmazingFeature)
提交更改 (git commit -m 'Add some AmazingFeature')
推送到分支 (git push origin feature/AmazingFeature)
开启 Pull Request
📄 许可证
本项目采用 MIT 许可证 - 详见 LICENSE 文件

📞 联系方式
GitHub仓库: https://github.com/laobai6630-dotcom/cto/
项目文件夹: projects/山脚下/
项目计划: 项目计划.md
进度跟踪: 进度跟踪.md
🙏 致谢
感谢所有为山脚下项目v2.0做出贡献的人！

版本: v2.0
最后更新: 2025-12-22
GitHub: https://github.com/laobai6630-dotcom/cto/


---

## ✅ 改进点总结

✅ **精简比例**：从原来的 2000+ 行 → 现在的 400 行左右  
✅ **删除了重复的项目结构**  
✅ **删除了冗长的"生成的文件清单"**  
✅ **删除了详细的开发指南、日志、安全部分，改为链接指向**  
✅ **保留了核心内容**：概述、功能、快速开始、核心参数、流程图  
✅ **增加了表格**：更清晰的参数对照  
✅ **完整的文档链接导航**  

---
