import pandas as pd
import plotly.express as px
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
    
    # 创建交互式折线图
    fig = px.line(df, x='日期', y='安装数', 
                  title='Dify Marketplace Installs',
                  markers=True,
                  labels={'安装数': '', '日期': ''})
    
    # 在数据点上显示数值
    fig.update_traces(textposition='top center', text=df['安装数'])
    
    # 保存为PNG图片
    fig.write_image('plugin_installs_trend.png', width=1200, height=600, scale=2)
    
    print("图表已保存为 plugin_installs_trend.png")

if __name__ == "__main__":
    generate_chart()