#!/usr/bin/python
#-*- coding : utf-8 -*-
#主要是拼合文件csvt特殊表头的文件

import pandas as pd
import glob,os
import urllib.request

man_URL = "c:\\do_data\\"

#获取文件目录并且放入list
def get_list():
    global man_URL
    csv_product_file_list =[]
    #获取当前文件夹下边的相同文件的
    def get_file_name_list():#传入后缀确定合并哪一个文件
        return glob.glob(r''+man_URL+'*.csv')
    csv_list = get_file_name_list()
    if csv_list is not None:
        for x in csv_list:
            try:
                csv_product_file_list.append(pd.read_csv(x,skiprows=4,encoding="gbk"))
            except:
                print("这个文件"+x+"编码错误现在用的是gbk编码")
            
    return pd.concat(csv_product_file_list)

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
    #清理数据
    asd.dropna(axis=0, how='all', inplace=True)

    asd = asd[asd["商户订单号"].str.contains('\#')==False]
    
    asd.to_csv(""+man_URL+"all.csv",index=False)

if __name__ == "__main__":
    if(kaiguan()):
        print("写入文件正常")
        writer_file()
        print("文件已经生成在"+man_URL+"文件夹内")
        os.system('pause')
        os.system("explorer.exe %s" % ""+man_URL+"")
    else:
        print("写入文件异常")