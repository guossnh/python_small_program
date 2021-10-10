#!/usr/bin/python
#-*- coding : utf-8 -*-

#计算抖音店铺销量的程序

import pandas as pd
import glob,os,openpyxl,re,platform
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

#获取执行程序的文件夹的路径
def get_file_folder():
    #fielpath = os.getcwd()
    global man_URL
    folder_list = os.listdir(os.path.dirname(__file__))
    if("file" in folder_list):
        print("修改工作路径")
        man_URL = os.path.dirname(__file__).replace("\\","\\\\")+"\\\\"
    else:
        print("调试路径")

#判断系统版本然后修改对应的工作路径
def find_version_of_OS():
    sysstr = platform.system()
    global man_URL,shuangxiegang
    if(sysstr =="Windows"):
        get_file_folder()
    elif(sysstr == "Darwin"):
        man_URL = "/Users/tlkzhuo/tlk/git/make_dy_data/"
    else:
        print ("Other System tasks")

#根据系统版本生成相应的路径符号
def return_symbol():
    sysstr = platform.system()
    if(sysstr =="Windows"):
        return "\\"
    elif(sysstr == "Darwin"):
        return "/"
    else:
        return "出错了"
#读取抖音文件并且返回
def  read_shell_file():
    product_file_list =[]
    def get_file_name_list():
        return glob.glob(r''+man_URL+'file'+return_symbol()+'*.csv')
        print("读取"+str(len(product_file_list))+"个销量数据文件")
 
    #放入list
    for product_file in get_file_name_list():
        try:
            product_file_list.append(pd.read_csv(product_file))
        except:
            print("数据文件"+product_file+"出现错误")
    #返回合并
    return pd.concat(product_file_list)

def make_data():
    print(read_shell_file())



if __name__ == "__main__":
    if(kaiguan()):
        print("访问正常")
        #开始判断修改操作区路径
        find_version_of_OS()
        print(man_URL)



        make_data()

    else:
        print("无法获取配置文件")
