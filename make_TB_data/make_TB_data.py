#!/usr/bin/python
#-*- coding : utf-8 -*-
#主要是拼合文件csvt特殊表头的文件


#到时候需要检测文件的密码

import pandas as pd
import glob,os
import urllib.request   

man_URL = "d:\\应用\\make_TB_data\\"
shell_car_data = ""

 
 #这个方法调用之后返回住文件夹下边的file文件夹里边的相同后缀名的文件的list
def get_file_name_list(last_name):
    return glob.glob(r''+man_URL+'file\\*.'+last_name+'')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#读取读取并且合并多个管家婆下载的文件
def add_GJP_file_for_code():
    global shell_car_data
    print("开始读取管家婆数据")
    xl_list = get_file_name_list("xls")
    gjp_list = []
    for x in xl_list:
        try:
            gjp_list.append(pd.read_excel(x,skiprows=11))
        except:
            print("读取管家婆文件"+x+"出现错误")
    shell_car_data = pd.concat(gjp_list)
    #return shell_car_data


#这个 方法主要就是并且把产品编码和sku名称拿出来予以对应返
def get_sku_name_from_code(code):
    #https://blog.csdn.net/w55100/article/details/90145191
    #可以上边的页面 先测试再查找坐标
    global shell_car_data
    shell_car_data[shell_car_data["套餐编码"]==code].index.tolist()
    
    #判断数组是不是为空如

def content():
    #流程如下 首先合并管家婆导出的文件这样可以实现编码和产品sku名字对应
    add_GJP_file_for_code()


if __name__ == "__main__":
    content()#调用主要方法
