import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

def generate_chart():
    """
    根据download.csv文件生成安装数趋势曲线图
    """
    # 检查文件是否存在
    if not os.path.exists('download.csv'):
        print("错误: download.csv 文件不存在")
        return
    
    # 读取CSV文件
    df = pd.read_csv('download.csv')
    
    # 转换日期列为datetime类型
    df['日期'] = pd.to_datetime(df['日期'])
    
    # 按日期排序
    df = df.sort_values('日期')
    
    # 创建图表
    plt.figure(figsize=(12, 6))
    plt.plot(df['日期'], df['安装数'], marker='o', linewidth=2, markersize=6)
    
    # 设置标题和标签
    plt.title('Dify Marketplace Installs', fontsize=16, pad=20)
    plt.xlabel('', fontsize=12)
    plt.ylabel('', fontsize=12)
    
    # 格式化x轴日期显示
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gcf().autofmt_xdate()  # 自动旋转日期标签
    
    # 设置网格
    plt.grid(True, alpha=0.3)
    
    # 在每个数据点上显示具体数值
    for i, row in df.iterrows():
        plt.annotate(str(row['安装数']), 
                    (row['日期'], row['安装数']),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('plugin_installs_trend.png', dpi=300, bbox_inches='tight')
    print("图表已保存为 plugin_installs_trend.png")

if __name__ == "__main__":
    generate_chart()