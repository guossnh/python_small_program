import pandas as pd
import xlrd,os,glob

product_file_list =[]

def make_all_file():
    #获取桌面的需要统计的所有文件的数据
    def get_file_name_list():
        #now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        return glob.glob(r'D:\\cache\\2020年9月1日\\客服数据\\赵紫娟\\*.xls')
    global product_file_list
    for product_file in get_file_name_list():
        product_file_list.append(pd.read_excel(product_file))
    pd1 = pd.concat(product_file_list)
    pd1 = pd1.dropna(subset=["咨询人数"])
    pd1.to_csv("D:\\cache\\2020年9月1日\\客服数据\\赵紫娟.csv",index=False,sep=',')

if __name__ == "__main__":
    make_all_file()