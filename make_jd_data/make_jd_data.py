#-*- coding : utf-8 -*-
#京东的计算程序

import pandas as pd
import numpy as np
import time,os,datetime,glob,sys,csv,xlrd,re
import urllib.request

man_URL = "d:\\应用\\ceshi17\\"


#======================通用方法======================
#获取时间比较多就放在一块了
def day_time(day):
    today_time = datetime.datetime.now()
    today_time = today_time.strftime('%Y%m%d')
    yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)
    yes_time = yes_time.strftime('%Y%m%d')
    if(day=="today"):
        return today_time 
    elif(day=="yestday"):
        return yes_time
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

#这个是判断网络链接的方法 
def kaiguan2():
    req = urllib.request.Request('http://guossnh.com/if/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False


#======================计算方法======================



#======================华丽的分割线======================


if __name__ == "__main__":
    if(kaiguan2()):
        print("访问正常")
        #开始判断修改操作区路径
        get_file_folder()
        #读取快卖数据获取产品信息和产品简称用于做对称

    else:
        print("无法获取配置文件")
