

完整的 cto 文件夹树状图（包含路径、名称、作用说明）：



D:\\cto\\  ← Git 仓库根目录

│

├─ 【采集程序 - 原始数据采集】

│  ├─ 日线和分钟线数据获取.py          ※ 采集日线和分钟线数据

│  ├─ 周线数据获取.py                  ※ 采集周线数据

│  ├─ 月线数据获取.py                  ※ 采集月线数据

│  └─ 财务和基本面数据获取.py          ※ 采集财务数据（一天一次，7天采集完）

│

├─ 【原始数据输出文件夹 - 采集程序输出】

│  ├─ daily\_minute\_data/               ※ 日线+分钟线数据输出

│  │  ├─ daily\_data.csv                ※ 最新数据

│  │  ├─ daily\_data\_backup.csv         ※ 固定备份

│  │  └─ daily\_data\_backup\_YYYY-MM-DD.csv  ※ 历史备份（×180个，保留180日）

│  │

│  ├─ weekly\_data/                     ※ 周线数据输出

│  │  ├─ weekly\_data.csv               ※ 最新周线数据

│  │  └─ weekly\_data\_backup\_YYYY-MM-DD.csv  ※ 历史备份

│  │

│  ├─ monthly\_data/                    ※ 月线数据输出

│  │  └─ monthly\_data.csv              ※ 最新月线数据

│  │

│  └─ financial\_data/                  ※ 财务数据输出

│     ├─ profit\_data.csv               ※ 利润数据

│     ├─ balance\_data.csv              ※ 资产负债表数据

│     ├─ operation\_data.csv            ※ 运营数据

│     ├─ basic\_info.csv                ※ 基本信息

│     └─ \[其他财务备份]

│

├─ .git/                               ※ Git版本控制目录

├─ .gitignore                          ※ Git忽略文件列表

├─ README.md                           ※ 项目说明文档

│

└─ projects\\

&nbsp;  │

&nbsp;  └─ 山脚下\\                          ← 完整项目目录

&nbsp;     │

&nbsp;     ├─ 【项目文档】

&nbsp;     │  ├─ 项目计划.md                ※ 完整项目计划书（v2.0）

&nbsp;     │  ├─ 项目计划\_目录导航.md       ※ 项目计划快速导航索引

&nbsp;     │  ├─ 进度跟踪.md                ※ 实时进度跟踪表

&nbsp;     │  ├─ 新聊天快速恢复.md          ※ 新窗口快速恢复清单

&nbsp;     │  ├─ README.md                  ※ 项目说明文档

&nbsp;     │  └─ PROJECT\_SUMMARY.md         ※ 项目总结文档

&nbsp;     │

&nbsp;     ├─ config/                       ※ 配置文件目录

&nbsp;     │  ├─ path\_config.py             ※ 【NEW】统一路径管理（所有程序从这里读取路径）

&nbsp;     │  ├─ config.json                ※ 项目配置

&nbsp;     │  ├─ parameters.json            ※ 参数配置

&nbsp;     │  └─ weights.json               ※ 权重配置

&nbsp;     │

&nbsp;     ├─ scripts/                      ※ 程序脚本主目录

&nbsp;     │  │

&nbsp;     │  ├─ data\_collection/           ※ 【数据采集调度】

&nbsp;     │  │  ├─ scheduler\_main.py       ※ 【NEW】主调度程序（调度日线、周线、月线）

&nbsp;     │  │  ├─ scheduler\_financial.py  ※ 【NEW】财务采集独立调度（7天采集）

&nbsp;     │  │  └─ data\_cleaning.py        ※ 数据清洗程序

&nbsp;     │  │

&nbsp;     │  ├─ feature\_engineering/       ※ 【特征提取】

&nbsp;     │  │  ├─ feature\_extraction.py   ※ 提取134个原始特征

&nbsp;     │  │  ├─ ai\_feature\_synthesis.py ※ 合成10个AI特征

&nbsp;     │  │  ├─ chip\_distribution.py    ※ 提取10个筹码分布特征

&nbsp;     │  │  ├─ feature\_normalization.py ※ 特征标准化处理

&nbsp;     │  │  └─ feature\_importance.py   ※ 特征重要性排名

&nbsp;     │  │

&nbsp;     │  ├─ ml\_training/               ※ 【ML模型训练】

&nbsp;     │  │  ├─ model\_training.py       ※ 模型训练主程序

&nbsp;     │  │  ├─ model\_ensemble.py       ※ 模型集成（LR+RF+GB）

&nbsp;     │  │  └─ model\_evaluation.py     ※ 模型评估指标计算

&nbsp;     │  │

&nbsp;     │  ├─ filtering/                 ※ 【相似度筛选】

&nbsp;     │  │  ├─ similarity\_filter.py    ※ 相似度筛选主程序

&nbsp;     │  │  └─ filtering\_logic.py      ※ 递进筛选逻辑（50%→40%→30%）

&nbsp;     │  │

&nbsp;     │  ├─ contrast\_group/            ※ 【对照组分析】

&nbsp;     │  │  ├─ identify\_contrast\_group.py    ※ 识别跌幅前20名对照组

&nbsp;     │  │  ├─ extract\_contrast\_features.py  ※ 提取对照组特征

&nbsp;     │  │  └─ compare\_contrast\_vs\_candidates.py ※ 对比分析

&nbsp;     │  │

&nbsp;     │  ├─ tracking/                  ※ 【30天跟踪】

&nbsp;     │  │  ├─ track\_candidates\_30d.py       ※ 跟踪候选股票30天

&nbsp;     │  │  ├─ performance\_evaluation.py     ※ 效果评估

&nbsp;     │  │  ├─ generate\_daily\_report.py      ※ 生成日报

&nbsp;     │  │  ├─ generate\_weekly\_report.py     ※ 生成周报

&nbsp;     │  │  └─ generate\_monthly\_report.py    ※ 生成月报



