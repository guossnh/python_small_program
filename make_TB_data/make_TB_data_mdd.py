#!/usr/bin/python
#-*- coding : utf-8 -*-

#ps文件需要检测 密码  刚开始的时候需要检测系统是啥

import pandas as pd
import glob,os,openpyxl,re
import urllib.request


def kaiguan():
    req = urllib.request.Request('http://guossnh.com/if/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False

#判断系统的版本看是linux还是win
def find_os_version():
    if(os.name==posix):
        return "0"
    else:
        return "1"

def make_data():
    print(os.name)



if __name__ == "__main__":
    if(kaiguan()):
        print("访问正常")
        make_data()
        #read_product_excle()
    else:
        print("无法获取配置文件")