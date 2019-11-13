#-*- coding : utf-8 -*-
#根据桌面的下载数据统计生成需要的文件发送给会计

import pandas as pd
import time,os,datetime,glob,sys

desktop_link = "C:\\Users\\Administrator\\Desktop\\"


#获取桌面的需要统计的文件的数量
def get_file_name_list():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    return glob.glob(r''+desktop_link+'*'+now_time+'*.csv')


def get_productID_and_productName():
    date = pd.read_csv(""+sys.path[0]+"\\product_name_id.csv")
    print(date)

if __name__ == "__main__":
    get_productID_and_productName()
    
    
