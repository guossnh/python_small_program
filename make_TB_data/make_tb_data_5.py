import os
import pandas as pd
import re
import glob
import warnings

# 忽略警告
warnings.filterwarnings('ignore')

def main():
    # 获取程序文件所在的文件夹目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 读取销量数据文件
    sales_data = read_sales_data(current_dir)
    
    # 筛选销量数据
    sales_data = filter_sales_data(sales_data)
    
    # 读取管家婆数据
    gjp_data = read_gjp_data(current_dir)
    
    # 处理套餐名称
    gjp_data = process_package_name(gjp_data)
    
    # 连接销量数据和管家婆数据
    sales_data = pd.merge(sales_data, gjp_data, how='left', left_on='商家编码', right_on='套餐编码')
    
    # 读取产品明细数据
    product_detail = read_product_detail(current_dir)
    
    # 连接销量数据和产品明细数据
    sales_data = pd.merge(sales_data, product_detail, how='left', left_on='套餐名称名字', right_on='产品简称')
    
    # 读取产品数据表格淘宝
    taobao_data = read_taobao_data(current_dir)
    
    # 连接销量数据和淘宝数据
    sales_data = pd.merge(sales_data, taobao_data, how='left', left_on='商品ID', right_on='产品ID')
    
    # 计算货物成本价格
    sales_data = calculate_cost(sales_data)
    
    # 生成订单类型
    sales_data = determine_order_type(sales_data)
    
    # 添加有效快递数据列
    sales_data['有效快递数据'] = 1
    
    # 计算货物数量
    sales_data = calculate_goods_quantity(sales_data)
    
    # 保存原始订单数据
    sales_data.to_csv(os.path.join(current_dir, '原始订单数据.csv'), index=False, encoding='utf-8-sig')
    
    # 创建数据透视表并导出结果
    create_pivot_table(sales_data, current_dir)
    
    print("处理完成，数据已保存到原始订单数据.csv和结果.xlsx")

def read_sales_data(current_dir):
    """读取销量数据文件"""
    file_dir = os.path.join(current_dir, 'file')
    all_files = glob.glob(os.path.join(file_dir, '*.xlsx')) + glob.glob(os.path.join(file_dir, '*.xls'))
    
    # 要读取的列
    columns = ['子订单编号', '商家编码', '订单状态', '买家实付金额', '退款状态', '商品ID', '商家备注', '购买数量']
    
    # 存储所有读取的数据
    all_data = []
    
    for file in all_files:
        try:
            # 读取Excel文件
            df = pd.read_excel(file, usecols=columns)
            
            # 处理买家实付金额，去除千位分隔符
            if '买家实付金额' in df.columns:
                df['买家实付金额'] = df['买家实付金额'].astype(str).str.replace(',', '').astype(float)
            
            # 处理商品ID，只保留数字
            if '商品ID' in df.columns:
                df['商品ID'] = df['商品ID'].astype(str).apply(lambda x: re.sub(r'\D', '', x))
            
            all_data.append(df)
        except Exception as e:
            print(f"文件 {os.path.basename(file)} 读取出错: {str(e)}")
    
    # 合并所有数据
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        # 根据子订单编号去重
        combined_data = combined_data.drop_duplicates(subset=['子订单编号'])
        return combined_data
    else:
        print("没有成功读取任何销量数据文件")
        return pd.DataFrame(columns=columns)

def filter_sales_data(sales_data):
    """筛选销量数据"""
    if sales_data.empty:
        return sales_data
    
    # 订单状态筛选
    order_status = ['买家已付款', '卖家已发货', '交易成功', '卖家已发货，等待买家确认']
    
    # 退款状态筛选
    refund_status = ['买家已经申请退款，等待卖家同意', '卖家已经同意退款，等待买家退货', '没有申请退款', '退款关闭']
    
    # 应用筛选条件
    filtered_data = sales_data[
        (sales_data['订单状态'].isin(order_status)) &
        (sales_data['退款状态'].isin(refund_status))
    ]
    
    return filtered_data

def read_gjp_data(current_dir):
    """读取管家婆数据"""
    gjp_dir = os.path.join(current_dir, 'gjp')
    all_files = glob.glob(os.path.join(gjp_dir, '*.xls')) + glob.glob(os.path.join(gjp_dir, '*.xlsx'))
    
    # 存储所有读取的数据
    all_data = []
    
    for file in all_files:
        try:
            # 跳过前10行，只读取套餐名称和套餐编码
            df = pd.read_excel(file, skiprows=10, usecols=['套餐名称', '套餐编码'])
            all_data.append(df)
        except Exception as e:
            print(f"管家婆文件 {os.path.basename(file)} 读取出错: {str(e)}")
    
    # 合并所有数据
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        # 删除空值
        combined_data = combined_data.dropna(subset=['套餐名称', '套餐编码'])
        # 根据套餐编码去重
        combined_data = combined_data.drop_duplicates(subset=['套餐编码'])
        return combined_data
    else:
        print("没有成功读取任何管家婆数据文件")
        return pd.DataFrame(columns=['套餐名称', '套餐编码'])

def process_package_name(gjp_data):
    """处理套餐名称"""
    if gjp_data.empty:
        return gjp_data
    
    # 处理套餐名称
    def process_name(name):
        # 如果有+号，删除+号及后面的内容
        if '+' in name:
            name = name.split('+')[0]
        
        # 查找数字
        match = re.search(r'(\d+)', name)
        if match:
            # 数字前的内容作为套餐名称名字
            package_name = name[:match.start()].strip()
            # 数字作为套餐名称数量
            package_quantity = match.group(1)
            return package_name, package_quantity
        else:
            # 如果没有数字，整个名称作为套餐名称名字，数量为1
            return name, '1'
    
    # 应用处理函数
    gjp_data[['套餐名称名字', '套餐名称数量']] = gjp_data['套餐名称'].apply(lambda x: pd.Series(process_name(x)))
    
    return gjp_data

def read_product_detail(current_dir):
    """读取产品明细数据"""
    file_path = os.path.join(current_dir, '产品明细.xlsx')
    
    try:
        # 读取产品明细
        product_detail = pd.read_excel(file_path, usecols=['产品名称', '产品简称', '成本价格'])
        
        # 删除成本价格为空的行
        product_detail = product_detail.dropna(subset=['成本价格'])
        
        # 根据产品简称去重
        product_detail = product_detail.drop_duplicates(subset=['产品简称'])
        
        return product_detail
    except Exception as e:
        print(f"产品明细文件读取出错: {str(e)}")
        return pd.DataFrame(columns=['产品名称', '产品简称', '成本价格'])

def read_taobao_data(current_dir):
    """读取淘宝数据"""
    file_path = os.path.join(current_dir, '产品数据表格淘宝.xlsx')
    
    try:
        # 读取Excel文件的所有表格名称
        excel = pd.ExcelFile(file_path)
        sheet_names = excel.sheet_names
        
        # 筛选出以"组"结尾的表格
        group_sheets = [sheet for sheet in sheet_names if sheet and sheet[-1] == '组']
        
        all_data = []
        
        for sheet in group_sheets:
            # 读取表格
            df = pd.read_excel(file_path, sheet_name=sheet, usecols=['店铺', '姓名', '产品ID'])
            # 添加组名字列
            df['组名字'] = sheet
            all_data.append(df)
        
        if all_data:
            # 合并所有表格数据
            combined_data = pd.concat(all_data, ignore_index=True)
            
            # 清理产品ID，只保留数字
            combined_data['产品ID'] = combined_data['产品ID'].astype(str).apply(lambda x: re.sub(r'\D', '', x))
            
            # 根据产品ID去重
            combined_data = combined_data.drop_duplicates(subset=['产品ID'])
            
            return combined_data
        else:
            print("没有找到以'组'结尾的表格")
            return pd.DataFrame(columns=['店铺', '姓名', '产品ID', '组名字'])
    except Exception as e:
        print(f"淘宝数据文件读取出错: {str(e)}")
        return pd.DataFrame(columns=['店铺', '姓名', '产品ID', '组名字'])

def calculate_cost(sales_data):
    """计算货物成本价格"""
    if sales_data.empty:
        return sales_data
    
    # 确保所需列存在
    required_columns = ['购买数量', '套餐名称数量', '成本价格']
    for col in required_columns:
        if col not in sales_data.columns:
            print(f"警告: 计算货物成本价格时缺少必要列 '{col}'")
            sales_data['货物成本价格'] = None
            return sales_data
    
    # 将列转换为数值类型
    sales_data['购买数量'] = pd.to_numeric(sales_data['购买数量'], errors='coerce')
    sales_data['套餐名称数量'] = pd.to_numeric(sales_data['套餐名称数量'], errors='coerce')
    sales_data['成本价格'] = pd.to_numeric(sales_data['成本价格'], errors='coerce')
    
    # 计算货物成本价格
    sales_data['货物成本价格'] = sales_data['购买数量'] * sales_data['套餐名称数量'] * sales_data['成本价格']
    
    return sales_data

def determine_order_type(sales_data):
    """生成订单类型"""
    if sales_data.empty or '商家备注' not in sales_data.columns:
        if not sales_data.empty:
            sales_data['订单类型'] = '真实'
        return sales_data
    
    # 将商家备注转换为字符串类型
    sales_data['商家备注'] = sales_data['商家备注'].astype(str)
    
    # 定义判断订单类型的函数
    def get_order_type(remark):
        if pd.isna(remark) or remark == 'nan':
            return '真实'
        
        remark = str(remark).lower()
        
        if any(pattern in remark for pattern in ['g-', 'g_']):
            return '刷单'
        elif any(pattern in remark for pattern in ['v-', 'v_']):
            return '放单'
        else:
            return '真实'
    
    # 应用函数生成订单类型
    sales_data['订单类型'] = sales_data['商家备注'].apply(get_order_type)
    
    return sales_data

def calculate_goods_quantity(sales_data):
    """计算货物数量"""
    if sales_data.empty:
        return sales_data
    
    # 确保所需列存在
    required_columns = ['购买数量', '套餐名称数量']
    for col in required_columns:
        if col not in sales_data.columns:
            print(f"警告: 计算货物数量时缺少必要列 '{col}'")
            sales_data['货物数量'] = None
            return sales_data
    
    # 将列转换为数值类型
    sales_data['购买数量'] = pd.to_numeric(sales_data['购买数量'], errors='coerce')
    sales_data['套餐名称数量'] = pd.to_numeric(sales_data['套餐名称数量'], errors='coerce')
    
    # 计算货物数量
    sales_data['货物数量'] = sales_data['购买数量'] * sales_data['套餐名称数量']
    
    return sales_data

def create_pivot_table(sales_data, current_dir):
    """创建数据透视表并导出结果"""
    if sales_data.empty:
        print("警告: 无法创建数据透视表，数据为空")
        return
    
    # 确保所需列存在
    required_columns = ['店铺', '姓名', '组名字', '订单类型', '产品简称', '套餐名称名字', 
                        '有效快递数据', '买家实付金额', '货物成本价格', '货物数量']
    
    missing_columns = [col for col in required_columns if col not in sales_data.columns]
    if missing_columns:
        print(f"警告: 创建数据透视表时缺少必要列: {', '.join(missing_columns)}")
        # 为缺失的列添加默认值
        for col in missing_columns:
            sales_data[col] = None
    
    # 创建数据透视表
    pivot_table = pd.pivot_table(
        sales_data,
        index=['店铺', '姓名', '组名字', '订单类型', '产品简称', '套餐名称名字'],
        values=['有效快递数据', '买家实付金额', '货物成本价格', '货物数量'],
        aggfunc='sum'
    )
    
    # 重置索引，将索引转换为列
    pivot_table = pivot_table.reset_index()
    
    # 修改列名
    column_mapping = {
        '套餐名称名字': '产品名',
        '买家实付金额': '销售额',
        '货物成本价格': '货物总成本'
    }
    
    pivot_table = pivot_table.rename(columns=column_mapping)
    
    # 导出结果
    result_path = os.path.join(current_dir, '结果.xlsx')
    pivot_table.to_excel(result_path, index=False)
    print(f"数据透视表已保存到: {result_path}")

if __name__ == "__main__":
    main()