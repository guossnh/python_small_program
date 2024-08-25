import os
import pandas as pd
from openpyxl import load_workbook
import re
import logging
import numpy as np

# 获取脚本目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 设置日志记录
log_file_path = os.path.join(script_dir, 'process_log.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

# 打印日志文件路径以确认
print(f"日志文件路径: {log_file_path}")

def process_sales_data():
    folder_path = os.path.join(script_dir, 'file')
    all_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

    merged_data = pd.DataFrame()
    error_files = []
    month_data_counts = {}
    null_payment_times = 0

    for file in all_files:
        try:
            df = pd.read_csv(file, usecols=['订单号', '订单状态', '支付时间', '商品数量(件)', '商品id', '商家编码-规格维度', '售后状态', '商家实收金额(元)', '快递公司', '商家备注'])
            df['商家编码-规格维度'].fillna('-', inplace=True)
            df['商家编码-规格维度'] = df['商家编码-规格维度'].astype(str)
            df['文件名'] = os.path.basename(file)
            
            def ensure_two_parts(value):
                parts = value.split('-')
                if len(parts) < 2:
                    parts.append('default')
                return '-'.join(parts)
             
            df['商家编码-规格维度'] = df['商家编码-规格维度'].apply(ensure_two_parts)
            df[['商品编码', '规格数量']] = df['商家编码-规格维度'].str.split('-', expand=True, n=1)
            
            df['支付时间'] = pd.to_datetime(df['支付时间'], errors='coerce')
            df['月'] = df['支付时间'].dt.month
            
            for month, count in df['月'].value_counts().items():
                month_data_counts[month] = month_data_counts.get(month, 0) + count
            
            null_payment_times += df['支付时间'].isna().sum()
            
            df = df[~df['订单状态'].isin(['未发货，退款成功', '已取消', '已取消，退款成功','未成交，退款成功'])]

            merged_data = pd.concat([merged_data, df], ignore_index=True)
        except Exception as e:
            error_files.append(file)
            logging.error(f"处理文件 {file} 时出错：{e}")

    if not merged_data.empty:
        merged_data['商品id'] = merged_data['商品id'].apply(lambda x: re.sub(r'\D', '', str(x)))

    merged_data.drop(columns=['月'], inplace=True)

    for month, count in month_data_counts.items():
        logging.info(f"月份 {month} 有 {count} 条数据")

    logging.info(f"支付时间为空值的记录数：{null_payment_times}")

    return merged_data

def process_km_data(sales_data):
    km_folder_path = os.path.join(script_dir, 'km')
    all_km_files = [os.path.join(km_folder_path, file) for file in os.listdir(km_folder_path) if file.endswith('.csv')]

    km_data = pd.DataFrame()

    for file in all_km_files:
        try:
            df = pd.read_csv(file, skiprows=6, usecols=['商品商家编码', '商品名称'], encoding='GB18030')
            km_data = pd.concat([km_data, df], ignore_index=True)
        except Exception as e:
            logging.error(f"处理文件 {file} 时出错：{e}")

    km_data = km_data.drop_duplicates(subset=['商品商家编码'])

    product_code_to_name = pd.Series(km_data['商品名称'].values, index=km_data['商品商家编码']).to_dict()

    sales_data['商品名称'] = sales_data['商品编码'].map(product_code_to_name)

    def fill_missing_product_names(group):
        if group['商品名称'].notna().any():
            most_common_name = group['商品名称'].dropna().mode()[0]
            group['商品名称'].fillna(most_common_name, inplace=True)
        return group

    sales_data = sales_data.groupby('商品id').apply(fill_missing_product_names).reset_index(drop=True)

    missing_products = sales_data[sales_data['商品名称'].isna()]['商品编码'].unique()
    
    if len(missing_products) > 0:
        logging.warning(f"以下商品编码在快麦数据表中没有找到对应的商品名称，需要更新快麦表格：{missing_products}")

    return sales_data

def process_product_data(sales_data):
    product_data_file = os.path.join(script_dir, '产品数据表格.xlsx')
    all_sheets = pd.read_excel(product_data_file, sheet_name=None)
    group_sheets = {name: df for name, df in all_sheets.items() if name.endswith('组')}

    product_data = pd.DataFrame()

    for name, df in group_sheets.items():
        df = df[['店铺', '产品ID', '姓名', '产品简称']]
        df['表名字'] = name
        product_data = pd.concat([product_data, df], ignore_index=True)

    product_data.drop(columns=['产品简称'], inplace=True)
    product_data['产品ID'] = product_data['产品ID'].astype(str).str.replace(r'\D', '', regex=True)

    sales_data['产品ID'] = sales_data['商品id'].astype(str).str.replace(r'\D', '', regex=True)
    merged_data = pd.merge(sales_data, product_data, how='left', left_on='产品ID', right_on='产品ID')

    def fill_missing_shops(group):
        if group['店铺'].isnull().all():
            return group
        
        most_common_shop = group['店铺'].mode()[0]
        group['店铺'].fillna(most_common_shop, inplace=True)
        return group

    merged_data = merged_data.groupby('文件名').apply(fill_missing_shops).reset_index(drop=True)

    return merged_data

def clean_order_number(order_number):
    return re.sub(r'[^0-9-]', '', str(order_number))

def process_sd_data(sales_data):
    sd_folder = os.path.join(script_dir, 'sd')

    if not os.path.exists(sd_folder) or not any(os.path.isfile(os.path.join(sd_folder, f)) for f in os.listdir(sd_folder)):
        logging.info("没有找到sd文件夹中的文件，生成包含指定列的空DataFrame。")
        sd_data = pd.DataFrame(columns=['店铺名', '实付金额', '总服务费', '下单时间'])
    else:
        all_files = [os.path.join(sd_folder, f) for f in os.listdir(sd_folder) if f.endswith('.xlsx')]
        sd_data = pd.DataFrame()

        for file in all_files:
            try:
                df = pd.read_excel(file, usecols=['平台', '订单号', '店铺名', '实付金额', '结算金额', '商品服务费', '加速服务费', '视频服务费', '追评服务费', '行家服务费', '达人服务费', '结算状态', '下单时间'])
                df['订单号'] = df['订单号'].apply(clean_order_number)
                sd_data = pd.concat([sd_data, df], ignore_index=True)
            except Exception as e:
                logging.error(f"处理文件 {file} 时出错：{e}")

        sd_data = sd_data[(sd_data['平台'] == '拼多多') & (sd_data['结算状态'] == '已结算')]
        sd_data.drop(columns=['平台', '结算状态'], inplace=True)

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

        sd_data.drop(columns=['结算金额', '商品服务费', '加速服务费', '视频服务费', '追评服务费', '行家服务费', '达人服务费'], inplace=True)
        sd_data.drop_duplicates(subset=['订单号'], inplace=True)

        merged_data = pd.merge(sales_data, sd_data, how='left', left_on='订单号', right_on='订单号')

        unmatched_orders = sd_data[~sd_data['订单号'].isin(sales_data['订单号'])]

        if not unmatched_orders.empty:
            unmatched_file = os.path.join(script_dir, '多推吧没有对应到的订单.xlsx')
            unmatched_orders.to_excel(unmatched_file, index=False)
            logging.info(f"没有对应到的订单已经导出到 {unmatched_file}")
        
        return merged_data
    
    merged_data = pd.merge(sales_data, sd_data, how='left', left_on='订单号', right_on='订单号')
    return merged_data

def process_purchase_data(sales_data):
    purchase_file = os.path.join(script_dir, '产品进价表.xlsx')
    xls = pd.ExcelFile(purchase_file)
    purchase_data = pd.DataFrame()

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df = df[['产品', '简称', '拿货价格']]
        purchase_data = pd.concat([purchase_data, df], ignore_index=True)

    purchase_data.drop_duplicates(subset=['简称'], inplace=True)
    purchase_data = purchase_data.dropna(subset=['简称'])
    purchase_data = purchase_data[~purchase_data['简称'].str.isspace()]
    purchase_data = purchase_data[purchase_data['简称'].str.strip() != '']

    merged_data = pd.merge(sales_data, purchase_data, how='left', left_on='商品编码', right_on='简称')

    unmatched_sales = merged_data[merged_data['简称'].isnull() & merged_data['商品编码'].str.strip().ne('')]
    if not unmatched_sales.empty:
        missing_product_codes = unmatched_sales['商品编码'].tolist()
        logging.warning(f"产品进价表未找到以下商品编码：{missing_product_codes}")

    missing_prices = merged_data[merged_data['拿货价格'].isnull() & merged_data['商品编码'].str.strip().ne('')]
    if not missing_prices.empty:
        missing_price_codes = missing_prices['商品编码'].tolist()
        logging.warning(f"以下商品的拿货价格为空：{missing_price_codes}")

    return merged_data

def process_ztc_data():
    ztc_folder = os.path.join(script_dir, 'ztc')

    if not os.path.exists(ztc_folder):
        logging.info(f"{ztc_folder} 文件夹不存在。")
        return pd.DataFrame()

    ztc_files = [os.path.join(ztc_folder, f) for f in os.listdir(ztc_folder) if f.endswith('.xlsx')]

    ztc_data = pd.DataFrame()

    for file in ztc_files:
        try:
            df = pd.read_excel(file)
            df = df.iloc[:-1]

            if '总花费(元)' in df.columns:
                df.rename(columns={'总花费(元)': '花费(元)'}, inplace=True)

            df = df[['商品ID', '花费(元)', '交易额(元)', '实际投产比', '成交笔数', '直接成交笔数', '间接成交笔数']]

            ztc_data = pd.concat([ztc_data, df], ignore_index=True)
        except Exception as e:
            logging.error(f"处理文件 {file} 时出错：{e}")

    ztc_data = ztc_data[ztc_data['花费(元)'] != 0]

    return ztc_data

def calculate_order_cost(sales_data):
    def calculate_cost(row):
        try:
            quantity = float(row['商品数量(件)'])
            spec_quantity = float(row['规格数量'])
            purchase_price = float(row['拿货价格'])
            return quantity * spec_quantity * purchase_price
        except ValueError:
            sales_amount = float(row['商家实收金额(元)'])
            if sales_amount > 5:
                return sales_amount * 0.5
            else:
                return sales_amount * 0.8

    sales_data['货物成本'] = sales_data.apply(calculate_cost, axis=1)
    return sales_data

def determine_order_attribute(row):
    remark = str(row['商家备注']).lower() if '商家备注' in row else ''
    if 'v-' in remark or 'V-' in remark:
        return '放单'
    elif 'g-' in remark or 'G-' in remark:
        return '刷单'
    elif not pd.isna(row['总服务费']):
        return '放单'
    else:
        return '正常'

def add_order_attributes(sales_data):
    sales_data['订单属性'] = sales_data.apply(determine_order_attribute, axis=1)
    return sales_data

def fill_na_with_zero(df, columns):
    for column in columns:
        df[column].fillna(0, inplace=True)
    return df

def calculate_final_order_cost(sales_data):
    def compute_final_cost(row):
        if row['订单状态'] in ['已发货，待收货', '已收货']:
            return round(row['商家实收金额(元)'] - row['货物成本'] - row['实付金额'] - row['总服务费'] - 2.7, 2)
        else:
            return round(0 - row['货物成本'] - row['实付金额'] - row['总服务费'] - 2.7, 2)

    sales_data['订单成本'] = sales_data.apply(compute_final_cost, axis=1)
    return sales_data

def calculate_return_rate(sales_data):
    express_data = sales_data[sales_data['快递公司'].notna() & sales_data['快递公司'].str.strip() != '']
    
    total_orders = express_data['快递公司'].value_counts()
    
    signed_orders = express_data[express_data['订单状态'].isin(['已发货，待收货', '已收货'])]['快递公司'].value_counts()
    
    return_rates = (total_orders - signed_orders).fillna(0) / total_orders * 100
    
    for company in total_orders.index:
        total = total_orders[company]
        returned = total - signed_orders.get(company, 0)
        return_rate = return_rates[company].round(2)
        logging.info(f"快递公司: {company}, 发货量: {total}, 退货率: {return_rate}%")
        print(f"快递公司: {company}, 发货量: {total}, 退货率: {return_rate}%")

def fill_na_columns(sales_data, columns, fill_value):
    for column in columns:
        sales_data[column].fillna(fill_value, inplace=True)
    return sales_data

def add_simple_order_status(sales_data):
    conditions = [
        sales_data['订单状态'].isin(['已发货，待收货', '已收货']),
        sales_data['订单状态'].isin(['已发货，退款成功', '已收货，退款成功'])
    ]
    choices = ['收货', '退款']
    sales_data['简易订单状态'] = pd.Series(np.select(conditions, choices, default='其他'))
    return sales_data

def create_pivot_table(sales_data):
    sales_data['店铺'].fillna('没有ID', inplace=True)
    sales_data['姓名'].fillna('没有ID', inplace=True)
    sales_data['表名字'].fillna('没有ID', inplace=True)
    sales_data['商品名称'].fillna('没有编码', inplace=True)
    sales_data['订单成本'].fillna(0, inplace=True)

    aggregated_data = sales_data.groupby([
        '商品id', '简易订单状态', '订单属性', '店铺', '姓名', '表名字', '商品名称'
    ]).agg({'订单成本': 'sum'}).reset_index()

    pivot_table = aggregated_data.pivot_table(
        values='订单成本',
        index=['商品id', '店铺', '姓名', '表名字'],
        columns=['简易订单状态', '订单属性'],
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    product_names = aggregated_data.groupby(['商品id', '店铺', '姓名', '表名字'])['商品名称'].apply(lambda x: ', '.join(x.unique())).reset_index()

    pivot_table = pd.merge(pivot_table, product_names, on=['商品id', '店铺', '姓名', '表名字'], how='left')

    pivot_table.columns = ['商品id', '店铺', '姓名', '表名字'] + ['_'.join(col).strip() for col in pivot_table.columns[4:-1]] + ['商品名称']

    return pivot_table

def merge_ztc_data(pivot_table, ztc_data):
    required_columns = ['商品id', '花费(元)', '交易额(元)', '实际投产比', '成交笔数', '直接成交笔数', '间接成交笔数']
    
    if ztc_data.empty:
        ztc_data = pd.DataFrame(columns=required_columns)
    else:
        ztc_data.rename(columns={'商品ID': '商品id'}, inplace=True)
    
    for col in required_columns:
        if col not in ztc_data.columns:
            ztc_data[col] = 0
    
    ztc_data['商品id'] = ztc_data['商品id'].str.lower()
    pivot_table['商品id'] = pivot_table['商品id'].str.lower()

    merged_table = pd.merge(pivot_table, ztc_data, on='商品id', how='left')

    merged_table.fillna(0, inplace=True)

    merged_table.columns = merged_table.columns.str.replace('_', '')

    merged_table = merged_table.loc[:, ~merged_table.columns.duplicated()]

    return merged_table

def main():
    merged_data = process_sales_data()
    logging.info("销量数据处理完成")

    sales_data = process_km_data(merged_data)
    logging.info("快麦数据处理完成")

    sales_data = process_product_data(sales_data)
    logging.info("产品数据处理完成")

    sales_data = process_sd_data(sales_data)
    logging.info("刷单数据处理完成")

    sales_data = process_purchase_data(sales_data)
    logging.info("产品进价数据处理完成")

    sales_data = calculate_order_cost(sales_data)
    logging.info("货物成本计算完成")

    sales_data = add_order_attributes(sales_data)
    logging.info("订单属性添加完成")

    sales_data = fill_na_with_zero(sales_data, ['货物成本', '实付金额', '总服务费'])
    logging.info("空值填充为0完成")

    sales_data = calculate_final_order_cost(sales_data)
    logging.info("订单成本计算完成")

    sales_data = add_simple_order_status(sales_data)
    logging.info("简易订单状态添加完成")

    pivot_table = create_pivot_table(sales_data)
    logging.info("透视表创建完成")

    ztc_data = process_ztc_data()
    merged_pivot_table = merge_ztc_data(pivot_table, ztc_data)
    logging.info("直通车数据合并完成")

    calculate_return_rate(sales_data)
    logging.info("退货率计算完成")

    result_file = os.path.join(script_dir, 'result.csv')
    sales_data.to_csv(result_file, index=False, encoding='utf-8-sig')
    logging.info(f"最终结果保存到 {result_file}")

    pivot_file = os.path.join(script_dir, 'pivot_result.csv')
    merged_pivot_table.to_csv(pivot_file, index=False, encoding='utf-8-sig')
    logging.info(f"透视表结果保存到 {pivot_file}")

    if not ztc_data.empty:
        ztc_file = os.path.join(script_dir, 'ztc_result.csv')
        ztc_data.to_csv(ztc_file, index=False, encoding='utf-8-sig')
        logging.info(f"直通车数据处理完成，结果保存到 {ztc_file}")

if __name__ == "__main__":
    main()
