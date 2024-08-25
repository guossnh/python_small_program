import os
import pandas as pd
from openpyxl import load_workbook
from pathlib import Path
import glob
import logging
import re

# 设置日志记录
logging.basicConfig(filename='process_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def process_sales_data():
    # 获取程序文件所在的文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, 'file')
    
    # 获取所有的CSV文件路径
    all_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

    merged_data = pd.DataFrame()
    error_files = []
    month_data_counts = {}
    null_payment_times = 0

    for file in all_files:
        try:
            # 读取CSV文件，保留指定的列
            df = pd.read_csv(file, usecols=['订单号', '订单状态', '支付时间', '商品数量(件)', '商品id', '商家编码-规格维度', '售后状态', '商家实收金额(元)', '快递公司'])
            df['商家编码-规格维度'].fillna('-', inplace=True)
            df['商家编码-规格维度'] = df['商家编码-规格维度'].astype(str)
            
            # 确保每行至少有两个部分，使用默认值填充
            def ensure_two_parts(value):
                parts = value.split('-')
                if len(parts) < 2:
                    parts.append('default')  # 填充默认值
                return '-'.join(parts)
            
            df['商家编码-规格维度'] = df['商家编码-规格维度'].apply(ensure_two_parts)
            
            # 拆分列
            df[['商品编码', '规格数量']] = df['商家编码-规格维度'].str.split('-', expand=True, n=1)
            
            # 处理支付时间，统计每个月的数据量
            df['支付时间'] = pd.to_datetime(df['支付时间'], errors='coerce')
            df['月'] = df['支付时间'].dt.month
            
            for month, count in df['月'].value_counts().items():
                if month in month_data_counts:
                    month_data_counts[month] += count
                else:
                    month_data_counts[month] = count
            
            null_payment_times += df['支付时间'].isna().sum()
            
            # 筛选并删除指定订单状态的记录
            df = df[~df['订单状态'].isin(['未发货，退款成功', '已取消', '已取消，退款成功'])]

            # 合并当前文件数据到总数据框中
            merged_data = pd.concat([merged_data, df], ignore_index=True)
        except Exception as e:
            # 记录出错的文件
            error_files.append(file)
            print(f"处理文件 {file} 时出错：{e}")

    # 清理商品id，只保留数字并转换为文本格式
    if not merged_data.empty:
        merged_data['商品id'] = merged_data['商品id'].apply(lambda x: re.sub(r'\D', '', str(x)))

    # 删除临时的'月'列
    merged_data.drop(columns=['月'], inplace=True)

    # 输出每个月的数据量统计
    for month, count in month_data_counts.items():
        print(f"月份 {month} 有 {count} 条数据")

    # 输出支付时间为空值的记录数
    print(f"支付时间为空值的记录数：{null_payment_times}")

    # 返回合并后的数据框
    return merged_data


#处理快麦数据
def process_km_data(sales_data):
    # 获取程序文件所在的文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__))
    km_folder_path = os.path.join(script_dir, 'km')
    
    # 获取所有的CSV文件路径
    all_km_files = [os.path.join(km_folder_path, file) for file in os.listdir(km_folder_path) if file.endswith('.csv')]

    km_data = pd.DataFrame()

    for file in all_km_files:
        try:
            # 读取CSV文件，忽略前6行，保留指定的列
            df = pd.read_csv(file, skiprows=6, usecols=['商品商家编码', '商品名称'], encoding='GB18030')
            km_data = pd.concat([km_data, df], ignore_index=True)
        except Exception as e:
            print(f"处理文件 {file} 时出错：{e}")

    # 去重
    km_data = km_data.drop_duplicates(subset=['商品商家编码'])

    # 创建商品编码到商品名称的映射
    product_code_to_name = pd.Series(km_data['商品名称'].values, index=km_data['商品商家编码']).to_dict()

    # 处理销量数据
    sales_data['商品名称'] = sales_data['商品编码'].map(product_code_to_name)

    # 找出没有对应商品名称的商品编码
    missing_products = sales_data[sales_data['商品名称'].isna()]['商品编码'].unique()
    
    if len(missing_products) > 0:
        print("以下商品编码在快麦数据表中没有找到对应的商品名称，需要更新快麦表格：")
        for code in missing_products:
            print(code)

    return sales_data



#这块还需要修改不能直接去除重复。需要导出来。然后人工判断。
def process_product_data(sales_data):
    # 获取程序文件所在的文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__))
    product_data_file = os.path.join(script_dir, '产品数据表格.xlsx')

    # 读取所有表格
    all_sheets = pd.read_excel(product_data_file, sheet_name=None)

    # 筛选出名字最后一个字是“组”的表格
    group_sheets = {name: df for name, df in all_sheets.items() if name.endswith('组')}

    product_data = pd.DataFrame()

    # 合并筛选出的表格
    for name, df in group_sheets.items():
        df = df[['店铺', '产品ID', '姓名', '产品简称']]
        df['表名字'] = name
        product_data = pd.concat([product_data, df], ignore_index=True)

    # 去除“产品简称”列
    product_data.drop(columns=['产品简称'], inplace=True)

    # 清洗“产品ID”列，删除除数字之外的其他字符并转换为文本格式
    product_data['产品ID'] = product_data['产品ID'].astype(str).str.replace(r'\D', '', regex=True)

    # 处理销量数据，将“商品id”和产品数据表中的“产品ID”匹配
    sales_data['产品ID'] = sales_data['商品id'].astype(str).str.replace(r'\D', '', regex=True)
    merged_data = pd.merge(sales_data, product_data, how='left', left_on='产品ID', right_on='产品ID')

    # 返回最终的表格
    return merged_data

#多推吧刷单
def clean_order_number(order_number):
    """清理订单号，只保留数字和短横杠"""
    return re.sub(r'[^0-9-]', '', str(order_number))

def process_sd_data(sales_data):
    # 获取程序文件所在的文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sd_folder = os.path.join(script_dir, 'sd')

    # 检查sd文件夹是否存在文件
    if not os.path.exists(sd_folder) or not any(os.path.isfile(os.path.join(sd_folder, f)) for f in os.listdir(sd_folder)):
        print("没有找到sd文件夹中的文件，不进行后续操作。")
        return sales_data

    all_files = [os.path.join(sd_folder, f) for f in os.listdir(sd_folder) if f.endswith('.xlsx')]
    sd_data = pd.DataFrame()

    # 合并所有sd文件夹中的xlsx文件
    for file in all_files:
        try:
            df = pd.read_excel(file, usecols=['平台', '订单号', '商品id', '店铺名', '实付金额', '结算金额', '商品服务费', '加速服务费', '视频服务费', '追评服务费', '行家服务费', '达人服务费', '结算状态', '下单时间'])
            # 清理订单号
            df['订单号'] = df['订单号'].apply(clean_order_number)
            sd_data = pd.concat([sd_data, df], ignore_index=True)
        except Exception as e:
            print(f"处理文件 {file} 时出错：{e}")

    # 根据平台筛选“拼多多”并结算状态选择“已结算”
    sd_data = sd_data[(sd_data['平台'] == '拼多多') & (sd_data['结算状态'] == '已结算')]

    # 删除“平台”和“结算状态”列
    sd_data.drop(columns=['平台', '结算状态'], inplace=True)

    # 计算总服务费
    sd_data['总服务费'] = (
        sd_data['结算金额'] + 
        sd_data['商品服务费'] + 
        sd_data['加速服务费'] + 
        sd_data['视频服务费'] + 
        sd_data['追评服务费'] + 
        sd_data['行家服务费'] + 
        sd_data['达人服务费'] - 
        sd_data['实付金额']
    )

    # 删除不再需要的列
    sd_data.drop(columns=['结算金额', '商品服务费', '加速服务费', '视频服务费', '追评服务费', '行家服务费', '达人服务费'], inplace=True)

    # 按照订单号去重
    sd_data.drop_duplicates(subset=['订单号'], inplace=True)

    # 将刷单数据与销量数据链接，销量表为主表
    merged_data = pd.merge(sales_data, sd_data, how='left', left_on='订单号', right_on='订单号')

    # 找到没有对应到的订单
    unmatched_orders = sd_data[~sd_data['订单号'].isin(sales_data['订单号'])]

    if not unmatched_orders.empty:
        # 导出没有对应到的订单
        unmatched_file = os.path.join(script_dir, '多推吧没有对应到的订单.xlsx')
        unmatched_orders.to_excel(unmatched_file, index=False)
        print(f"没有对应到的订单已经导出到 {unmatched_file}")

    # 返回最终的表格
    return merged_data

#接下来是成本表
def process_purchase_data(sales_data):
    # 获取程序文件所在的文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__))
    purchase_file = os.path.join(script_dir, '产品进价表.xlsx')

    # 读取所有表格
    xls = pd.ExcelFile(purchase_file)
    purchase_data = pd.DataFrame()

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        # 只保留必要的列
        df = df[['产品', '简称', '拿货价格']]
        purchase_data = pd.concat([purchase_data, df], ignore_index=True)

    # 根据产品简称去重
    purchase_data.drop_duplicates(subset=['简称'], inplace=True)

    # 清洗数据：删除产品简称为空的行
    purchase_data = purchase_data.dropna(subset=['简称'])

    # 清洗数据：删除产品简称中只包含制表符或空格的行
    purchase_data = purchase_data[~purchase_data['简称'].str.isspace()]
    purchase_data = purchase_data[purchase_data['简称'].str.strip() != '']

    # 将进价表与销量数据表链接，销量表为主表
    merged_data = pd.merge(sales_data, purchase_data, how='left', left_on='商品编码', right_on='简称')

    # 检查未找到的商品编码
    unmatched_sales = merged_data[merged_data['简称'].isnull() & merged_data['商品编码'].str.strip().ne('')]
    if not unmatched_sales.empty:
        missing_product_codes = unmatched_sales['商品编码'].tolist()
        print(f"产品进价表未找到以下商品编码：{missing_product_codes}")

    # 检查拿货价格为空的商品
    missing_prices = merged_data[merged_data['拿货价格'].isnull() & merged_data['商品编码'].str.strip().ne('')]
    if not missing_prices.empty:
        missing_price_codes = missing_prices['商品编码'].tolist()
        print(f"以下商品的拿货价格为空：{missing_price_codes}")

    # 返回最终的表格
    return merged_data

#直通车数据
def process_ztc_data():
    # 获取程序文件所在的文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ztc_folder = os.path.join(script_dir, 'ztc')

    # 如果文件夹不存在，则直接返回空数据框
    if not os.path.exists(ztc_folder):
        print(f"{ztc_folder} 文件夹不存在。")
        return pd.DataFrame()

    # 获取ztc文件夹中的所有xlsx文件
    ztc_files = [os.path.join(ztc_folder, f) for f in os.listdir(ztc_folder) if f.endswith('.xlsx')]

    ztc_data = pd.DataFrame()

    for file in ztc_files:
        try:
            # 读取文件
            df = pd.read_excel(file)
            # 删除最后一行（总计行）
            df = df.iloc[:-1]

            # 处理列名兼容性问题
            if '总花费(元)' in df.columns:
                df.rename(columns={'总花费(元)': '花费(元)'}, inplace=True)

            # 保留指定的字段
            df = df[['商品ID', '花费(元)', '交易额(元)', '实际投产比', '成交笔数', '直接成交笔数', '间接成交笔数']]

            # 合并数据
            ztc_data = pd.concat([ztc_data, df], ignore_index=True)
        except Exception as e:
            print(f"处理文件 {file} 时出错：{e}")

    # 清理数据，删除花费(元)为0的行
    ztc_data = ztc_data[ztc_data['花费(元)'] != 0]

    return ztc_data

# 调用方法处理直通车数据
ztc_data = process_ztc_data()
if not ztc_data.empty:
    print("直通车数据处理成功。")
else:
    print("没有找到直通车数据或处理直通车数据时出错。")

def main():
    #merged_data = process_sales_data()
    ##开始处理快麦数据
    #sales_data = process_sd_data(process_product_data(process_km_data(merged_data)))
#
    #sales_datas = process_purchase_data(sales_data)
    #
    #sales_datas.to_csv("D:\\git_try\\try1\\result.csv",index=False,encoding="utf-8-sig")

    #sales_datas = process_ztc_data()
    #sales_datas.to_csv("D:\\git_try\\try1\\ztc.csv",index=False,encoding="utf-8-sig")
    pass
    

if __name__ == "__main__":
    main()
