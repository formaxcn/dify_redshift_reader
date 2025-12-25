import requests
import csv
import os
from datetime import datetime

def fetch_install_count():
    """
    从Dify Marketplace API获取插件安装数量
    """
    url = "https://marketplace.dify.ai/api/v1/plugins/formaxcn/redshift_reader"
    
    try:
        # 发送GET请求获取API数据
        response = requests.get(url)
        response.raise_for_status()
        
        # 解析JSON响应
        data = response.json()
        
        # 根据实际返回的数据结构获取安装数量
        install_count = data.get("data", {}).get("plugin", {}).get("install_count")
        
        if install_count is not None:
            return install_count
        else:
            print("无法找到安装数量信息")
            return None
            
    except requests.RequestException as e:
        print(f"获取API数据时出错: {e}")
        return None
    except ValueError as e:  # ValueError会在JSON解析失败时抛出
        print(f"解析API响应时出错: {e}")
        return None

def save_to_csv(install_count):
    """
    将安装数量和当前日期保存到CSV文件
    """
    filename = "download.csv"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 检查文件是否存在
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # 如果文件不存在，先写入表头
        if not file_exists:
            writer.writerow(["日期", "安装数"])
        
        # 写入当前数据
        writer.writerow([current_date, install_count])
    
    print(f"数据已保存到 {filename}: {current_date} - {install_count}")

def main():
    """
    主函数
    """
    print("正在获取插件安装数量...")
    install_count = fetch_install_count()
    
    if install_count is not None:
        print(f"当前安装数量: {install_count}")
        save_to_csv(install_count)
    else:
        print("获取安装数量失败")

if __name__ == "__main__":
    main()