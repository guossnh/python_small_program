
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
            df = pd.read_csv(file, encoding='utf-8')  # 你可以尝试其他编码，如'gb2312'、'utf-16'

            # 保留需要的列
            df_filtered = df[required_columns]

            # 确保相关列的数据类型为字符串类型
            for col in ['商品ID', '商家编码', '商家备注', '订单状态', '售后状态']:
                df_filtered[col] = df_filtered[col].astype(str)

            # 处理订单应付金额，去除千位分隔符并转换为浮点数
            df_filtered['订单应付金额'] = df_filtered['订单应付金额'].str.replace(',', '').astype(float)

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
