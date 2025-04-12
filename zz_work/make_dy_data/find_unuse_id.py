import os
import pandas as pd
import numpy as np
import re
import glob
from openpyxl import load_workbook
import sys

def main():
    # 获取程序所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 读取file文件夹下的所有csv文件
    file_dir = os.path.join(current_dir, 'file')
    all_files = glob.glob(os.path.join(file_dir, '*.csv'))
    
    if not all_files:
        print("file文件夹中没有找到csv文件")
        sys.exit(1)
    
    # 存储所有商品id
    all_product_ids = []
    
    # 读取每个csv文件
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        try:
            # 尝试不同编码读取文件
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(file_path, encoding='gb2312')
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='gbk')
            
            # 检查是否存在商品id列
            if '商品id' not in df.columns:
                print(f"文件 {file_name} 中没有找到'商品id'列，跳过处理")
                continue
            
            # 提取商品id列
            product_ids = df['商品id'].dropna().astype(str).tolist()
            all_product_ids.extend(product_ids)
            
        except Exception as e:
            print(f"读取文件 {file_name} 时出错: {str(e)}")
            sys.exit(1)
    
    # 去除重复的商品id
    unique_product_ids = list(set(all_product_ids))
    
    # 清理商品id，只保留数字
    cleaned_product_ids = [re.sub(r'\D', '', pid) for pid in unique_product_ids]
    cleaned_product_ids = [pid for pid in cleaned_product_ids if pid]  # 移除空字符串
    
    print(f"从销量数据中提取到 {len(cleaned_product_ids)} 个唯一商品id")
    
    # 读取产品数据表格.xlsx
    product_excel_path = os.path.join(current_dir, '产品数据表格.xlsx')
    
    if not os.path.exists(product_excel_path):
        print("未找到产品数据表格.xlsx文件")
        sys.exit(1)
    
    # 获取所有表格名称
    try:
        xls = pd.ExcelFile(product_excel_path)
        sheet_names = [name for name in xls.sheet_names if name[-1] == '组']
        
        if not sheet_names:
            print("产品数据表格.xlsx中没有找到以'组'结尾的表格")
            sys.exit(1)
        
        # 读取所有符合条件的表格
        all_product_data = []
        
        for sheet_name in sheet_names:
            try:
                df = pd.read_excel(product_excel_path, sheet_name=sheet_name, usecols=["店铺", "姓名", "产品ID", "产品简称"])
                df['表格名'] = sheet_name  # 添加表格名列，用于后续保存
                all_product_data.append(df)
            except Exception as e:
                print(f"读取表格 {sheet_name} 时出错: {str(e)}")
                continue
        
        if not all_product_data:
            print("没有成功读取任何产品数据")
            sys.exit(1)
        
        # 合并所有表格数据
        product_data = pd.concat(all_product_data, ignore_index=True)
        
        # 清理产品ID，只保留数字
        product_data['产品ID原始'] = product_data['产品ID'].copy()  # 保存原始ID用于显示
        product_data['产品ID'] = product_data['产品ID'].astype(str).apply(lambda x: re.sub(r'\D', '', x))
        
        # 将产品ID转换为文本格式
        product_data['产品ID'] = product_data['产品ID'].astype(str)
        
        # 创建用于匹配的数据副本
        product_data_for_matching = product_data.copy()
        
        # 根据产品ID去除重复（保留第一次出现的记录）
        product_data_for_matching = product_data_for_matching.drop_duplicates(subset=['产品ID'])
        
        # 分离匹配和未匹配的产品数据
        matched_ids = product_data_for_matching[product_data_for_matching['产品ID'].isin(cleaned_product_ids)]['产品ID'].tolist()
        
        # 在原始数据中标记匹配状态
        product_data['匹配状态'] = product_data['产品ID'].apply(lambda x: '已使用' if x in matched_ids else '未使用')
        
        # 分离匹配和未匹配的数据
        matched_data = product_data[product_data['匹配状态'] == '已使用'].copy()
        unmatched_data = product_data[product_data['匹配状态'] == '未使用'].copy()
        
        # 删除辅助列
        matched_data.drop(['匹配状态', '产品ID原始'], axis=1, inplace=True)
        unmatched_data.drop(['匹配状态', '产品ID原始'], axis=1, inplace=True)
        
        # 按表格名分组并保存到对应的Excel文件
        with pd.ExcelWriter(os.path.join(current_dir, '产品数据表格保留.xlsx')) as writer:
            for sheet_name, group in matched_data.groupby('表格名'):
                # 删除表格名列
                group = group.drop('表格名', axis=1)
                # 写入Excel
                group.to_excel(writer, sheet_name=sheet_name, index=False)
        
        with pd.ExcelWriter(os.path.join(current_dir, '产品数据表格删除.xlsx')) as writer:
            for sheet_name, group in unmatched_data.groupby('表格名'):
                # 删除表格名列
                group = group.drop('表格名', axis=1)
                # 写入Excel
                group.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"处理完成！")
        print(f"已使用的产品ID数量: {len(matched_data)}")
        print(f"未使用的产品ID数量: {len(unmatched_data)}")
        print(f"结果已保存到 '产品数据表格保留.xlsx' 和 '产品数据表格删除.xlsx'")
        
    except Exception as e:
        print(f"处理产品数据表格时出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()