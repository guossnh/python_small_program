import os
import pandas as pd
from openpyxl import load_workbook
from pathlib import Path
import logging

# 设置日志记录
logging.basicConfig(filename='process_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def process_sales_data():
    """处理销量数据"""
    try:
        current_dir = os.path.dirname(__file__)
        sales_folder = os.path.join(current_dir, 'file')
        
        # 读取所有csv文件并合并
        sales_data = pd.DataFrame()
        for file in os.listdir(sales_folder):
            if file.endswith('.csv'):
                file_path = os.path.join(sales_folder, file)
                try:
                    df = pd.read_csv(file_path, usecols=['订单号', '订单状态', '支付时间', '商品数量(件)', '商品id',
                                                         '商家编码-规格维度', '售后状态', '商家实收金额(元)', '快递公司'])
                    sales_data = pd.concat([sales_data, df], ignore_index=True)
                    logging.info(f"成功读取销量文件: {file}")
                except pd.errors.EmptyDataError:
                    logging.warning(f"销量文件为空: {file}")
                except Exception as e:
                    logging.error(f"读取销量文件失败: {file}, 错误信息: {e}")
                    raise
        
        if sales_data.empty:
            logging.warning("未找到任何有效销量数据，退出程序。")
            return None
        
        # 去除重复订单号
        sales_data.drop_duplicates(subset=['订单号'], inplace=True)
        
        # 检查并替换空值为"-"
        sales_data['商家编码-规格维度'].fillna('-', inplace=True)
        
        # 判断并拆分商家编码-规格维度列
        sales_data[['商品编码', '规格数量']] = sales_data['商家编码-规格维度'].str.split('-', expand=True)
        logging.info("商家编码-规格维度列拆分成功。")
        
        # 清洗支付时间列
        if '支付时间' in sales_data.columns:
            sales_data['支付时间'] = pd.to_datetime(sales_data['支付时间'], errors='coerce')
            month_counts = sales_data['支付时间'].dt.month.value_counts()
            dominant_month = month_counts.idxmax()
            sales_data = sales_data[sales_data['支付时间'].dt.month == dominant_month]
        
        # 清洗商品id列
        if '商品id' in sales_data.columns:
            sales_data['商品id'] = sales_data['商品id'].astype(str).str.replace(r'\D', '', regex=True)
        
        return sales_data
    
    except Exception as e:
        logging.error(f"处理销量数据出错: {e}")
        raise

def process_km_data(sales_data):
    """处理快麦数据并与销量数据链接"""
    try:
        current_dir = os.path.dirname(__file__)
        km_folder = os.path.join(current_dir, 'km')
        
        # 读取所有csv文件并合并
        km_data = pd.DataFrame()
        for file in os.listdir(km_folder):
            if file.endswith('.csv'):
                file_path = os.path.join(km_folder, file)
                try:
                    df = pd.read_csv(file_path, skiprows=6, usecols=['商品商家编码', '商品名称'], encoding='GB18030')
                    km_data = pd.concat([km_data, df], ignore_index=True)
                    logging.info(f"成功读取快麦文件: {file}")
                except Exception as e:
                    logging.error(f"读取快麦文件失败: {file}, 错误信息: {e}")
                    raise
        
        if km_data.empty:
            logging.warning("未找到任何有效快麦数据，退出程序。")
            return None
        
        # 去除重复商品商家编码
        km_data.drop_duplicates(subset=['商品商家编码'], inplace=True)
        
        # 与销量数据进行链接
        km_data = pd.merge(km_data, sales_data[['商品id', '订单号', '支付时间']], how='left', left_on='商品商家编码', right_on='商品id')
        logging.info("快麦数据与销量数据链接完成。")
        
        return km_data
    
    except Exception as e:
        logging.error(f"处理快麦数据出错: {e}")
        raise

def process_product_data(sales_data):
    """处理产品数据并与销量数据链接"""
    try:
        current_dir = os.path.dirname(__file__)
        product_file = os.path.join(current_dir, '产品数据表格.xlsx')
        
        # 读取所有表格
        product_data = pd.DataFrame()
        xls = pd.ExcelFile(product_file)
        for sheet_name in xls.sheet_names:
            if sheet_name.endswith('组'):
                df = pd.read_excel(product_file, sheet_name=sheet_name, usecols=['店铺', '产品ID', '姓名', '产品简称'])
                df['表名字'] = sheet_name
                product_data = pd.concat([product_data, df], ignore_index=True)
                logging.info(f"成功读取产品表格: {sheet_name}")
        
        if product_data.empty:
            logging.warning("未找到任何有效产品数据，退出程序。")
            return None
        
        # 去除产品简称列
        if '产品简称' in product_data.columns:
            product_data.drop(columns=['产品简称'], inplace=True)
        
        # 清洗产品ID列
        if '产品ID' in product_data.columns:
            product_data['产品ID'] = product_data['产品ID'].astype(str).str.replace(r'\D', '', regex=True)
        
        # 与销量数据进行链接
        product_data = pd.merge(product_data, sales_data[['商品id', '订单号', '支付时间']], how='left', left_on='产品ID', right_on='商品id')
        logging.info("产品数据与销量数据链接完成。")
        
        return product_data
    
    except Exception as e:
        logging.error(f"处理产品数据出错: {e}")
        raise

def process_dtb_data(sales_data):
    """处理多推吧数据并与销量数据链接"""
    try:
        current_dir = os.path.dirname(__file__)
        dtb_folder = os.path.join(current_dir, 'sd')
        
        # 读取所有xlsx文件并合并
        dtb_data = pd.DataFrame()
        for file in os.listdir(dtb_folder):
            if file.endswith('.xlsx'):
                file_path = os.path.join(dtb_folder, file)
                try:
                    df = pd.read_excel(file_path, skipfooter=1,
                                       usecols=['平台', '订单号', '商品id', '店铺名', '实付金额', '结算金额',
                                                '商品服务费', '加速服务费', '视频服务费', '追评服务费',
                                                '行家服务费', '达人服务费', '结算状态', '下单时间'])
                    df = df[df['平台'] == '拼多多']
                    df = df[df['结算状态'] == '已结算']
                    dtb_data = pd.concat([dtb_data, df], ignore_index=True)
                    logging.info(f"成功读取多推吧文件: {file}")
                except Exception as e:
                    logging.error(f"读取多推吧文件失败: {file}, 错误信息: {e}")
                    raise
        
        if dtb_data.empty:
            logging.warning("未找到任何有效多推吧数据，退出程序。")
            return None
        
        # 去除重复订单号
        dtb_data.drop_duplicates(subset=['订单号'], inplace=True)
        
        # 与销量数据进行链接
        dtb_data = pd.merge(dtb_data, sales_data[['订单号', '支付时间']], how='left', on='订单号')
        logging.info("多推吧数据与销量数据链接完成。")
        
        return dtb_data
    
    except Exception as e:
        logging.error(f"处理多推吧数据出错: {e}")
        raise

def process_cost_data(sales_data):
    """处理进价数据并与销量数据链接"""
    try:
        current_dir = os.path.dirname(__file__)
        cost_file = os.path.join(current_dir, '产品进价表.xlsx')
        
        # 读取所有表格并合并
        cost_data = pd.DataFrame()
        xls = pd.ExcelFile(cost_file)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(cost_file, sheet_name=sheet_name, usecols=['产品', '简称', '拿货价格'])
            cost_data = pd.concat([cost_data, df], ignore_index=True)
            logging.info(f"成功读取进价表格: {sheet_name}")
        
        if cost_data.empty:
            logging.warning("未找到任何有效进价数据，退出程序。")
            return None
        
        # 清洗产品列
        if '产品' in cost_data.columns:
            cost_data['产品'] = cost_data['产品'].astype(str).str.replace(r'\D', '', regex=True)
        
        # 与销量数据进行链接
        cost_data = pd.merge(cost_data, sales_data[['商品id', '订单号', '支付时间']], how='left', left_on='产品', right_on='商品id')
        logging.info("进价数据与销量数据链接完成。")
        
        return cost_data
    
    except Exception as e:
        logging.error(f"处理进价数据出错: {e}")
        raise

def process_ztc_data(sales_data):
    """处理直通车数据并与销量数据链接"""
    try:
        current_dir = os.path.dirname(__file__)
        ztc_folder = os.path.join(current_dir, 'file')
        
        # 读取所有csv文件并合并
        ztc_data = pd.DataFrame()
        for file in os.listdir(ztc_folder):
            if file.startswith('直通车') and file.endswith('.csv'):
                file_path = os.path.join(ztc_folder, file)
                try:
                    df = pd.read_csv(file_path, usecols=['关键词', '直通车广告费(元)', '展现量', '点击量', '点击率', '点击转化率', '成交笔数',
                                                         '间接成交笔数'])
                    ztc_data = pd.concat([ztc_data, df], ignore_index=True)
                    logging.info(f"成功读取直通车文件: {file}")
                except Exception as e:
                    logging.error(f"读取直通车文件失败: {file}, 错误信息: {e}")
                    raise
        
        if ztc_data.empty:
            logging.warning("未找到任何有效直通车数据，退出程序。")
            return None
        
        # 与销量数据进行链接
        ztc_data = pd.merge(ztc_data, sales_data[['订单号', '支付时间']], how='left', on='订单号')
        logging.info("直通车数据与销量数据链接完成。")
        
        return ztc_data
    
    except Exception as e:
        logging.error(f"处理直通车数据出错: {e}")
        raise

def export_original_sales_data(sales_data):
    """导出原始销量数据表格"""
    try:
        current_dir = os.path.dirname(__file__)
        output_file = os.path.join(current_dir, '原始数据表格.csv')
        sales_data.to_csv(output_file, index=False, encoding='utf-8-sig')
        logging.info("成功导出原始数据表格.csv")
    except Exception as e:
        logging.error(f"导出原始数据表格失败: {e}")

def main():
    """主函数"""
    try:
        logging.info("程序开始执行。")
        
        # 处理销量数据
        sales_data = process_sales_data()
        if sales_data is not None:
            logging.info("销量数据处理完成。")
            export_original_sales_data(sales_data)
        else:
            logging.warning("处理销量数据时出现问题，程序退出。")
            return
        
        # 处理快麦数据
        km_data = process_km_data(sales_data)
        if km_data is not None:
            logging.info("快麦数据处理完成。")
        else:
            logging.warning("处理快麦数据时出现问题，程序退出。")
        
        # 处理产品数据
        product_data = process_product_data(sales_data)
        if product_data is not None:
            logging.info("产品数据处理完成。")
        else:
            logging.warning("处理产品数据时出现问题，程序退出。")
        
        # 处理多推吧数据
        dtb_data = process_dtb_data(sales_data)
        if dtb_data is not None:
            logging.info("多推吧数据处理完成。")
        else:
            logging.warning("处理多推吧数据时出现问题，程序退出。")
        
        # 处理进价数据
        cost_data = process_cost_data(sales_data)
        if cost_data is not None:
            logging.info("进价数据处理完成。")
        else:
            logging.warning("处理进价数据时出现问题，程序退出。")
        
        # 处理直通车数据
        ztc_data = process_ztc_data(sales_data)
        if ztc_data is not None:
            logging.info("直通车数据处理完成。")
        else:
            logging.warning("处理直通车数据时出现问题，程序退出。")
        
        # 其他操作...
        
        logging.info("所有数据处理完成")
    
    except Exception as e:
        logging.error(f"发生异常: {e}")
        raise

if __name__ == "__main__":
    main()
