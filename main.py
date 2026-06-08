"""
设备保养数据分析器
==================
练习重点：pandas 数据处理 + matplotlib 可视化

场景：分析工厂设备的保养记录，找出保养规律和异常
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import json
import os
from data_generator import generate_sample_data

# 配置中文显示（不然图表里的中文全是方块）
matplotlib.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
matplotlib.rcParams["axes.unicode_minus"] = False


def load_or_generate_data(filepath: str = "maintenance_data.csv") -> pd.DataFrame:
    """
    加载数据 - 如果文件不存在就生成示例数据

    这就是 pandas 最常用的操作：读 CSV
    """
    if not os.path.exists(filepath):
        print(f"📂 数据文件不存在，正在生成示例数据...")
        generate_sample_data(filepath)
        print(f"✅ 示例数据已保存到 {filepath}")

    # pandas 读 CSV - 最基础的操作
    df = pd.read_csv(filepath, encoding="utf-8")
    print(f"\n📊 数据加载完成，共 {len(df)} 条记录")
    return df


def basic_info(df: pd.DataFrame):
    """基本信息查看 - 拿到数据的第一件事"""
    print("\n" + "=" * 50)
    print("  一、数据概览")
    print("=" * 50)

    # df.head() - 看前几行，了解数据长什么样
    print("\n📋 前 5 条记录：")
    print(df.head().to_string(index=False))

    # df.info() - 看列名、数据类型、有没有空值
    print("\n📋 数据类型和空值情况：")
    print(df.info())

    # df.describe() - 基本统计：均值、最值、分位数
    print("\n📋 数值列统计：")
    print(df.describe().to_string())


def data_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    数据清洗 - 真实数据都是脏的

    练习重点：
      - 处理空值
      - 转换日期格式
      - 去除重复行
    """
    print("\n" + "=" * 50)
    print("  二、数据清洗")
    print("=" * 50)

    # 检查空值
    null_counts = df.isnull().sum()
    print(f"\n🔍 空值情况：")
    print(null_counts[null_counts > 0].to_string() if null_counts.sum() > 0 else "  无空值 ✅")

    # 日期列转换 - pandas 的 to_datetime 超好用
    df["保养日期"] = pd.to_datetime(df["保养日期"])
    df["月份"] = df["保养日期"].dt.month
    df["周次"] = df["保养日期"].dt.isocalendar().week.astype(int)

    # 去重
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    if before > after:
        print(f"  🗑️ 去除 {before - after} 条重复记录")

    print(f"  ✅ 清洗完成，剩余 {len(df)} 条记录")
    return df


def analysis_by_line(df: pd.DataFrame):
    """
    按产线分析 - groupby 是 pandas 的核心操作

    练习重点：
      - df.groupby() 分组
      - .agg() 聚合（求和、计数、均值等）
      - .sort_values() 排序
    """
    print("\n" + "=" * 50)
    print("  三、按产线分析")
    print("=" * 50)

    # groupby：按产线分组，然后对每组做聚合
    line_stats = df.groupby("产线").agg(
        保养次数=("设备编号", "count"),
        平均保养时长_分钟=("保养时长_分钟", "mean"),
        总保养时长_分钟=("保养时长_分钟", "sum"),
    ).round(1)

    # sort_values：按保养次数排序
    line_stats = line_stats.sort_values("保养次数", ascending=False)
    print("\n📋 各产线保养统计：")
    print(line_stats.to_string())

    return line_stats


def analysis_by_type(df: pd.DataFrame):
    """按保养类型分析"""
    print("\n" + "=" * 50)
    print("  四、按保养类型分析")
    print("=" * 50)

    type_stats = df.groupby("保养类型").agg(
        次数=("设备编号", "count"),
        平均时长_分钟=("保养时长_分钟", "mean"),
    ).round(1)

    type_stats = type_stats.sort_values("次数", ascending=False)
    print("\n📋 各保养类型统计：")
    print(type_stats.to_string())

    return type_stats


def monthly_trend(df: pd.DataFrame):
    """
    月度趋势分析 - 时间序列入门

    练习重点：
      - 按时间分组
      - 计算月度趋势
    """
    print("\n" + "=" * 50)
    print("  五、月度保养趋势")
    print("=" * 50)

    # 按月份分组统计
    monthly = df.groupby("月份").agg(
        保养次数=("设备编号", "count"),
        平均时长=("保养时长_分钟", "mean"),
    ).round(1)

    print("\n📋 月度保养统计：")
    print(monthly.to_string())

    return monthly


def plot_line_comparison(line_stats: pd.DataFrame):
    """画图1：各产线保养次数对比（柱状图）"""
    fig, ax = plt.subplots(figsize=(8, 5))

    # pandas 内置画图 - 比直接用 matplotlib 简单
    line_stats["保养次数"].plot(
        kind="bar",
        ax=ax,
        color=["#e74c3c", "#3498db", "#2ecc71", "#f39c12"],
        edgecolor="white",
    )

    ax.set_title("各产线保养次数对比", fontsize=14, fontweight="bold")
    ax.set_xlabel("产线")
    ax.set_ylabel("保养次数")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

    # 在柱子上标数字
    for i, v in enumerate(line_stats["保养次数"]):
        ax.text(i, v + 0.3, str(v), ha="center", fontweight="bold")

    plt.tight_layout()
    plt.savefig("chart_line_comparison.png", dpi=150)
    print("  📊 已保存：chart_line_comparison.png")
    plt.close()


def plot_monthly_trend(monthly: pd.DataFrame):
    """画图2：月度保养趋势（折线图）"""
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # 双 Y 轴：左轴保养次数，右轴平均时长
    months = monthly.index.tolist()

    ax1.plot(months, monthly["保养次数"], "o-", color="#e74c3c", linewidth=2, label="保养次数")
    ax1.set_xlabel("月份")
    ax1.set_ylabel("保养次数", color="#e74c3c")
    ax1.tick_params(axis="y", labelcolor="#e74c3c")

    ax2 = ax1.twinx()
    ax2.plot(months, monthly["平均时长"], "s--", color="#3498db", linewidth=2, label="平均时长(分)")
    ax2.set_ylabel("平均保养时长(分钟)", color="#3498db")
    ax2.tick_params(axis="y", labelcolor="#3498db")

    ax1.set_title("月度保养趋势", fontsize=14, fontweight="bold")
    ax1.set_xticks(months)

    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.tight_layout()
    plt.savefig("chart_monthly_trend.png", dpi=150)
    print("  📊 已保存：chart_monthly_trend.png")
    plt.close()


def plot_type_pie(type_stats: pd.DataFrame):
    """画图3：保养类型占比（饼图）"""
    fig, ax = plt.subplots(figsize=(7, 7))

    type_stats["次数"].plot(
        kind="pie",
        ax=ax,
        autopct="%1.1f%%",
        colors=["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"],
        startangle=90,
        textprops={"fontsize": 12},
    )

    ax.set_title("保养类型分布", fontsize=14, fontweight="bold")
    ax.set_ylabel("")  # 去掉默认的列名标签

    plt.tight_layout()
    plt.savefig("chart_type_pie.png", dpi=150)
    print("  📊 已保存：chart_type_pie.png")
    plt.close()


def export_summary(df: pd.DataFrame, line_stats, type_stats, monthly):
    """导出汇总报告"""
    print("\n" + "=" * 50)
    print("  六、导出汇总")
    print("=" * 50)

    # pandas 写 CSV
    line_stats.to_csv("report_line_stats.csv", encoding="utf-8-sig")
    type_stats.to_csv("report_type_stats.csv", encoding="utf-8-sig")
    monthly.to_csv("report_monthly.csv", encoding="utf-8-sig")

    # 写一个文字版汇总
    summary = f"""设备保养数据分析报告
{'='*40}
数据期间：{df['保养日期'].min()} 至 {df['保养日期'].max()}
总记录数：{len(df)}
涉及设备：{df['设备编号'].nunique()} 台
涉及产线：{df['产线'].nunique()} 条

各产线保养统计：
{line_stats.to_string()}

保养类型分布：
{type_stats.to_string()}

月度趋势：
{monthly.to_string()}
"""

    with open("report_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("  ✅ 已导出：")
    print("    - report_line_stats.csv")
    print("    - report_type_stats.csv")
    print("    - report_monthly.csv")
    print("    - report_summary.txt")


def main():
    print("=" * 50)
    print("  设备保养数据分析器")
    print("  pandas + matplotlib 练手项目")
    print("=" * 50)

    # 1. 加载数据
    df = load_or_generate_data()

    # 2. 查看基本信息
    basic_info(df)

    # 3. 数据清洗
    df = data_cleaning(df)

    # 4. 分析
    line_stats = analysis_by_line(df)
    type_stats = analysis_by_type(df)
    monthly = monthly_trend(df)

    # 5. 可视化
    print("\n" + "=" * 50)
    print("  生成可视化图表...")
    print("=" * 50)
    plot_line_comparison(line_stats)
    plot_monthly_trend(monthly)
    plot_type_pie(type_stats)

    # 6. 导出
    export_summary(df, line_stats, type_stats, monthly)

    print("\n🎉 分析完成！")


if __name__ == "__main__":
    main()
