#-*- coding : utf-8 -*-
#之前的太乱了往后整合到一块去
#重复筛选提醒

import pandas as pd
import numpy as np
import time,os,datetime,glob,sys,csv,xlrd
import urllib.request

boy_name = ""
product_list =[]
product_file_list =[]
man_URL = "d:\\make_everyday_PDD_date_for_YY\\"
#简称和全称的字典数据
product_ename_and_aname = {}
#直通车数据对象
shell_car_data = ""

#======================华丽的分割线======================

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
    print("读取"+str(len(product_file_list))+"个销量数据文件")
    #放入list
    for product_file in get_file_name_list():
        try:
            product_file_list.append(pd.read_csv(product_file))
        except:
            print("数据文件"+product_file+"出现错误")
    #返回合并
    return pd.concat(product_file_list)

#建立直通车的pandas对象
def get_car_data_to_pd():
    global shell_car_data
    car_money_file_list=[]#初始化文件路径list
    car_money_pd =[]#初始化直通车数据对象list
    car_money_file_list = glob.glob(r''+man_URL+'file\\*.xls')#获取所有的直通车文件list
    print("总共需要处理"+str(len(car_money_file_list))+"个直通车文件")
    for x in car_money_file_list:
        try:
            car_money_pd.append(pd.read_excel(x))
        except:
            print("直通车文件"+x+"出现错误")
    shell_car_data = pd.concat(car_money_pd)

#通过这个方法可以查询直通车的数据
def find_carmoney_data(productID):
    global shell_car_data
    productID = str(productID)
    one_resultpd = shell_car_data[(shell_car_data['推广计划'].str.find(productID, start=0, end=None)>=0)]
    if(len(one_resultpd)):
        return one_resultpd["花费(元)"].sum()
    else:
        return 0

#这块是通过各类数据开始计算结果
def compute_result(df,shell_date):
    #筛选需要统计的销量信息
    shell_date = shell_date[(shell_date["售后状态"]=="无售后或售后取消")|(shell_date["售后状态"]=="售后处理中")]
    shell_date = shell_date[(shell_date["订单状态"]=="待发货")|(shell_date["订单状态"]=="已发货，待签收")|(shell_date["订单状态"]=="已签收")]

    shell_date["商品id"].astype("str")
    #开始计算
    #先修改名字  不修改的话带括号的名字在计算的时候容易出错
    shell_date = shell_date.rename(columns={'商家实收金额(元)':'商家实收金额'})
    #创建一个方法用来区分单条数据是干预，真实，网站放单
    def return_type(x):
        try:
            if((x.find('V-')!= -1)|(x.find('v-')!= -1)):
                return 1
            elif((x.find('G-')!= -1)|(x.find('g-')!=-1)):
                return 2
            else:
                return 0
        except:
            return 0
    #总共销量表格加入type区分干预，真实，网站放单
    shell_date['type'] = shell_date.商家备注.apply(return_type)
    #在df表里边加入各种销量数据
    v_shell_data = shell_date[shell_date['type']==1]
    g_shell_data = shell_date[shell_date['type']==2]
    t_shell_data = shell_date[shell_date['type']==0]
    df['销量'] = df.产品ID.apply(lambda x : t_shell_data.商家实收金额.loc[t_shell_data.商品id == x].sum())
    df['干预'] = df.产品ID.apply(lambda x : g_shell_data.商家实收金额.loc[g_shell_data.商品id == x].sum())
    df['放单'] = df.产品ID.apply(lambda x : v_shell_data.商家实收金额.loc[v_shell_data.商品id == x].sum())
    #在df表里边加入直通车数据
    df['直通车'] = df.产品ID.apply(find_carmoney_data)

    #加入全称数据可以不显示
    df['商品全称'] = df.产品简称.apply(find_product_full_name2)

    return df

#写出文件
def write_file2(df):
    global man_URL
    df.to_csv(""+man_URL+day_time('today')+"result.csv",index=False,encoding="utf-8-sig",columns=['店铺','产品简称','商品全称','姓名','产品ID','组','销量','干预','放单','直通车'])

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

#检测执行步骤到哪一步卡死了
def content():
    print("载入配置文件")
    df = read_config_xlsx_new()
    print("开始载入销量数据")
    shell_date = get_sell_date_to_pd()
    print("载入直通车数据")
    get_car_data_to_pd()
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
