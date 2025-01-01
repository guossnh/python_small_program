import os
import pandas as pd

# 获取程序文件所在的文件夹路径
def get_program_directory():
    program_path = os.path.abspath(__file__)
    program_directory = os.path.dirname(program_path)
    return program_directory

# 获取当前文件夹下 'file' 文件夹内的所有CSV文件
def get_csv_files():
    file_folder = os.path.join(get_program_directory(), 'file')
    csv_files = [f for f in os.listdir(file_folder) if f.endswith('.csv')]
    return [os.path.join(file_folder, file) for file in csv_files]

# 获取当前文件夹下 'GJP' 文件夹内的所有XLS文件
def get_xls_files():
    gjp_folder = os.path.join(get_program_directory(), 'gjp')
    xls_files = [f for f in os.listdir(gjp_folder) if f.endswith('.xls') or f.endswith('.xlsx')]
    return [os.path.join(gjp_folder, file) for file in xls_files]

# 获取当前文件夹下的 'dy产品数据表格.xlsx'
def get_dy_product_data():
    product_data_file = os.path.join(get_program_directory(), 'dy产品数据表格.xlsx')

    try:
        # 读取 Excel 文件中的所有表格
        xls = pd.ExcelFile(product_data_file)
        
        all_data = []
        
        # 遍历所有表格
        for sheet_name in xls.sheet_names:
            # 只读取表格名最后一个字是"组"的表格
            if sheet_name.endswith('组'):
                df = pd.read_excel(xls, sheet_name=sheet_name)

                # 给表格添加一列，列名为"组"
                df['组'] = sheet_name

                # 清理产品ID，将其转化为文本格式并去除非数字字符
                df['产品ID'] = df['产品ID'].astype(str).str.replace(r'\D', '', regex=True)

                # 将处理后的DataFrame加入到列表
                all_data.append(df)

        # 合并所有符合条件的表格
        combined_data = pd.concat(all_data, ignore_index=True) if all_data else None
        
        return combined_data
    except Exception as e:
        print(f"读取文件 {product_data_file} 时出错: {e}")
        return None

# 处理CSV数据
def process_sales_data():
    csv_files = get_csv_files()
    all_data = []

    # 指定需要保留的列
    required_columns = ['主订单编号', '商品数量', '商品ID', '商家编码', 
                        '订单应付金额', '商家备注', '售后状态', '订单状态']

    # 逐个读取文件并处理
    for file in csv_files:
        try:
            # 尝试读取文件时指定编码格式
            df = pd.read_csv(file, encoding='gbk')  # 你可以尝试其他编码，如'gb2312'、'utf-16'

            # 保留需要的列
            df_filtered = df[required_columns]

            # 确保商品ID为字符串类型
            df_filtered['商品ID'] = df_filtered['商品ID'].astype(str)

            # 筛选"订单状态"列，只保留"已发货"和"已完成"状态
            df_filtered = df_filtered[df_filtered['订单状态'].isin(['已发货', '已完成'])]

            # 筛选"售后状态"列，只保留"-"和"售后关闭"状态
            df_filtered = df_filtered[df_filtered['售后状态'].isin(['-', '售后关闭'])]

            # 去除'商家编码'列中的空格和换行符
            df_filtered['商家编码'] = df_filtered['商家编码'].str.replace(r'\s+', '', regex=True)

            # 将处理后的DataFrame加入到合并列表
            all_data.append(df_filtered)
        except Exception as e:
            print(f"读取文件 {file} 时出错: {e}")

    # 合并所有的DataFrame
    combined_data = pd.concat(all_data, ignore_index=True)
    
    return combined_data

# 处理GJP数据
def process_gjp_data():
    xls_files = get_xls_files()
    all_data = []

    # 指定需要保留的列
    required_columns = ['套餐名称', '套餐编码', '套餐成本金额']

    # 逐个读取文件并处理
    for file in xls_files:
        try:
            # 读取XLS文件，忽略前10行
            df = pd.read_excel(file, skiprows=10)

            # 保留需要的列
            df_filtered = df[required_columns]

            # 去重，依据'套餐编码'列去除重复项
            df_filtered = df_filtered.drop_duplicates(subset=['套餐编码'], keep='first')

            # 去除'套餐编码'列中的空格和换行符
            df_filtered['套餐编码'] = df_filtered['套餐编码'].str.replace(r'\s+', '', regex=True)

            # 将处理后的DataFrame加入到合并列表
            all_data.append(df_filtered)
        except Exception as e:
            print(f"读取文件 {file} 时出错: {e}")

    # 合并所有的DataFrame
    combined_data = pd.concat(all_data, ignore_index=True)
    
    return combined_data

# 合并销售数据和GJP数据
def merge_sales_and_gjp_data():
    # 获取合并后的销售数据
    sales_data = process_sales_data()

    # 获取合并后的GJP数据
    gjp_data = process_gjp_data()

    # 根据 '商家编码' 和 '套餐编码' 列进行合并
    merged_data = pd.merge(sales_data, gjp_data, left_on='商家编码', right_on='套餐编码', how='left')

    return merged_data

# 合并所有数据：销售数据、GJP数据和产品数据
def merge_all_data():
    # 获取合并后的销售数据和GJP数据
    merged_data = merge_sales_and_gjp_data()

    # 获取 dy产品数据表格.xlsx 数据
    product_data = get_dy_product_data()

    if product_data is not None:
        # 确保两个ID列都是字符串类型
        merged_data['商品ID'] = merged_data['商品ID'].astype(str)
        product_data['产品ID'] = product_data['产品ID'].astype(str)

        # 对product_data根据产品ID去重
        product_data = product_data.drop_duplicates(subset=['产品ID'], keep='first')

        # 根据 '商品ID' 和 '产品ID' 进行合并
        merged_data = pd.merge(merged_data, product_data, left_on='商品ID', right_on='产品ID', how='left')

    return merged_data

# 处理商家备注并添加类型标记
def add_order_type(merged_data):
    def determine_type(remark):
        if pd.isna(remark):  # 处理空值情况
            return '真实'
        remark = str(remark).lower()  # 转换为小写以统一处理
        if 'v-' in remark:
            return '放单'
        elif 'g-' in remark:
            return '刷单'
        return '真实'

    # 添加新的type列
    merged_data['type'] = merged_data['商家备注'].apply(determine_type)
    return merged_data

# 处理套餐名称并分离数量
def process_package_name(merged_data):
    def clean_package_name(name):
        if pd.isna(name):
            return name
        # 分割并获取第一个"+"之前的内容
        return name.split('+')[0].strip()
    
    def extract_name_and_quantity(name):
        try:
            if pd.isna(name):
                return pd.Series({'套餐产品名称': None, '套餐数量': None})
            
            import re
            # 查找第一个数字
            match = re.search(r'(\d+).*$', str(name).strip())
            if match:
                # 获取数字的起始位置
                num_start = name.find(match.group(1))
                # 尝试转换数字
                try:
                    quantity = int(match.group(1))
                    product_name = name[:num_start].strip()
                    if product_name:  # 确保产品名称不为空
                        return pd.Series({'套餐产品名称': product_name, '套餐数量': quantity})
                except ValueError:
                    return pd.Series({'套餐产品名称': None, '套餐数量': None})
            
            # 如果没有找到有效的数字或产品名称，返回空值
            return pd.Series({'套餐产品名称': None, '套餐数量': None})
            
        except Exception as e:
            # 如果处理过程中出现任何错误，返回空值
            print(f"处理数据时出错: {e}, 数据: {name}")
            return pd.Series({'套餐产品名称': None, '套餐数量': None})

    # 创建数据副本
    merged_data = merged_data.copy()
    
    # 首先处理加号并保存到临时列
    temp_names = merged_data['套餐名称'].apply(clean_package_name)
    
    # 然后对处理完加号的名称进行数字分离
    name_quantity_df = temp_names.apply(extract_name_and_quantity)
    merged_data[['套餐产品名称', '套餐数量']] = name_quantity_df
    
    # 计算总数量 = 商品数量 * 套餐数量
    merged_data.loc[:, '总数量'] = merged_data['商品数量'] * merged_data['套餐数量']
    
    # 添加有效订单数量列，默认值为1
    merged_data.loc[:, '有效订单数量'] = 1
    
    return merged_data

# 读取产品明细数据
def get_product_details():
    try:
        file_path = os.path.join(get_program_directory(), '产品明细.xlsx')
        # 只读取指定的三列数据
        product_details = pd.read_excel(
            file_path,
            usecols=['产品名称', '产品简称', '成本价格']
        )
        
        # 创建数据副本
        product_details = product_details.copy()
        
        # 删除产品简称或成本价格为空的行
        product_details = product_details.dropna(subset=['产品简称', '成本价格'])
        
        # 如果过滤后没有数据，返回None
        if product_details.empty:
            print("警告：产品明细表过滤后没有有效数据！")
            return None
            
        # 根据产品简称去除重复行，保留第一次出现的记录
        product_details = product_details.drop_duplicates(subset=['产品简称'], keep='first')
            
        return product_details
    except Exception as e:
        print(f"读取产品明细文件时出错: {e}")
        return None

def main():
    # 获取合并后的所有数据
    merged_data = merge_all_data()
    
    if merged_data is not None:
        # 添加订单类型
        merged_data = add_order_type(merged_data)
        # 处理套餐名称
        merged_data = process_package_name(merged_data)
        
        # 读取产品明细数据并进行链接
        product_details = get_product_details()
        if product_details is not None:
            # 使用左连接合并数据，基于套餐产品名称和产品简称
            merged_data = pd.merge(
                merged_data,
                product_details,
                left_on='套餐产品名称',
                right_on='产品简称',
                how='left'
            )
            
            # 计算总成本 = 成本价格 * 总数量
            merged_data['货物总成本'] = merged_data['成本价格'] * merged_data['总数量']
        
        # 重命名相关列
        merged_data = merged_data.rename(columns={
            'type': '类型',
            '总数量': '货物总数量',
            '有效订单数量': '有效快递数量',
            '订单应付金额': '有效销售额',
        })
        
        # 导出原始数据到CSV文件
        output_csv_path = os.path.join(get_program_directory(), '结果.csv')
        try:
            # 将主订单编号列转换为字符串格式
            if '主订单编号' in merged_data.columns:
                merged_data['主订单编号'] = merged_data['主订单编号'].astype(str)
            
            merged_data.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
            print(f"原始数据已成功导出到: {output_csv_path}")
        except Exception as e:
            print(f"导出原始数据时出错: {e}")

        # 创建数据透视表
        try:
            # 创建详细数据透视表
            pivot_table = pd.pivot_table(
                merged_data,
                index=['店铺', '姓名', '组', '类型', '产品简称'],  # 分组字段
                values=['货物总数量', '货物总成本', '有效销售额', '有效快递数量'],  # 需要聚合的字段
                aggfunc={
                    '货物总数量': 'sum',     # 货物总数量求和
                    '货物总成本': 'sum',     # 货物总成本求和
                    '有效销售额': 'sum',     # 有效销售额求和
                    '有效快递数量': 'sum'    # 有效快递数量求和
                }
            )

            # 创建总表数据透视表
            summary_table = pd.pivot_table(
                merged_data,
                index=['店铺', '组', '类型'],  # 分组字段
                values=['有效销售额'],        # 只需要有效销售额
                aggfunc={'有效销售额': 'sum'} # 求和
            )

            # 导出数据透视表到Excel文件
            output_excel_path = os.path.join(get_program_directory(), '结果.xlsx')
            with pd.ExcelWriter(output_excel_path) as writer:
                pivot_table.to_excel(writer, sheet_name='详细数据')  # 第一个sheet
                summary_table.to_excel(writer, sheet_name='总表')    # 第二个sheet
            
            print(f"数据透视表已成功导出到: {output_excel_path}")
        except Exception as e:
            print(f"创建或导出数据透视表时出错: {e}")
        
        print("数据处理完成！")
    else:
        print("合并数据时出错！")

# 运行主函数
if __name__ == "__main__":
    main()
    # 添加等待用户输入
    input("\n按回车键退出程序...")
