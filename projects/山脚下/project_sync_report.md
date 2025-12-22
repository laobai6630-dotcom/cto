# projects/山脚下 目录同步检查报告

**检查时间**: 2025-12-22 13:58:16

**项目路径**: D:\cto\projects\山脚下

**GitHub路径**: https://github.com/laobai6630-dotcom/cto/tree/main/projects/山脚下

## 📊 总体状态

| 指标 | 数值 |
|------|------|
| 总文件数 | 63 |
| 已同步 | 0 |
| 本地独有 | 2 |
| 内容不同 | 61 |

**同步率**: ❌ 0.0%

## ⚠️ 本地独有文件（未上传 GitHub）

- `task_manager_config.json`
- `task_manager_data.json`

## 🔄 内容不同的文件

**可能原因**：行尾符差异（CRLF vs LF）

- `PROJECT_SUMMARY.md`
- `README.md`
- `config/config.json`
- `config/parameters.json`
- `config/path_config.py`
- `config/weights.json`
- `dashboard/assets/css/styles.css`
- `dashboard/assets/data/candidates.json`
- `dashboard/assets/data/overview.json`
- `dashboard/assets/js/auth.js`
- `dashboard/assets/js/dashboard.js`
- `dashboard/assets/js/i18n.js`
- `dashboard/index.html`
- `docs/API_REFERENCE.md`
- `docs/ARCHITECTURE.md`
- `docs/CHANGELOG.md`
- `docs/DEPLOYMENT.md`
- `docs/DIRECTORY_STRUCTURE.md`
- `docs/MAINTENANCE.md`
- `docs/README.md`
- `features/feature_window.py`
- `features/raw_feature_extractor.py`
- `locales/en_US.json`
- `locales/zh_CN.json`
- `requirements.txt`
- `scripts/contrast_group/compare_contrast_vs_candidates.py`
- `scripts/contrast_group/extract_contrast_features.py`
- `scripts/contrast_group/identify_contrast_group.py`
- `scripts/data_collection/QUICK_START.md`
- `scripts/data_collection/README.md`
- `scripts/data_collection/data_cleaning.py`
- `scripts/data_collection/scheduler_financial.py`
- `scripts/data_collection/scheduler_main.py`
- `scripts/data_collection/test_schedulers.py`
- `scripts/feature_engineering/ai_feature_synthesis.py`
- `scripts/feature_engineering/chip_distribution.py`
- `scripts/feature_engineering/feature_extraction.py`
- `scripts/feature_engineering/feature_importance.py`
- `scripts/feature_engineering/feature_normalization.py`
- `scripts/filtering/filtering_logic.py`
- `scripts/filtering/similarity_filter.py`
- `scripts/github/github_trigger.py`
- `scripts/ml_training/model_ensemble.py`
- `scripts/ml_training/model_evaluation.py`
- `scripts/ml_training/model_training.py`
- `scripts/monitoring/generate_supervisory_report.py`
- `scripts/tracking/generate_daily_report.py`
- `scripts/tracking/generate_monthly_report.py`
- `scripts/tracking/generate_weekly_report.py`
- `scripts/tracking/performance_evaluation.py`
- `scripts/tracking/track_candidates_30d.py`
- `scripts/utils/backup_manager.py`
- `scripts/utils/check_sync.py`
- `scripts/utils/verify_backup.py`
- `shanjiaxia_task_manager.py`
- `task_manager.py`
- `upgrade_step1_real_features.py`
- `新聊天快速恢复.md`
- `进度跟踪.md`
- `项目计划.md`
- `项目计划_目录导航.md`

**解决方案**：
```bash
cd D:\cto
git config core.autocrlf true
git add --renormalize .
git commit -m 'chore: normalize line endings'
git push origin main
```

## 💡 总体结论

⚠️ **发现同步问题，请参考上方的解决方案。**

