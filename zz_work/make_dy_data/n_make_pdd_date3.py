import os
import pandas as pd
from openpyxl import load_workbook
import re
import logging

# 获取脚本目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 设置日志记录
log_file_path = os.path.join(script_dir, 'process_log.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

# 打印日志文件路径以确认
print(f"日志文件路径: {log_file_path}")

def process_sales_data():
    """
    处理销量数据：
    1. 读取file文件夹中的所有CSV文件。
    2. 保留指定列并拆分“商家编码-规格维度”列。
    3. 统计每个月的数据量和支付时间为空的记录数。
    4. 删除特定订单状态的记录。
    5. 清理商品ID数据。
    6. 返回合并后的DataFrame。
    """
    folder_path = os.path.join(script_dir, 'file')
    all_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

    merged_data = pd.DataFrame()
    error_files = []
    month_data_counts = {}
    null_payment_times = 0

    for file in all_files:
        try:
            # 读取CSV文件并保留指定的列
            df = pd.read_csv(file, usecols=['订单号', '订单状态', '支付时间', '商品数量(件)', '商品id', '商家编码-规格维度', '售后状态', '商家实收金额(元)', '快递公司',"商家备注"])
            df['商家编码-规格维度'].fillna('-', inplace=True)
            df['商家编码-规格维度'] = df['商家编码-规格维度'].astype(str)
            
            # 确保每行至少有两个部分，使用默认值填充
            def ensure_two_parts(value):
                parts = value.split('-')
                if len(parts) < 2:
                    parts.append('default')  # 填充默认值
                return '-'.join(parts)
            
            df['商家编码-规格维度'] = df['商家编码-规格维度'].apply(ensure_two_parts)
            df[['商品编码', '规格数量']] = df['商家编码-规格维度'].str.split('-', expand=True, n=1)
            
            # 统计每个月的数据量
            df['支付时间'] = pd.to_datetime(df['支付时间'], errors='coerce')
            df['月'] = df['支付时间'].dt.month
            
            for month, count in df['月'].value_counts().items():
                month_data_counts[month] = month_data_counts.get(month, 0) + count
            
            null_payment_times += df['支付时间'].isna().sum()
            
            # 删除指定订单状态的记录
            df = df[~df['订单状态'].isin(['未发货，退款成功', '已取消', '已取消，退款成功','未成交，退款成功'])]

            # 合并当前文件数据到总数据框中
            merged_data = pd.concat([merged_data, df], ignore_index=True)
        except Exception as e:
            error_files.append(file)
            logging.error(f"处理文件 {file} 时出错：{e}")

    # 清理商品ID，只保留数字并转换为文本格式
    if not merged_data.empty:
        merged_data['商品id'] = merged_data['商品id'].apply(lambda x: re.sub(r'\D', '', str(x)))

    merged_data.drop(columns=['月'], inplace=True)

    for month, count in month_data_counts.items():
        logging.info(f"月份 {month} 有 {count} 条数据")

    logging.info(f"支付时间为空值的记录数：{null_payment_times}")

    return merged_data

def process_km_data(sales_data):
    """
    处理快麦数据：
    1. 读取km文件夹中的所有CSV文件。
    2. 合并并去重。
    3. 将快麦数据与销量数据匹配。
    4. 返回更新后的销量数据。
    """
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

    missing_products = sales_data[sales_data['商品名称'].isna()]['商品编码'].unique()
    
    if len(missing_products) > 0:
        logging.warning(f"以下商品编码在快麦数据表中没有找到对应的商品名称，需要更新快麦表格：{missing_products}")

    return sales_data

def process_product_data(sales_data):
    """
    处理产品数据：
    1. 读取产品数据表格.xlsx中的所有表。
    2. 筛选名字最后一个字是“组”的表格。
    3. 合并表格并去除“产品简称”列。
    4. 清理“产品ID”列并与销量数据匹配。
    5. 返回更新后的销量数据。
    """
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

    return merged_data

def clean_order_number(order_number):
    """
    清理订单号，只保留数字和短横杠
    """
    return re.sub(r'[^0-9-]', '', str(order_number))

def process_sd_data(sales_data):
    """
    处理刷单数据：
    1. 读取sd文件夹中的所有xlsx文件。
    2. 筛选并处理指定的列。
    3. 清理订单号并计算总服务费。
    4. 根据平台和结算状态筛选数据。
    5. 将刷单数据与销量数据匹配。
    6. 导出没有对应到的订单。
    7. 返回更新后的销量数据。
    """
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
            logging.info(f"没有对应到的订单已经导出到 {unmatched_file}")
        
        return merged_data
    
    # 在没有刷单文件的情况下，直接返回原始的sales_data
    merged_data = pd.merge(sales_data, sd_data, how='left', left_on='订单号', right_on='订单号')
    return merged_data

def process_purchase_data(sales_data):
    """
    处理产品进价数据：
    1. 读取产品进价表.xlsx中的所有表。
    2. 合并表格并去重。
    3. 清理数据：删除产品简称为空或只包含空白字符的行。
    4. 将进价表与销量数据匹配。
    5. 检查未找到的商品编码并记录日志。
    6. 返回更新后的销量数据。
    """
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

    # 清理数据：删除产品简称为空或只包含空白字符的行
    purchase_data = purchase_data.dropna(subset=['简称'])
    purchase_data = purchase_data[~purchase_data['简称'].str.isspace()]
    purchase_data = purchase_data[purchase_data['简称'].str.strip() != '']

    # 将进价表与销量数据表链接，销量表为主表
    merged_data = pd.merge(sales_data, purchase_data, how='left', left_on='商品编码', right_on='简称')

    # 检查未找到的商品编码
    unmatched_sales = merged_data[merged_data['简称'].isnull() & merged_data['商品编码'].str.strip().ne('')]
    if not unmatched_sales.empty:
        missing_product_codes = unmatched_sales['商品编码'].tolist()
        logging.warning(f"产品进价表未找到以下商品编码：{missing_product_codes}")

    # 检查拿货价格为空的商品
    missing_prices = merged_data[merged_data['拿货价格'].isnull() & merged_data['商品编码'].str.strip().ne('')]
    if not missing_prices.empty:
        missing_price_codes = missing_prices['商品编码'].tolist()
        logging.warning(f"以下商品的拿货价格为空：{missing_price_codes}")

    # 返回最终的表格
    return merged_data

def process_ztc_data():
    """
    处理直通车数据：
    1. 读取ztc文件夹中的所有xlsx文件。
    2. 删除最后一行（总计行）。
    3. 处理列名兼容性问题。
    4. 合并数据并删除花费(元)为0的行。
    5. 返回直通车数据的DataFrame。
    """
    ztc_folder = os.path.join(script_dir, 'ztc')

    if not os.path.exists(ztc_folder):
        logging.info(f"{ztc_folder} 文件夹不存在。")
        return pd.DataFrame()

    # 获取ztc文件夹中的所有xlsx文件
    ztc_files = [os.path.join(ztc_folder, f) for f in os.listdir(ztc_folder) if f.endswith('.xlsx')]

    ztc_data = pd.DataFrame()

    for file in ztc_files:
        try:
            df = pd.read_excel(file)
            df = df.iloc[:-1]  # 删除最后一行（总计行）

            # 处理列名兼容性问题
            if '总花费(元)' in df.columns:
                df.rename(columns={'总花费(元)': '花费(元)'}, inplace=True)

            # 保留指定的字段
            df = df[['商品ID', '花费(元)', '交易额(元)', '实际投产比', '成交笔数', '直接成交笔数', '间接成交笔数']]

            # 合并数据
            ztc_data = pd.concat([ztc_data, df], ignore_index=True)
        except Exception as e:
            logging.error(f"处理文件 {file} 时出错：{e}")

    # 清理数据，删除花费(元)为0的行
    ztc_data = ztc_data[ztc_data['花费(元)'] != 0]

    return ztc_data

def calculate_order_cost(sales_data):
    """
    计算货物成本：
    1. 使用商品数量乘上规格数量再乘上拿货价格计算成本。
    2. 对于规格数量为default或空值的订单，使用商家实收金额的特定百分比作为成本。
    """
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
    """
    根据商家备注和总服务费确定订单属性。
    - 如果商家备注包含 'v-' 或 'V-'，则标记为放单。
    - 如果商家备注包含 'g-' 或 'G-'，则标记为刷单。
    - 如果总服务费有值，则标记为放单。
    - 其他情况标记为正常。
    """
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
    """
    为订单添加属性列，依据商家备注和总服务费来确定属性。
    """
    sales_data['订单属性'] = sales_data.apply(determine_order_attribute, axis=1)
    return sales_data

def fill_na_with_zero(df, columns):
    """
    将指定列中的空值填充为0。
    """
    for column in columns:
        df[column].fillna(0, inplace=True)
    return df

def calculate_final_order_cost(sales_data):
    """
    计算订单成本：根据订单状态不同计算订单成本。
    - 如果订单状态是“已发货，待收货”或“已收货”，订单成本为：商家实收金额(元) - 货物成本 - 实付金额 - 总服务费 - 2.5，并保留两位小数。
    - 否则，订单成本为：0 - 货物成本 - 实付金额 - 总服务费 - 2.5，并保留两位小数。
    """
    def compute_final_cost(row):
        if row['订单状态'] in ['已发货，待收货', '已收货']:
            return round(row['商家实收金额(元)'] - row['货物成本'] - row['实付金额'] - row['总服务费'] - 2.5, 2)
        else:
            return round(0 - row['货物成本'] - row['实付金额'] - row['总服务费'] - 2.5, 2)

    sales_data['订单成本'] = sales_data.apply(compute_final_cost, axis=1)
    return sales_data

def calculate_return_rate(sales_data):
    """
    计算每种快递公司的退货率：
    签收状态包括：已发货，待收货 和 已收货。
    其他状态视为退货。
    """
    # 过滤掉快递公司为空的记录
    express_data = sales_data[sales_data['快递公司'].notna() & sales_data['快递公司'].str.strip() != '']
    
    # 分组统计每个快递公司的订单数量
    total_orders = express_data['快递公司'].value_counts()
    
    # 统计每个快递公司签收状态的订单数量
    signed_orders = express_data[express_data['订单状态'].isin(['已发货，待收货', '已收货'])]['快递公司'].value_counts()
    
    # 计算退货量和退货率
    return_rates = (total_orders - signed_orders).fillna(0) / total_orders * 100
    
    # 打印并记录每个快递公司的发货量和退货率
    for company in total_orders.index:
        total = total_orders[company]
        returned = total - signed_orders.get(company, 0)
        return_rate = return_rates[company].round(2)
        logging.info(f"快递公司: {company}, 发货量: {total}, 退货率: {return_rate}%")
        print(f"快递公司: {company}, 发货量: {total}, 退货率: {return_rate}%")

def fill_na_columns(sales_data, columns, fill_value):
    """
    将指定列中的空值填充为指定值。
    """
    for column in columns:
        sales_data[column].fillna(fill_value, inplace=True)
    return sales_data

def add_simple_order_status(sales_data):
    """
    添加简易订单状态列，根据订单状态设置简易订单状态：
    - '已发货，待收货' 和 '已收货' -> '收货'
    - '已发货，退款成功' 和 '已收货，退款成功' -> '退款'
    """
    conditions = [
        sales_data['订单状态'].isin(['已发货，待收货', '已收货']),
        sales_data['订单状态'].isin(['已发货，退款成功', '已收货，退款成功'])
    ]
    choices = ['收货', '退款']
    sales_data['简易订单状态'] = pd.Series(pd.np.select(conditions, choices, default='其他'))
    return sales_data

def create_pivot_table(sales_data):
    """
    创建一个透视表，基于商品id、简易订单状态、店铺、姓名、表名字、产品、订单属性进行分组，并计算订单成本总和。
    """
    # 补全空值
    sales_data['店铺'].fillna('没有编码', inplace=True)
    sales_data['姓名'].fillna('没有编码', inplace=True)
    sales_data['表名字'].fillna('没有编码', inplace=True)
    sales_data['产品'].fillna('没有编码', inplace=True)
    sales_data['订单成本'].fillna(0, inplace=True)

    # 创建透视表
    pivot_table = sales_data.groupby(['商品id', '简易订单状态', '店铺', '姓名', '表名字', '产品', '订单属性']).agg({'订单成本': 'sum'}).reset_index()
    return pivot_table

def main():
    # 处理销量数据
    merged_data = process_sales_data()
    logging.info("销量数据处理完成")

    # 处理快麦数据
    sales_data = process_km_data(merged_data)
    logging.info("快麦数据处理完成")

    # 处理产品数据
    sales_data = process_product_data(sales_data)
    logging.info("产品数据处理完成")

    # 处理刷单数据
    sales_data = process_sd_data(sales_data)
    logging.info("刷单数据处理完成")

    # 处理产品进价数据
    sales_data = process_purchase_data(sales_data)
    logging.info("产品进价数据处理完成")

    # 计算货物成本
    sales_data = calculate_order_cost(sales_data)
    logging.info("货物成本计算完成")

    # 添加订单属性
    sales_data = add_order_attributes(sales_data)
    logging.info("订单属性添加完成")

    # 填充空值为0
    sales_data = fill_na_with_zero(sales_data, ['货物成本', '实付金额', '总服务费'])
    logging.info("空值填充为0完成")

    # 计算订单成本
    sales_data = calculate_final_order_cost(sales_data)
    logging.info("订单成本计算完成")

    # 添加简易订单状态
    sales_data = add_simple_order_status(sales_data)
    logging.info("简易订单状态添加完成")

    # 创建透视表
    pivot_table = create_pivot_table(sales_data)
    logging.info("透视表创建完成")

    # 保存结果
    result_file = os.path.join(script_dir, 'result.csv')
    sales_data.to_csv(result_file, index=False, encoding='utf-8-sig')
    logging.info(f"最终结果保存到 {result_file}")

    pivot_file = os.path.join(script_dir, 'pivot_result.csv')
    pivot_table.to_csv(pivot_file, index=False, encoding='utf-8-sig')
    logging.info(f"透视表结果保存到 {pivot_file}")

    # 处理直通车数据
    ztc_data = process_ztc_data()
    if not ztc_data.empty:
        ztc_file = os.path.join(script_dir, 'ztc_result.csv')
        ztc_data.to_csv(ztc_file, index=False, encoding='utf-8-sig')
        logging.info(f"直通车数据处理完成，结果保存到 {ztc_file}")
    else:
        logging.info("没有找到直通车数据或处理直通车数据时出错")

if __name__ == "__main__":
    main()