#!/usr/bin/python
#-*- coding : utf-8 -*-
#主要是拼合文件 xls  xldx  csv文件的拼合

import pandas as pd
import glob

man_URL = "c:\\do_data"

#获取文件目录并且放入list
def get_list():
    #获取当前文件夹下边的相同文件的
    def get_file_name_list(last_name):#传入后缀确定合并哪一个文件
        return glob.glob(r''+man_URL+'file\\*.'+last_name+'')

if __name__ == "__main__":
    pass