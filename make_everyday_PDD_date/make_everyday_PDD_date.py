#-*- coding : utf-8 -*-
#根据桌面的下载数据统计生成需要的文件发送给会计

import pandas as pd
import time,os,datetime,glob

desktop_link = "C:\\Users\\Administrator\\Desktop\\"


#获取桌面的需要统计的文件的数量
def get_file_name_list():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    return glob.glob(r''+desktop_link+'*'+now_time+'*.csv')


if __name__ == "__main__":
    get_file_name_list()