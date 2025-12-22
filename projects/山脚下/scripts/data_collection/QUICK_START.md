# 数据采集调度系统 - 快速启动指南

## 🚀 5分钟快速开始

### 1️⃣ 安装依赖

```bash
pip install APScheduler>=3.10.0
```

### 2️⃣ 验证配置

```bash
cd /home/engine/project/projects/山脚下/config
python3 path_config.py
```

期望输出：
```
项目根目录: /home/engine/project
日志目录: /home/engine/project/projects/山脚下/logs
数据目录: /home/engine/project
✅ 所有路径验证通过
```

### 3️⃣ 运行测试

```bash
cd /home/engine/project/projects/山脚下/scripts/data_collection
python3 test_schedulers.py
```

期望输出：
```
通过率: 5/5 (100.0%)
🎉 所有测试通过！
```

### 4️⃣ 启动主调度器

```bash
python3 scheduler_main.py
```

你将看到：
```
🚀 山脚下项目 - 主数据采集调度系统启动
✅ 路径验证通过
✅ 已添加任务: 日线和分钟线数据采集 (周二-周日 09:00)
✅ 已添加任务: 周线数据采集 (每周二 16:00)
✅ 已添加任务: 月线数据采集 (每月1日 16:00, 遇周一顺延)
⏰ 调度器已启动，等待执行任务...
```

### 5️⃣ 启动财务调度器（可选，独立运行）

在另一个终端：
```bash
cd /home/engine/project/projects/山脚下/scripts/data_collection
python3 scheduler_financial.py
```

---

## 📋 调度任务一览表

### 主调度器 (scheduler_main.py)

| 任务 | 频率 | 时间 | 避开周一 |
|------|------|------|---------|
| 日线和分钟线数据 | 每日 | 09:00 | ✅ 周二至周日 |
| 周线数据 | 每周 | 周二 16:00 | ✅ 固定周二 |
| 月线数据 | 每月 | 1日 16:00 | ✅ 遇周一顺延 |

### 财务调度器 (scheduler_financial.py)

| 季度 | 开始日期 | 时间 | 运行天数 |
|------|---------|------|---------|
| Q1 | 1月2日 | 11:30 | 连续7天 |
| Q2 | 4月2日 | 11:30 | 连续7天 |
| Q3 | 7月2日 | 11:30 | 连续7天 |
| Q4 | 10月2日 | 11:30 | 连续7天 |

**注意：** 如果季度第二天是周一，自动顺延到周二

---

## 📊 查看日志

### 实时查看主调度日志

```bash
tail -f /home/engine/project/projects/山脚下/logs/scheduler_main.log
```

### 实时查看财务调度日志

```bash
tail -f /home/engine/project/projects/山脚下/logs/scheduler_financial.log
```

---

## 🔍 检查数据输出

### 查看采集的数据文件

```bash
# 日线数据
ls -lh /home/engine/project/daily_minute_data/

# 周线数据
ls -lh /home/engine/project/weekly_data/

# 月线数据
ls -lh /home/engine/project/monthly_data/

# 财务数据
ls -lh /home/engine/project/financial_data/
```

---

## ⚠️ 常见问题

### Q: 调度器无法启动，提示找不到模块

**A:** 安装 APScheduler
```bash
pip install APScheduler>=3.10.0
```

### Q: 提示路径不存在

**A:** 运行路径验证
```bash
cd /home/engine/project/projects/山脚下/config
python3 path_config.py
```

### Q: 如何停止调度器？

**A:** 按 `Ctrl+C` 优雅停止

### Q: 采集任务为什么没有执行？

**A:** 检查以下几点：
1. 今天是否为周一（避开周一逻辑）
2. 查看日志文件了解详细情况
3. 确认采集脚本是否存在

### Q: 如何手动触发一次采集？

**A:** 直接运行采集脚本
```bash
cd /home/engine/project
python3 日线和分钟线数据获取.py
```

---

## 📚 更多文档

- **完整文档**: [README.md](README.md)
- **部署说明**: [SCHEDULER_SETUP.md](/home/engine/project/SCHEDULER_SETUP.md)
- **完成报告**: [TASK_1_2_COMPLETION_REPORT.md](/home/engine/project/TASK_1_2_COMPLETION_REPORT.md)

---

## 🎯 下一步

1. **生产环境部署**
   - 使用 systemd 或 supervisor 管理进程
   - 配置开机自启动
   - 设置日志轮转

2. **监控和告警**
   - 添加失败告警机制
   - 监控磁盘空间
   - 定期检查日志

3. **数据处理**
   - 实施数据清洗流程
   - 特征工程处理
   - 模型训练准备

---

**祝您使用愉快！** 🎉
