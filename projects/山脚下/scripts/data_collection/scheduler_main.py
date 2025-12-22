#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主调度程序 - 负责调度日线、周线、月线数据采集任务
使用 APScheduler 实现定时调度，包含避开周一逻辑
"""

import sys
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from config import path_config

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(path_config.SCHEDULER_MAIN_LOG, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def avoid_monday(target_date):
    """
    检查日期是否为周一，如果是则顺延到周二
    
    Args:
        target_date: datetime对象
        
    Returns:
        调整后的datetime对象
    """
    if target_date.weekday() == 0:  # 0 = 周一
        adjusted_date = target_date + timedelta(days=1)
        logger.info(f"⚠️  检测到周一 {target_date.date()}，顺延到周二 {adjusted_date.date()}")
        return adjusted_date
    return target_date


def run_collection_task(program_path, task_name):
    """
    执行数据采集任务
    
    Args:
        program_path: 采集程序的路径
        task_name: 任务名称
    """
    start_time = datetime.now()
    logger.info(f"{'='*60}")
    logger.info(f"开始执行任务: {task_name}")
    logger.info(f"程序路径: {program_path}")
    
    # 检查是否为周一
    if start_time.weekday() == 0:
        logger.warning(f"⚠️  今天是周一，跳过任务: {task_name}")
        logger.info(f"{'='*60}")
        return
    
    try:
        if not Path(program_path).exists():
            raise FileNotFoundError(f"采集程序不存在: {program_path}")
        
        result = subprocess.run(
            [sys.executable, str(program_path)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=3600
        )
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if result.returncode == 0:
            logger.info(f"✅ SUCCESS: {task_name} 执行成功")
            logger.info(f"⏱️  耗时: {elapsed:.2f} 秒")
            if result.stdout:
                logger.info(f"输出:\n{result.stdout}")
        else:
            logger.error(f"❌ ERROR: {task_name} 执行失败 (返回码: {result.returncode})")
            logger.error(f"错误信息:\n{result.stderr}")
        
    except subprocess.TimeoutExpired:
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.error(f"❌ TIMEOUT: {task_name} 执行超时 (>{elapsed:.0f}秒)")
        
    except Exception as e:
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.error(f"❌ EXCEPTION: {task_name} 执行异常")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"错误信息: {str(e)}")
        
    finally:
        logger.info(f"{'='*60}\n")


def collect_daily_minute():
    """采集日线和分钟线数据"""
    run_collection_task(
        path_config.COLLECT_DAILY_MINUTE_PY,
        "日线和分钟线数据采集"
    )


def collect_weekly():
    """采集周线数据"""
    run_collection_task(
        path_config.COLLECT_WEEKLY_PY,
        "周线数据采集"
    )


def collect_monthly():
    """采集月线数据"""
    run_collection_task(
        path_config.COLLECT_MONTHLY_PY,
        "月线数据采集"
    )


def setup_scheduler():
    """
    设置定时任务调度
    
    调度配置:
    - 日线数据: 每日 09:00 (避开周一)
    - 周线数据: 每周二 16:00 (自动避开周一)
    - 月线数据: 每月1日 16:00 (避开周一则顺延到2日)
    """
    scheduler = BlockingScheduler()
    
    # 任务1: 日线和分钟线数据 - 每日 09:00
    scheduler.add_job(
        func=collect_daily_minute,
        trigger=CronTrigger(hour=9, minute=0, day_of_week='tue-sun'),
        id='daily_minute_collection',
        name='日线和分钟线数据采集',
        max_instances=1,
        coalesce=True,
        replace_existing=True
    )
    logger.info("✅ 已添加任务: 日线和分钟线数据采集 (周二-周日 09:00)")
    
    # 任务2: 周线数据 - 每周二 16:00
    scheduler.add_job(
        func=collect_weekly,
        trigger=CronTrigger(hour=16, minute=0, day_of_week='tue'),
        id='weekly_collection',
        name='周线数据采集',
        max_instances=1,
        coalesce=True,
        replace_existing=True
    )
    logger.info("✅ 已添加任务: 周线数据采集 (每周二 16:00)")
    
    # 任务3: 月线数据 - 每月1日 16:00 (需避开周一)
    # 使用装饰器方式添加动态检查
    @scheduler.scheduled_job(
        trigger=CronTrigger(hour=16, minute=0, day=1),
        id='monthly_collection',
        name='月线数据采集',
        max_instances=1,
        coalesce=True
    )
    def collect_monthly_with_check():
        """月线数据采集（含周一检查）"""
        today = datetime.now()
        if today.weekday() == 0:  # 周一
            logger.warning(f"⚠️  今天是周一 ({today.date()})，月线数据采集顺延到明天")
            # 重新安排到明天同一时间
            scheduler.add_job(
                func=collect_monthly,
                trigger=DateTrigger(run_date=today + timedelta(days=1)),
                id='monthly_collection_postponed',
                name='月线数据采集（顺延）',
                replace_existing=True
            )
        else:
            collect_monthly()
    
    logger.info("✅ 已添加任务: 月线数据采集 (每月1日 16:00, 遇周一顺延)")
    
    return scheduler


def main():
    """主函数"""
    logger.info("="*60)
    logger.info("🚀 山脚下项目 - 主数据采集调度系统启动")
    logger.info("="*60)
    
    # 验证路径
    try:
        path_config.verify_paths()
        logger.info("✅ 路径验证通过")
    except Exception as e:
        logger.error(f"❌ 路径验证失败: {e}")
        return 1
    
    # 创建并启动调度器
    scheduler = setup_scheduler()
    
    logger.info("\n📋 当前调度任务列表:")
    for job in scheduler.get_jobs():
        logger.info(f"  - {job.name} (ID: {job.id})")
        if hasattr(job, 'next_run_time') and job.next_run_time:
            logger.info(f"    下次运行: {job.next_run_time}")
        else:
            logger.info(f"    触发器: {job.trigger}")
    
    logger.info("\n⏰ 调度器已启动，等待执行任务...")
    logger.info("   按 Ctrl+C 停止调度器\n")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("\n⚠️  收到停止信号，正在关闭调度器...")
        scheduler.shutdown()
        logger.info("✅ 调度器已停止")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
