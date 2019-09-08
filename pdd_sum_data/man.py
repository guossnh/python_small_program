#!/usr/bin/python
#-*- coding : utf-8 -*-
#这个主要是谢同学使用的每天根据每个店铺导出的数据文档然后分析昨天的销量然后统计给boss
import pandas as pd
import os
Folder_Path = r'C:\\do_data'          #要拼接的文件夹及其完整路径，注意不要包含中文
SaveFile_Path =  r'C:\\do_data'       #拼接后要保存的文件路径
SaveFile_Name = r'all.csv'              #合并后要保存的文件名
 
#修改当前工作目录
os.chdir(Folder_Path)
#将该文件夹下的所有文件名存入一个列表
file_list = os.listdir()
 
#读取第一个CSV文件并包含表头
df = pd.read_csv(Folder_Path +'\\'+ file_list[0])   #编码默认UTF-8，若乱码自行更改
 
#将读取的第一个CSV文件写入合并后的文件保存
df.to_csv(SaveFile_Path+'\\'+ SaveFile_Name,encoding="utf_8_sig",index=False)
 
#循环遍历列表中各个CSV文件名，并追加到合并后的文件
for i in range(1,len(file_list)):
    df = pd.read_csv(Folder_Path + '\\'+ file_list[i])
    df.to_csv(SaveFile_Path+'\\'+ SaveFile_Name,encoding="utf_8_sig",index=False, header=False, mode='a+')
