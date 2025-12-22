#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试调度器配置和功能
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from config import path_config

def test_path_config():
    """测试路径配置"""
    print("=" * 60)
    print("测试1: 路径配置验证")
    print("=" * 60)
    
    try:
        path_config.verify_paths()
        print("✅ 路径配置测试通过\n")
        return True
    except Exception as e:
        print(f"❌ 路径配置测试失败: {e}\n")
        return False

def test_collection_scripts():
    """测试采集脚本是否存在"""
    print("=" * 60)
    print("测试2: 采集脚本检查")
    print("=" * 60)
    
    scripts = [
        ("日线和分钟线", path_config.COLLECT_DAILY_MINUTE_PY),
        ("周线", path_config.COLLECT_WEEKLY_PY),
        ("月线", path_config.COLLECT_MONTHLY_PY),
        ("财务", path_config.COLLECT_FINANCIAL_PY),
    ]
    
    all_exist = True
    for name, script_path in scripts:
        if script_path.exists():
            print(f"✅ {name}采集脚本存在: {script_path}")
        else:
            print(f"❌ {name}采集脚本不存在: {script_path}")
            all_exist = False
    
    print()
    return all_exist

def test_monday_avoidance():
    """测试避开周一逻辑"""
    print("=" * 60)
    print("测试3: 避开周一逻辑")
    print("=" * 60)
    
    from scripts.data_collection.scheduler_main import avoid_monday
    
    test_cases = [
        (datetime(2025, 1, 6), datetime(2025, 1, 7)),   # 周一 -> 周二
        (datetime(2025, 1, 7), datetime(2025, 1, 7)),   # 周二 -> 周二
        (datetime(2025, 1, 13), datetime(2025, 1, 14)), # 周一 -> 周二
    ]
    
    all_passed = True
    for input_date, expected_date in test_cases:
        result = avoid_monday(input_date)
        weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        input_weekday = weekday_names[input_date.weekday()]
        result_weekday = weekday_names[result.weekday()]
        
        if result.date() == expected_date.date():
            print(f"✅ {input_date.date()} ({input_weekday}) -> {result.date()} ({result_weekday})")
        else:
            print(f"❌ {input_date.date()} ({input_weekday}) -> {result.date()} ({result_weekday}), 期望: {expected_date.date()}")
            all_passed = False
    
    print()
    return all_passed

def test_quarterly_calculation():
    """测试季度计算"""
    print("=" * 60)
    print("测试4: 季度第二天计算")
    print("=" * 60)
    
    from scripts.data_collection.scheduler_financial import calculate_quarter_second_day
    
    test_cases = [
        (2025, 1, datetime(2025, 1, 2)),   # Q1
        (2025, 4, datetime(2025, 4, 2)),   # Q2
        (2025, 7, datetime(2025, 7, 2)),   # Q3
        (2025, 10, datetime(2025, 10, 2)), # Q4
    ]
    
    all_passed = True
    for year, month, expected in test_cases:
        result = calculate_quarter_second_day(year, month)
        if result.date() == expected.date():
            print(f"✅ {year}年{month}月 -> Q{(month-1)//3+1} 第二天: {result.date()}")
        else:
            print(f"❌ {year}年{month}月 -> {result.date()}, 期望: {expected.date()}")
            all_passed = False
    
    print()
    return all_passed

def test_7day_schedule():
    """测试7天调度生成"""
    print("=" * 60)
    print("测试5: 7天调度计划生成（避开周一）")
    print("=" * 60)
    
    from scripts.data_collection.scheduler_financial import generate_7day_schedule
    
    start_date = datetime(2025, 1, 2)  # 周四
    schedule = generate_7day_schedule(start_date)
    
    weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    print(f"开始日期: {start_date.date()} ({weekday_names[start_date.weekday()]})")
    print(f"生成 {len(schedule)} 天调度:")
    
    has_monday = False
    for idx, date in enumerate(schedule, 1):
        weekday = weekday_names[date.weekday()]
        print(f"  第{idx}天: {date.date()} ({weekday})")
        if date.weekday() == 0:
            has_monday = True
    
    if len(schedule) == 7 and not has_monday:
        print("✅ 7天调度生成正确，无周一\n")
        return True
    else:
        print(f"❌ 调度生成有误: 天数={len(schedule)}, 包含周一={has_monday}\n")
        return False

def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("🧪 调度器功能测试")
    print("=" * 60 + "\n")
    
    results = []
    
    results.append(("路径配置", test_path_config()))
    results.append(("采集脚本", test_collection_scripts()))
    results.append(("避开周一逻辑", test_monday_avoidance()))
    results.append(("季度计算", test_quarterly_calculation()))
    results.append(("7天调度生成", test_7day_schedule()))
    
    print("=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️  {total-passed} 个测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
