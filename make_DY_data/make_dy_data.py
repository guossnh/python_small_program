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
    if(sysstr =="Windows"):
        get_file_folder()
    elif(sysstr == "Linux"):
        print ("Call Linux tasks")
    else:
        print ("Other System tasks")



def make_data():
    pass



if __name__ == "__main__":
    if(kaiguan()):
        print("访问正常")
        #开始判断修改操作区路径
        find_version_of_OS()
          



        make_data()

    else:
        print("无法获取配置文件")
