#!/usr/bin/python
#-*- coding : utf-8 -*-

#计算抖音店铺销量的程序

import pandas as pd
import glob,os,openpyxl,re
import urllib.request  

man_URL = "d:\\应用\\make_TB_data\\"
shell_car_data = ""

#这个方法调用之后返回住文件夹下边的file文件夹里边的相同后缀名的文件的list
def get_file_name_list(last_name):
    return glob.glob(r''+man_URL+'file\\*.'+last_name+'')

def kaiguan():
    req = urllib.request.Request('http://guossnh.com/if/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False


def make_data():
    pass



if __name__ == "__main__":
    if(kaiguan()):
        print("访问正常")
        make_data()
        print(os.getcwd())
        #read_product_excle()
    else:
        print("无法获取配置文件")
