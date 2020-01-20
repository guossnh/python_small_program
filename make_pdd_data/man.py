#-*- coding : utf-8 -*-
#这个是根据我们的拼多多销售数据分析一下数据

import xlrd,glob,os
import pandas as pd 

file_folder = "d:\\cache\\"#存放数据文件的文件夹

def get_file_link():#通过这个 方法可以获取到需要统计的文件的数组
    return glob.glob(r""+file_folder+"*")

def read_file():
    pd_list = []
    for x in get_file_link():
        pd_list.append(pd.read_excel(x))
    all_pd = pd.concat(pd_list)
    print(all_pd)

read_file()  