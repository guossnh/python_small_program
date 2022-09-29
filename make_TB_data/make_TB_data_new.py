#-*- coding : utf-8 -*-
#新版的淘宝这边的程序计算。
#拼多多有的功能大约都要添加一下  合拍单子的情况需要根据比例计算清楚

import pandas as pd
import numpy as np
import time,os,datetime,glob,sys,csv,xlrd,re
import urllib.request


man_URL = "d:\\应用\\ceshi15\\"
shell_car_data = ""

#==========================================基础部分==========================================
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

#这个方法是检测相同的ID的方法
def find_same_ID(df):
    same_id_num = int(df[df.duplicated('产品ID')].count()["产品ID"])#获取重复数量
    if(same_id_num>0):
        print("发现重复记录"+str(same_id_num)+"条")
        print("导出重复记录到默认路径"+day_time("today")+"重复的ID.csv")
        df[df.duplicated('产品ID')].to_csv(""+man_URL+day_time("today")+"重复.csv")
        return df.drop_duplicates("产品ID")
    else:
        print("没有发现重复的ID")
        return df

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

#这个方法调用之后返回住文件夹下边的file文件夹里边的相同后缀名的文件的list
def get_file_name_list(last_name,folder='file'):
    return glob.glob(r''+man_URL+''+folder+'\\*.'+last_name+'')



#==========================================逻辑部分==========================================
#根据简称检索全称并且返回
def find_product_full_name2(easyname):
    global product_ename_and_aname
    try:
        return product_ename_and_aname[easyname]
    except:
        return easyname

#这个是判断网络链接的方法 
def kaiguan2():
    req = urllib.request.Request('http://guossnh.com/if/if.json')
    result = urllib.request.urlopen(req).read().decode('utf-8')
    if(result[0:1]=="1"):
        return True
    else:
        return False

#这块是把产品明细读取一下加入数据表
def get_product_price_file():
    global man_URL
    x2 = pd.read_excel(""+man_URL+"产品明细.xlsx")
    x2 = x2[["产品简称","成本价格"]]#只保留有需要的两列
    x2 = x2.rename(columns={'产品简称':'产品简称2'})
    #清理重复数据
    x2 = x2.drop_duplicates("产品简称2")
    return x2

#读取读取并且合并多个管家婆下载的文件
def add_GJP_file_for_code():
    global shell_car_data

    #读取相应文件夹下边的所有xls格式文件
    def get_file_name_list(last_name):
        return glob.glob(r''+man_URL+'gjp\\*.'+last_name+'')

    print("开始读取管家婆数据")
    xl_list = get_file_name_list("xls")
    gjp_list = []
    for x in xl_list:
        try:
            gjp_list.append(pd.read_excel(x,skiprows=10))
        except:
            print("读取管家婆文件"+x+"出现错误")
    shell_gjp_data = pd.concat(gjp_list)
    shell_gjp_data = shell_gjp_data[["套餐名称","套餐编码"]]
    return shell_gjp_data

#读取配置文件分成两部分第一部分吧组数据放在一个对象了里，第二部分把所有的其他的
def read_config_xlsx_new():
    global man_URL,product_ename_and_aname
    xl = pd.read_excel(""+man_URL+"产品数据表格.xlsx",None)
    xl_list =[]
    for x in xl.keys():
        xl = pd.read_excel(""+man_URL+"产品数据表格.xlsx",x)#读取文件

        if(x.find("组")!= -1):
            xl['产品ID'] = pd.to_numeric(xl['产品ID'], errors='coerce')#将产品ID转化为数字格式

            #开始清理数据
            xl = xl.loc[:,["店铺","产品简称","姓名","产品ID"]]#只保留有需要的四列
            xl = xl.dropna(subset=['产品ID']) #删除确实ID的行
            xl = xl.dropna(axis=0,how='all') #删除为NaN的行

            xl.insert(xl.shape[1], '组', x)#将组名插入到数据里边

            xl_list.append(xl)#将所有的组数据放入list
        elif(x.find("数据")!= -1):
            for row in xl.itertuples():
                product_ename_and_aname[getattr(row, '产品简称')] = getattr(row, '产品名称')#载入全称简称转换字典数据
                #如果需要增加转化数据的话可以放在这里
    df = pd.concat(xl_list)
    #清理重复ID部分
    same_id_num = int(df[df.duplicated('产品ID')].count()["产品ID"])#获取重复数量
    if(same_id_num>0):
        print("发现重复记录"+str(same_id_num)+"条")
        print("导出重复记录到默认路径"+day_time("today")+"重复.csv")
        df[df.duplicated('产品ID')].to_csv(""+man_URL+day_time("today")+"重复.csv")
        return df.drop_duplicates("产品ID")
    else:
        print("没有发现重复的ID")
        return df

#读取所有的销量文件放在一块不需要筛选时间
def get_sell_date_to_pd():
    #获取程序文件夹里边的需要统计的所有文件的数据
    def get_file_name_list():
        return glob.glob(r''+man_URL+'file\\*.csv')
    global product_file_list
    print("读取"+str(len(get_file_name_list()))+"个销量数据文件")
    #放入list
    for product_file in get_file_name_list():
        try:
            product_file_list.append(pd.read_csv(product_file))
        except:
            print("数据文件"+product_file+"出现错误")
    #返回合并
    return pd.concat(product_file_list)

#==========================================控制部分==========================================
#检测执行步骤到哪一步卡死了
def content():
    print("判断路径")
    get_file_folder()
    print("载入配置文件")
    df = read_config_xlsx_new()
    print("开始载入销量数据")
    shell_date = get_sell_date_to_pd()
    print("载入直通车数据")
    if(get_car_data_to_pd()):
        print("直通车数据载入完毕")
    else:
        print("直通车数据是空不参与计算")
    print("开始计算")
    df = compute_result(df,shell_date)
    print("开始生成结果")
    write_file2(df)
    print("结束了")
    os.system('pause')
    os.system("explorer.exe %s" % ""+man_URL+"")

#主函数
if __name__ == "__main__":
    content()