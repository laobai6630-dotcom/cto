完整的 cto 文件夹树状图（包含路径、名称、作用说明）：

D:\cto\  ← Git 仓库根目录
│
├─ 【采集程序 - 原始数据采集】
│  ├─ 日线和分钟线数据获取.py          ※ 采集日线和分钟线数据
│  ├─ 周线数据获取.py                  ※ 采集周线数据
│  ├─ 月线数据获取.py                  ※ 采集月线数据
│  └─ 财务和基本面数据获取.py          ※ 采集财务数据（一天一次，7天采集完）
│
├─ 【原始数据输出文件夹 - 采集程序输出】
│  ├─ daily_minute_data/               ※ 日线+分钟线数据输出
│  │  ├─ daily_data.csv                ※ 最新数据
│  │  ├─ daily_data_backup.csv         ※ 固定备份
│  │  └─ daily_data_backup_YYYY-MM-DD.csv  ※ 历史备份（×180个，保留180日）
│  │
│  ├─ weekly_data/                     ※ 周线数据输出
│  │  ├─ weekly_data.csv               ※ 最新周线数据
│  │  └─ weekly_data_backup_YYYY-MM-DD.csv  ※ 历史备份
│  │
│  ├─ monthly_data/                    ※ 月线数据输出
│  │  └─ monthly_data.csv              ※ 最新月线数据
│  │
│  └─ financial_data/                  ※ 财务数据输出
│     ├─ profit_data.csv               ※ 利润数据
│     ├─ balance_data.csv              ※ 资产负债表数据
│     ├─ operation_data.csv            ※ 运营数据
│     ├─ basic_info.csv                ※ 基本信息
│     └─ [其他财务备份]
│
├─ .git/                               ※ Git版本控制目录
├─ .gitignore                          ※ Git忽略文件列表
├─ README.md                           ※ 项目说明文档
│
└─ projects\
   │
   └─ 山脚下\                          ← 完整项目目录
      │
      ├─ 【项目文档】
      │  ├─ 项目计划.md                ※ 完整项目计划书（v2.0）
      │  ├─ 项目计划_目录导航.md       ※ 项目计划快速导航索引
      │  ├─ 进度跟踪.md                ※ 实时进度跟踪表
      │  ├─ 新聊天快速恢复.md          ※ 新窗口快速恢复清单
      │  ├─ README.md                  ※ 项目说明文档
      │  └─ PROJECT_SUMMARY.md         ※ 项目总结文档
      │
      ├─ config/                       ※ 配置文件目录
      │  ├─ path_config.py             ※ 【NEW】统一路径管理（所有程序从这里读取路径）
      │  ├─ config.json                ※ 项目配置
      │  ├─ parameters.json            ※ 参数配置
      │  └─ weights.json               ※ 权重配置
      │
      ├─ scripts/                      ※ 程序脚本主目录
      │  │
      │  ├─ data_collection/           ※ 【数据采集调度】
      │  │  ├─ scheduler_main.py       ※ 【NEW】主调度程序（调度日线、周线、月线）
      │  │  ├─ scheduler_financial.py  ※ 【NEW】财务采集独立调度（7天采集）
      │  │  └─ data_cleaning.py        ※ 数据清洗程序
      │  │
      │  ├─ feature_engineering/       ※ 【特征提取】
      │  │  ├─ feature_extraction.py   ※ 提取134个原始特征
      │  │  ├─ ai_feature_synthesis.py ※ 合成10个AI特征
      │  │  ├─ chip_distribution.py    ※ 提取10个筹码分布特征
      │  │  ├─ feature_normalization.py ※ 特征标准化处理
      │  │  └─ feature_importance.py   ※ 特征重要性排名
      │  │
      │  ├─ ml_training/               ※ 【ML模型训练】
      │  │  ├─ model_training.py       ※ 模型训练主程序
      │  │  ├─ model_ensemble.py       ※ 模型集成（LR+RF+GB）
      │  │  └─ model_evaluation.py     ※ 模型评估指标计算
      │  │
      │  ├─ filtering/                 ※ 【相似度筛选】
      │  │  ├─ similarity_filter.py    ※ 相似度筛选主程序
      │  │  └─ filtering_logic.py      ※ 递进筛选逻辑（50%→40%→30%）
      │  │
      │  ├─ contrast_group/            ※ 【对照组分析】
      │  │  ├─ identify_contrast_group.py    ※ 识别跌幅前20名对照组
      │  │  ├─ extract_contrast_features.py  ※ 提取对照组特征
      │  │  └─ compare_contrast_vs_candidates.py ※ 对比分析
      │  │
      │  ├─ tracking/                  ※ 【30天跟踪】
      │  │  ├─ track_candidates_30d.py       ※ 跟踪候选股票30天
      │  │  ├─ performance_evaluation.py     ※ 效果评估
      │  │  ├─ generate_daily_report.py      ※ 生成日报
      │  │  ├─ generate_weekly_report.py     ※ 生成周报
      │  │  └─ generate_monthly_report.py    ※ 生成月报
