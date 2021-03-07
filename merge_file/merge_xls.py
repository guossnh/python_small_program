#!/usr/bin/python
#-*- coding : utf-8 -*-
#主要是拼合文件 xls 文件的拼合

import pandas as pd
import glob,xlrd,xlwt,openpyxl
import urllib.request

man_URL = "c:\\do_data\\"

xls_product_file_list= []

#获取文件目录并且放入list
def get_list():
    global xls_product_file_list
    #获取当前文件夹下边的相同文件的
    def get_file_name_list():#传入后缀确定合并哪一个文件
        return glob.glob(r''+man_URL+'*.xls')
    xls_list = get_file_name_list()
    if xls_list is not None:
        for xls_product_file in xls_list:
            xls_product_file_list.append(pd.read_excel(xls_product_file))
    return pd.concat(xls_product_file_list)

def kaiguan():
    req = urllib.request.Request('http://guossnh.com/if/if_sum_all_xls.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False

#开始写入文件
def writer_file():
    asd = get_list()
    asd.to_excel(""+man_URL+"all.xlsx")

if __name__ == "__main__":
    if(kaiguan()):
        print("写入文件正常")
        writer_file()
    else:
        print("写入文件异常")