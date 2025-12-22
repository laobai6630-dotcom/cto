#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务数据采集独立调度程序
每季度第二天开始，连续运行7天
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
        logging.FileHandler(path_config.SCHEDULER_FINANCIAL_LOG, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

collection_progress = {'current_day': 0, 'total_days': 7}


def calculate_quarter_second_day(year=None, month=None):
    """
    计算指定季度的第二天
    
    Args:
        year: 年份，默认为当前年份
        month: 月份，默认为当前月份
        
    Returns:
        季度第二天的datetime对象
    """
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    
    if month in [1, 2, 3]:
        quarter_first_day = datetime(year, 1, 1)
    elif month in [4, 5, 6]:
        quarter_first_day = datetime(year, 4, 1)
    elif month in [7, 8, 9]:
        quarter_first_day = datetime(year, 7, 1)
    else:
        quarter_first_day = datetime(year, 10, 1)
    
    quarter_second_day = quarter_first_day + timedelta(days=1)
    return quarter_second_day


def avoid_monday_for_financial(start_date):
    """
    财务采集专用：如果季度第二天是周一，则顺延到周二
    
    Args:
        start_date: 计划开始日期
        
    Returns:
        调整后的开始日期
    """
    if start_date.weekday() == 0:  # 周一
        adjusted_date = start_date + timedelta(days=1)
        logger.info(f"⚠️  季度第二天 {start_date.date()} 是周一，顺延到周二 {adjusted_date.date()}")
        return adjusted_date
    return start_date


def generate_7day_schedule(start_date):
    """
    生成7天的调度日期列表（避开周一）
    
    Args:
        start_date: 开始日期
        
    Returns:
        包含7个日期的列表
    """
    schedule_dates = []
    current_date = start_date
    day_count = 0
    
    while day_count < 7:
        if current_date.weekday() != 0:  # 不是周一
            schedule_dates.append(current_date)
            day_count += 1
        else:
            logger.info(f"⚠️  跳过周一: {current_date.date()}")
        current_date += timedelta(days=1)
    
    return schedule_dates


def run_financial_collection(day_number, total_days):
    """
    执行财务数据采集任务
    
    Args:
        day_number: 当前是第几天
        total_days: 总共需要采集几天
    """
    start_time = datetime.now()
    task_name = f"财务数据采集 ({day_number}/{total_days})"
    
    logger.info(f"{'='*60}")
    logger.info(f"开始执行任务: {task_name}")
    logger.info(f"程序路径: {path_config.COLLECT_FINANCIAL_PY}")
    logger.info(f"采集进度: 第 {day_number} 天 / 共 {total_days} 天")
    
    try:
        if not Path(path_config.COLLECT_FINANCIAL_PY).exists():
            raise FileNotFoundError(f"采集程序不存在: {path_config.COLLECT_FINANCIAL_PY}")
        
        result = subprocess.run(
            [sys.executable, str(path_config.COLLECT_FINANCIAL_PY)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=7200
        )
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if result.returncode == 0:
            logger.info(f"✅ SUCCESS: {task_name} 执行成功")
            logger.info(f"⏱️  耗时: {elapsed:.2f} 秒")
            if result.stdout:
                logger.info(f"输出:\n{result.stdout}")
            
            collection_progress['current_day'] = day_number
            logger.info(f"📊 总进度: {day_number}/{total_days} ({day_number/total_days*100:.1f}%)")
            
            if day_number == total_days:
                logger.info("🎉 财务数据采集已完成全部7天任务！")
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


def setup_quarterly_schedule(scheduler):
    """
    设置季度财务数据采集调度
    在每个季度的第二天 11:30 启动，连续7天
    
    Args:
        scheduler: APScheduler调度器实例
    """
    now = datetime.now()
    
    quarter_second_day = calculate_quarter_second_day(now.year, now.month)
    start_date = avoid_monday_for_financial(
        quarter_second_day.replace(hour=11, minute=30, second=0, microsecond=0)
    )
    
    logger.info(f"📅 当前季度: Q{(now.month-1)//3+1} {now.year}")
    logger.info(f"📅 季度第二天: {quarter_second_day.date()}")
    logger.info(f"📅 实际开始日期: {start_date.date()} {start_date.strftime('%H:%M')}")
    
    schedule_dates = generate_7day_schedule(start_date.replace(hour=0, minute=0, second=0))
    
    logger.info(f"\n📋 7天采集计划:")
    for idx, date in enumerate(schedule_dates, 1):
        schedule_time = date.replace(hour=11, minute=30, second=0)
        logger.info(f"  第{idx}天: {schedule_time.strftime('%Y-%m-%d (%A) %H:%M')}")
        
        scheduler.add_job(
            func=lambda day=idx: run_financial_collection(day, 7),
            trigger=DateTrigger(run_date=schedule_time),
            id=f'financial_day_{idx}',
            name=f'财务数据采集-第{idx}天',
            max_instances=1,
            replace_existing=True
        )
    
    logger.info(f"\n✅ 已配置7天财务数据采集任务")


def setup_auto_quarterly_trigger(scheduler):
    """
    设置自动季度触发器
    在每个季度的第二天自动启动7天采集计划
    """
    @scheduler.scheduled_job(
        trigger=CronTrigger(month='1,4,7,10', day=2, hour=11, minute=30),
        id='quarterly_trigger',
        name='季度财务采集触发器',
        max_instances=1
    )
    def quarterly_financial_trigger():
        """季度触发器：启动7天采集计划"""
        logger.info("🔔 季度财务采集触发器被触发")
        
        now = datetime.now()
        if now.weekday() == 0:
            logger.warning(f"⚠️  今天是周一，顺延到明天 11:30")
            tomorrow = now + timedelta(days=1)
            scheduler.add_job(
                func=lambda: setup_quarterly_schedule(scheduler),
                trigger=DateTrigger(run_date=tomorrow.replace(hour=11, minute=30)),
                id='quarterly_trigger_postponed',
                replace_existing=True
            )
        else:
            setup_quarterly_schedule(scheduler)
    
    logger.info("✅ 已设置季度自动触发器 (1/4/7/10月 2日 11:30)")


def main():
    """主函数"""
    logger.info("="*60)
    logger.info("🚀 山脚下项目 - 财务数据采集调度系统启动")
    logger.info("="*60)
    
    try:
        path_config.verify_paths()
        logger.info("✅ 路径验证通过")
    except Exception as e:
        logger.error(f"❌ 路径验证失败: {e}")
        return 1
    
    scheduler = BlockingScheduler()
    
    setup_auto_quarterly_trigger(scheduler)
    
    now = datetime.now()
    current_quarter_start = calculate_quarter_second_day(now.year, now.month)
    
    if now.date() <= (current_quarter_start + timedelta(days=10)).date():
        logger.info("\n🔍 检测到当前在季度初期，设置本季度的7天采集计划...")
        setup_quarterly_schedule(scheduler)
    
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
        
        if collection_progress['current_day'] > 0:
            logger.info(f"\n📊 本次采集进度: {collection_progress['current_day']}/{collection_progress['total_days']} 天")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
