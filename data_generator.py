"""
示例数据生成器
===============
生成模拟的设备保养记录 CSV，用于数据分析练习

如果后续有真实数据，替换这个文件就行
"""

import pandas as pd
import random
from datetime import datetime, timedelta


def generate_sample_data(filepath: str = "maintenance_data.csv"):
    """生成模拟保养数据"""

    # 设备清单（贴合制造业场景）
    devices = [
        # 8222线设备
        {"设备编号": "PL-8222-M01", "设备名称": "8222主电机", "产线": "8222除气线", "类型": "生产设备"},
        {"设备编号": "PL-8222-P01", "设备名称": "8222真空泵", "产线": "8222除气线", "类型": "生产设备"},
        {"设备编号": "PL-8222-F01", "设备名称": "8222风机", "产线": "8222除气线", "类型": "辅助设备"},
        {"设备编号": "IT-8222-T01", "设备名称": "8222测温仪", "产线": "8222除气线", "类型": "检测设备"},
        # 9610线设备
        {"设备编号": "PL-9610-M01", "设备名称": "9610主电机", "产线": "9610除气线", "类型": "生产设备"},
        {"设备编号": "PL-9610-P01", "设备名称": "9610真空泵", "产线": "9610除气线", "类型": "生产设备"},
        {"设备编号": "PL-9610-W01", "设备名称": "9610注水泵", "产线": "9610除气线", "类型": "辅助设备"},
        {"设备编号": "IT-9610-R01", "设备名称": "9610电阻检测仪", "产线": "9610除气线", "类型": "检测设备"},
    ]

    # 保养类型
    maintenance_types = ["周保养", "月保养", "季度保养", "年度保养"]

    # 生成日期范围（2026年1月到5月）
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 5, 31)

    # 保养人员
    workers = ["张三", "李四", "王五", "赵六", "孙七"]

    records = []
    current_date = start_date

    while current_date <= end_date:
        weekday = current_date.weekday()  # 0=周一, 6=周日

        # 工作日才有保养
        if weekday < 5:
            # 周一：周保养（所有设备）
            if weekday == 0:
                for device in devices:
                    records.append({
                        "设备编号": device["设备编号"],
                        "设备名称": device["设备名称"],
                        "产线": device["产线"],
                        "设备类型": device["类型"],
                        "保养日期": current_date.strftime("%Y-%m-%d"),
                        "保养类型": "周保养",
                        "保养时长_分钟": random.randint(20, 45),
                        "保养人员": random.choice(workers),
                        "保养结果": random.choice(["合格", "合格", "合格", "合格", "需跟进"]),
                    })

            # 每月1号：月保养（随机挑选几台）
            if current_date.day <= 5 and weekday == 0:
                selected = random.sample(devices, k=min(4, len(devices)))
                for device in selected:
                    records.append({
                        "设备编号": device["设备编号"],
                        "设备名称": device["设备名称"],
                        "产线": device["产线"],
                        "设备类型": device["类型"],
                        "保养日期": current_date.strftime("%Y-%m-%d"),
                        "保养类型": "月保养",
                        "保养时长_分钟": random.randint(60, 120),
                        "保养人员": random.choice(workers),
                        "保养结果": random.choice(["合格", "合格", "合格", "需跟进"]),
                    })

        current_date += timedelta(days=1)

    # 转成 DataFrame 并保存
    df = pd.DataFrame(records)

    # 打乱顺序，模拟真实数据（时间不一定严格排序）
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    df.to_csv(filepath, index=False, encoding="utf-8")
    print(f"  ✅ 生成 {len(df)} 条保养记录")


if __name__ == "__main__":
    generate_sample_data()
